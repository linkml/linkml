from linkml_runtime.loaders.delimited_file_loader import DelimitedFileLoader

class CSVLoader(DelimitedFileLoader):
    
    @property
    def delimiter(self):
        return ","
