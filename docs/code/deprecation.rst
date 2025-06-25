.. index:: Deprecation; Log

Deprecation Log
---------------------

See `Deprecation Guide <../developers/deprecation.md>`_

.. plot:: plots/deprecation_plot.py

.. jinja:: deprecations

    {% for dep in deprecations %}
    {{ dep.name }}
    ==============

    {% if dep.removed %}
    .. admonition:: Removed
    {% else %}
    .. admonition:: Deprecated
        :class: warning
    {% endif %}

        .. deprecated:: {{ dep.deprecated_in }}

        {% if dep.removed_in is not none %}
        *Removed in {{ dep.removed_in }}*
        {% endif %}

        {% if dep.issue is not none %}
        See also: `#{{ dep.issue }} <https://github.com/linkml/linkml/issues/{{ dep.issue }}>`_
        {% endif %}

    {{ dep.message }}

    {% if dep.recommendation %}
    **Recommendation:** {{ dep.recommendation }}
    {% endif %}

    {% endfor %}
