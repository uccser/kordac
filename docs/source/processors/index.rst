Using Processors
#######################################

- Tags should always be separated with newlines before and after each tag.
- If a processor requires both a start and end tag (for example: panels) and one tag is missing then a ``TagNotMatchedError`` Exception will be thrown.
- You can escape a double quote in a parameter with a slash ``\"`` though this also means you can never end a parameter with a ``\``.

Available Processors
#######################################

The following pages covers how to use the available processors within Markdown text:

.. toctree::
    :maxdepth: 1

    blockquote
    boxed-text
    button-link
    comment
    conditional
    external-link
    iframe
    glossary-link
    heading
    image
    image-inline
    interactive
    panel
    relative-link
    remove-title
    save-title
    scratch
    scratch-inline
    table-of-contents
    video

Implicit Processors
#######################################

The following pages cover processors that do not require explicit use when authoring Markdown:

.. toctree::
    :maxdepth: 1

    jinja
    orderedlist
    remove
    scratch-compatibility
    style
    unorderedlist
