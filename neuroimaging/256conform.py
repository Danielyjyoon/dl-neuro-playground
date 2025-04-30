import os
import argparse
import numpy as np
import nibabel as nib

def map_image(img, out_affine, out_shape, ras2ras=np.array([[1.0, 0, 0, 0],
                                                              [0, 1, 0, 0],
                                                              [0, 0, 1, 0],
                                                              [0, 0, 0, 1]]),
              order=1):
    """
    Function to map image to new voxel space (RAS orientation).

    :param nibabel.MGHImage img: the source 3D image with data and affine set.
    :param np.ndarray out_affine: target image affine.
    :param np.ndarray out_shape: target image shape.
    :param np.ndarray ras2ras: additional mapping (default is identity).
    :param int order: order of interpolation (0=nearest, 1=linear (default), etc.).
    :return: new_data (mapped image array) and vox2vox (the voxel-to-voxel transform).
    """
    from scipy.ndimage import affine_transform
    from numpy.linalg import inv

    # Compute vox2vox transformation from source to target
    vox2vox = inv(out_affine) @ ras2ras @ img.affine

    # Get image data (if multiple frames, squeeze to a single image)
    image_data = np.asanyarray(img.dataobj)
    if len(image_data.shape) > 3:
        if any(s != 1 for s in image_data.shape[3:]):
            raise ValueError(f"Multiple input frames {tuple(image_data.shape)} not supported!")
        image_data = np.squeeze(image_data, axis=tuple(range(3, len(image_data.shape))))

    # Apply the inverse transform to map the source image into target space
    new_data = affine_transform(image_data, inv(vox2vox), output_shape=out_shape, order=order)
    return new_data, vox2vox

def conform_PET(source_path, target_path, save_files=True, order=1):
    """
    Python version of mri_convert -c.
    
    Reslices images to standard position, fills slices to 256x256x256 format and enforces 1 mm isotropic voxel sizes.
    It first interpolates (float image) and then rescales to uchar.
    
    :param str source_path: path to the input image.
    :param str target_path: path where the conformed image will be saved.
    :param bool save_files: if True, the output is saved.
    :param int order: interpolation order (default is 1, linear).
    :return: the new image object.
    """
    from nibabel.freesurfer.mghformat import MGHHeader

    img = nib.load(source_path)
    cwidth = 256  # standard width
    csize = 1     # 1 mm isotropic voxels
    h1 = MGHHeader.from_header(img.header)  # May copy parameters if input was in MGH format

    # Set new shape and voxel dimensions
    h1.set_data_shape([cwidth, cwidth, cwidth, 1])
    h1.set_zooms([csize, csize, csize])
    h1['Mdc'] = [[-1, 0, 0],
                 [0, 0, -1],
                 [0, 1, 0]]
    h1['fov'] = cwidth
    h1['Pxyz_c'] = img.affine.dot(np.hstack((np.array(img.shape[:3]) / 2.0, [1])))[:3]

    # Map the image into the new voxel space
    mapped_data, orig_to_256 = map_image(img, h1.get_affine(), h1.get_data_shape(), order=order)

    new_img = nib.MGHImage(mapped_data, h1.get_affine(), h1)
    if save_files:
        nib.save(new_img, target_path)
        print("Wrote file:", target_path)
    
    # Return a new image object of the same type as the input
    return type(img)(mapped_data, affine=h1.get_affine(), header=h1)

def main():
    parser = argparse.ArgumentParser(
        description="Conform the specified source file in each subfolder of root_dir into a 256x256x256 image."
    )
    parser.add_argument("--root_dir", type=str, required=True,
                        help="Path to the root directory containing subfolders.")
    parser.add_argument("--source_file", type=str, required=True,
                        help="Name of the source file to process (e.g., PET.nii).")
    args = parser.parse_args()

    # Iterate over subdirectories in the root directory
    for subdir in os.listdir(args.root_dir):
        subdir_path = os.path.join(args.root_dir, subdir)
        if os.path.isdir(subdir_path):
            source_path = os.path.join(subdir_path, args.source_file)
            if os.path.exists(source_path):
                target_file = "256_" + args.source_file
                target_path = os.path.join(subdir_path, target_file)
                print(f"Processing {source_path} -> {target_path}")
                try:
                    conform_PET(source_path, target_path, save_files=True, order=1)
                except Exception as e:
                    print(f"Error processing {source_path}: {e}")
            else:
                print(f"File {args.source_file} not found in {subdir_path}")

if __name__ == "__main__":
    main()
