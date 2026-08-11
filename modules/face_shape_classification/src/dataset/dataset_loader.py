from pathlib import Path


class DatasetLoader:
    """
    Load face shape image dataset.

    Expected structure:

    dataset/
        oval/
            img1.jpg
        round/
            img2.jpg
        square/
            img3.jpg

    Returns:

    [
        (image_path, label)
    ]
    """

    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }


    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)


        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset path not found: {self.dataset_path}"
            )


    def load_images(self):
        """
        Scan dataset folders and collect images.

        Returns:
            list[tuple]
        """

        dataset = []


        # loop through class folders
        for class_folder in sorted(self.dataset_path.iterdir()):


            # ignore files
            if not class_folder.is_dir():
                continue


            label = class_folder.name


            # loop images inside class folder
            for image_file in sorted(class_folder.iterdir()):


                if image_file.suffix.lower() not in self.IMAGE_EXTENSIONS:
                    continue


                dataset.append(
                    (
                        image_file,
                        label
                    )
                )


        return dataset