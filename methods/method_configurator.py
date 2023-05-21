from method_builder import Method_Builder

class Method_Configurator():
    builder : Method_Builder

    def __init__(self, builder : Method_Builder) -> None:
        super().__init__()
        self.builder = builder
        if self.builder is None:
            raise AttributeError("Builder cannot be empty")
        
    def change_builder(self, new_builder: Method_Builder):
        self.builder = new_builder    

    def make_method(self):
        self.builder.pre_processing_step()
        self.builder.processing_step()
        return self.builder.post_processing_step()