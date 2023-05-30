from linkml_runtime.loaders.delimited_file_loader import DelimitedFileLoader

class TSVLoader(DelimitedFileLoader):
    
    @property
    def delimiter(self):
        return "\t"
