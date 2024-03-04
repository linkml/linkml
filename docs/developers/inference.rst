.. _inference:

Inferring Missing Values
========================

Expressions
-----------

LinkML supports the use of expressions to define how slot values can
be derived from other slot values. The slot
`equals_expression <https://w3id.org/linkml/equals_expression>`_
specifies how to calculate the value of a slot, as demonstrated here:

.. code-block:: yaml

  class:
    Person:
      attributes:
        age_in_years:
          range: decimal
          minimum_value: 0
          maximum_value: 999
          equals_expression: "{age_in_months} / 12"
        age_in_months:
          range: decimal
          equals_expression: "{age_in_years} * 12"
        is_juvenile:
          range: boolean
          equals_expression: "{age_in_years} < 18"

The following code will populate missing values:          

.. code-block:: python

    from linkml_runtime.utils.inference_utils import infer_all_slot_values
    from .personinfo infer Person

    p = Person(age_in_years=30)
    infer_all_slot_values(p, schemaview=sv)
    assert p.age_in_months == 360
    assert not p.juvenile

You can also use the ``linkml-convert`` script with the ``--infer`` flag

String serialization
--------------------

For simple string based expressions,
`string_serialization <https://w3id.org/linkml/string_serialization>`_
can be used:
    
.. code-block:: yaml
  
  Address:
    attributes:
      street:
      city:
      full_address:
        string_serialization: |-
          {street}
          {city}

The following code will populate the full address:

.. code-block:: python

    from linkml_runtime.utils.inference_utils import infer_all_slot_values
    from .personinfo infer Address

    a = Address(street="1 Oak street", city="Oaktown")
    infer_all_slot_values(p, schemaview=sv)
    print(a.full_address)

    
Configuration
-------------

.. currentmodule:: linkml_runtime.utils.inference_utils

.. autoclass:: Config
               
.. autoclass:: Policy
                   

Code
----
          
.. currentmodule:: linkml_runtime.utils.inference_utils

.. autofunction:: infer_slot_value
                  
.. autofunction:: infer_all_slot_values
                   

