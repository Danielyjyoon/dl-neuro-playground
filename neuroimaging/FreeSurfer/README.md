# 🧠 FreeSurfer Utilities

This folder contains bash and Python scripts to streamline FreeSurfer processing, including:

- recon-all automation (T1-only / T1+T2 FLAIR)
- Brainstem segmentation
- MGZ → NIfTI conversion
- Brainstem-DKT label merging

## 📜 Script List

| Script File | Description |
|-------------|-------------|
| `recon_all_single.sh` | Run recon-all for a single subject |
| `recon_all_bs_only.sh` | Only brainstem segmentation for one subject |
| `recon_all_iter.sh` | Iterate recon-all across all subject directories |
| `recon_all_iter_bs.sh` | Iterate brainstem segmentation only |
| `convert_mgz_to_nii.sh` | Convert specific `.mgz` files to `.nii` |
| `merge_brainstem.py` | (To be implemented) Merge brainstem segmentation into DKT label |

## 🚀 Usage

```bash
bash recon_all_iter.sh
