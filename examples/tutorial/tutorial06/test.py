from personinfo import Person, PersonStatus

person = Person(id='P1', full_name='Julius Caesar', status="DEAD")
print(f'STATUS={person.status}')
print(f'MEANING={person.status.meaning}')
