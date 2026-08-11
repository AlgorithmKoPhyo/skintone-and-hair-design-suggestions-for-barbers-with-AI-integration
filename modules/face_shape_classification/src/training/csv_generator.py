import csv
from pathlib import Path


class CSVGenerator:
    """
    Generate CSV feature dataset
    from extracted face features.
    """


    def __init__(self, output_path):

        self.output_path = Path(
            output_path
        )


        # create folder if missing

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )



    def save(self, dataset):

        """
        Save feature data.

        Args:
            dataset:

            [
                {
                  feature1:value,
                  feature2:value,
                  label:"Oval"
                }
            ]

        """


        if not dataset:

            raise ValueError(
                "No data to save"
            )


        fieldnames = list(
            dataset[0].keys()
        )


        with open(
            self.output_path,
            "w",
            newline=""
        ) as file:


            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )


            writer.writeheader()


            writer.writerows(
                dataset
            )


        print(
            f"CSV saved: {self.output_path}"
        )