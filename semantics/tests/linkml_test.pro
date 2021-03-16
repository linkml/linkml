:- include('biolink.pro').

expected(subclass_of(gene, named_thing)).
not_expected(subclass_of(named_thing, gene)).
%not_expected(incoherent).
    
