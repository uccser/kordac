External Link
#######################################

**Processor name:** ``external-link``

This processor will find any external links (links that start with ``http:``, ``https:``, ``mailto:``, etc.), and will create a HTML link with the ``target`` attribute set to ``"_blank"``.
This allows external links in Markdown to be opened in a new tab.

The default HTML for external links is:

.. literalinclude:: ../../../verto/html-templates/external-link.html
   :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../verto/tests/assets/external-link/https_schema.md
   :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/external-link/https_schema_expected.html
   :language: html
