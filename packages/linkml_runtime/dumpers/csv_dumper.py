from linkml_runtime.dumpers.delimited_file_dumper import DelimitedFileDumper


class CSVDumper(DelimitedFileDumper):

    @property
    def delimiter(self):
        return ","
