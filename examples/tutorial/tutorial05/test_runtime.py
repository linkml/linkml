from linkml_runtime.dumpers import json_dumper

from personinfo import Person

p1 = Person(id='ORCID:9876', full_name='Lex Luthor', aliases=["Bad Guy"])

print(json_dumper.dumps(p1))
