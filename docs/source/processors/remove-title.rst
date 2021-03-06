Remove Title
#######################################

**Processor name:** ``remove-title``

This preprocessor runs before any conversion of Markdown and searches for a heading in the first line of provided Markdown text.
If a heading is found on the first line, it deletes that line of text.
This preprocessor runs after the ``save-title`` preprocessor if present.

This preprocessor is **not** turned on by default.
To use ``remove-title``, it needs to be explicity provided in the ``processors`` parameter when creating the Verto converter, or given in the ``update_processors`` method (see example below).

**Example**

With the following text saved in ``example_string``:

.. literalinclude:: ../../../verto/tests/assets/remove-title/doc_example_basic_usage.md
    :language: none

.. code-block:: python

    import verto
    converter = verto.Verto()
    tags = verto.tag_defaults()
    tags.add('remove-title')
    converter.update_tags(tags)
    result = converter.convert(example_string)

The ``html_string`` value in ``result`` would be:

.. literalinclude:: ../../../verto/tests/assets/remove-title/doc_example_basic_usage_expected.html
    :language: none
