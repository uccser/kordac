Panel
#######################################

**Processor name:** ``panel``

You can include an panel using the following text tag:

.. literalinclude:: ../../../tests/assets/panel/doc_example_basic_usage.md
    :language: none

Required Tag Parameters
***************************************

- ``type`` - The type of panel to create.

    - The type is saved as a CCS class (with ``panel-`` prefix) in the panel (this allows colouring of all the same types of panels).

- ``title`` - Text to display as the panel's title.

Optional Tag Parameters
***************************************

- ``subtitle`` - Text to display as the panel's subtitle after the title.
- ``expanded`` - A value to state the panel's state:

    - If given as 'true', the panel contains the CSS class ``panel-expanded`` to state it should be expanded on load.
    - If set to 'always', the panel contains the CSS class ``panel-expanded-always`` to state it should be expanded at load and cannot be closed.
    - When ``expanded`` is not given or not a value above, the panel contains no extra CSS classes and be closed on load.

The default HTML for a panel is:

.. literalinclude:: ../../../kordac/html-templates/panel.html
   :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../tests/assets/panel/doc_example_basic_usage.md
   :language: none

The resulting HTML would be:

.. literalinclude:: ../../../tests/assets/panel/doc_example_basic_usage_expected.html
   :language: html

Overriding HTML for Panels
***************************************

When overriding the HTML for images, the following Jinja2 placeholders are available:

- ``{{ type }}`` - The type of panel to be created.
- ``{{ expanded }}`` - Text either set to 'true' or 'always' to state if the panel should be expanded. See parameter description above.
- ``{{ title }}`` - The provided title text.
- ``{{ subtitle }}`` - The provided subtitle text.
- ``{{ content }}`` - The text enclosed by the panel tags.

**Example**

For example, providing the following HTML:

.. literalinclude:: ../../../tests/assets/panel/doc_example_override_html_template.html
  :language: css+jinja

with the following tag:

.. literalinclude:: ../../../tests/assets/panel/doc_example_override_html.md
  :language: none

would result in:

.. literalinclude:: ../../../tests/assets/panel/doc_example_override_html_expected.html
  :language: html