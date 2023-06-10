from .method_builder import MethodBuilder
from .fp_method import FpMethodResult

class MethodConfigurator():
    builder: MethodBuilder

    def __init__(self, builder: MethodBuilder) -> None:
        super().__init__()
        self.builder = builder
        if self.builder is None:
            raise AttributeError("Builder cannot be empty")

    def change_builder(self, new_builder: MethodBuilder):
        self.builder = new_builder

    def make_method(self)-> FpMethodResult:
        self.builder.pre_processing_step()
        self.builder.processing_step()
        return self.builder.post_processing_step()
