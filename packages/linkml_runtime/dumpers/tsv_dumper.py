from linkml_runtime.dumpers.delimited_file_dumper import DelimitedFileDumper


class TSVDumper(DelimitedFileDumper):

    @property
    def delimiter(self):
        return "\t"
