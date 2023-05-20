from abc import ABC, abstractmethod

class Method_Builder(ABC):
    #input : str # filename or text

    # def __init__(self, input:str) -> None:
    #     super().__init__()
    #     self.input = input

    @abstractmethod
    def pre_processing_step(self):
        ...

    @abstractmethod
    def processing_step(self):
        ...

    @abstractmethod
    def post_processing_step(self):
        ...

    