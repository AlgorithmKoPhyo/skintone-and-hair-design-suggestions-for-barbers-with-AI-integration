# Face Shape Classification

A face shape classification system that uses computer vision and machine learning to classify human face shapes.

## Dataset Setup

Before running the face shape classification module, you need to download the face shape dataset.

### 1. Download the Dataset

Download the **Face Shape Dataset** from Kaggle:

[Face Shape Dataset — Kaggle](https://www.kaggle.com/datasets/niten19/face-shape-dataset?utm_source=chatgpt.com)

Download the dataset and extract it.

### 2. Create the Training Dataset Directory

Inside the project, create the following directory:

```text
modules/
└── face_shape_classification/
    └── data/
        └── raw/
            └── training_set/
```

The final path should be:

```text
modules/face_shape_classification/data/raw/training_set/
```

### 3. Add the Dataset

Copy the extracted face shape dataset images into:

```text
modules/face_shape_classification/data/raw/training_set/
```

The directory should contain the face-shape image classes provided by the dataset.

For example:

```text
modules/
└── face_shape_classification/
    └── data/
        └── raw/
            └── training_set/
                ├── Oval/
                ├── Round/
                ├── Square/
                ├── Heart/
                ├── Diamond/
                └── Oblong/
```

> **Important:** Do not commit the dataset to Git if the repository's `.gitignore` is configured to exclude training data. Download the dataset separately and place it in the required directory.

## Usage

After placing the dataset in the correct directory, run the face shape classification module according to the project's training/inference commands.

Make sure the required Python dependencies are installed before running the module.

### Dataset Location

The application expects the raw training images at:

```text
modules/face_shape_classification/data/raw/training_set/
```

If this directory or the required dataset images are missing, the face shape classification pipeline may not work correctly.

## Project Structure

```text
project/
├── modules/
│   └── face_shape_classification/
│       ├── data/
│       │   └── raw/
│       │       └── training_set/
│       └── ...
├── .gitignore
└── README.md
```

## Notes

* The dataset must be downloaded separately from Kaggle.
* Place the extracted training images in the specified `training_set` directory.
* Do not commit large datasets or generated training files unless they are intentionally required by the project.
* Keep the expected directory structure unchanged so that the classification pipeline can locate the dataset correctly.
