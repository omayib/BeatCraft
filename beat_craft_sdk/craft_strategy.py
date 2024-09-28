from abc import abstractmethod


class CraftStrategy():
    @abstractmethod
    def generate(self):
        pass