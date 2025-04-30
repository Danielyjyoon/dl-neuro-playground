# 🧠 Neuroimaging Utilities

This repository contains a collection of scripts and tools for multimodal brain imaging processing.  
It is organized by modality and includes pipelines for coregistration, conversion, and standardized preprocessing.

---

## 📁 Folder Overview

### 🧪 `amyloid/`
Scripts and resources related to amyloid PET image processing.

### ⚡ `FDG/`
Processing pipelines for FDG-PET including quantification and normalization workflows.

### 🎯 `DOPA_PET/`
Dopaminergic PET analysis scripts.  
Includes:
- Preprocessing pipeline
- A reference **template** for spatial normalization

### 🧠 `FreeSurfer/`
Automated `recon-all` execution and post-processing scripts such as:
- T1/T2-based reconstruction
- Brainstem segmentation
- `.mgz` to `.nii` conversion
- DKT label merging

---

## 🔧 General Utilities (in this directory)

### 🧭 `Nipype_coregistration/`
Nipype-based coregistration workflows.

### 🔀 `ANTS_coregistration/`
Scripts for coregistration using [ANTs](http://stnava.github.io/ANTs/).

### 🧾 `dicom_2_nifti/`
Batch conversion scripts from DICOM to NIfTI using `dcm2niix`.

### 🧱 `256conform/`
Utility to conform images to 256×256×256 resolution and voxel spacing — often required for FreeSurfer compatibility.

---

---

## 📦 Requirements

To install the required Python packages, run:

```bash
pip install -r requirements.txt
