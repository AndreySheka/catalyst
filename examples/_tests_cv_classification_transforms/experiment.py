from collections import OrderedDict

import torchvision

from catalyst.dl.experiment import ConfigExperiment


class MNIST(torchvision.datasets.MNIST):
    """
    `MNIST <http://yann.lecun.com/exdb/mnist/>`_ Dataset.
    """

    def __getitem__(self, index: int):
        """
        Fetches a sample for a given index from MNIST dataset.

        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class
        """
        image, target = self.data[index], self.targets[index]

        if self.transform is not None:
            image = self.transform({"image": image})["image"]

        return image, target


class Experiment(ConfigExperiment):
    """
    ``ConfigExperiment`` on MNIST dataset
    """

    def get_datasets(self, stage: str, **kwargs):
        """
        Provides train/validation subsets from MNIST dataset
        """
        datasets = OrderedDict()
        for mode in ("train", "valid"):
            datasets[mode] = MNIST(
                "./data",
                train=False,
                download=True,
                transform=self.get_transforms(stage=stage, dataset=mode),
            )

        return datasets
