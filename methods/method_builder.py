from abc import ABC, abstractmethod

class Method_Builder(ABC):

    @abstractmethod
    def pre_processing_step(self):
        ...

    @abstractmethod
    def processing_step(self):
        ...

    @abstractmethod
    def post_processing_step(self):
        ...

    