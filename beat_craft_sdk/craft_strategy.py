from abc import abstractmethod


class CraftStrategy():
    @abstractmethod
    def generate(self,output_dir,file_name, scale):
        pass

    @abstractmethod
    def evaluate(self,output_dir,file_name):
        pass