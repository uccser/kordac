import markdown
from verto.VertoExtension import VertoExtension

DEFAULT_PROCESSORS = frozenset({
    'blockquote',
    'boxed-text',
    'button-link',
    'comment',
    'conditional',
    'external-link',
    'glossary-link',
    'style',
    'heading',
    'iframe',
    'image-container',
    'image-tag',
    'image-inline',
    'interactive-tag',
    'interactive-container',
    'panel',
    'relative-link',
    'save-title',
    'scratch',
    'scratch-inline',
    'table-of-contents',
    'video'
})


class Verto(object):
    '''A converter object for converting markdown with complex elements
    to HTML.
    '''

    def __init__(self, processors=DEFAULT_PROCESSORS, html_templates={}, extensions=[], settings={}):
        '''Creates a Verto object.

        Args:
            processors: A set of processor names given as strings for which
                their processors are enabled. If given, all other
                processors are skipped.
            html_templates: A dictionary of HTML templates to override
                existing HTML templates for processors. Dictionary contains
                processor names given as a string as keys mapping HTML strings
                as values.
                eg: {'image': '<img src={{ source }}>'}
            extensions: A list of extra extensions to run on the
                markdown package.
            settings: A dictionary of settings to override default settings.
        '''
        self.processors = set(processors)
        self.html_templates = dict(html_templates)
        self.extensions = list(extensions)
        self.settings = settings
        self.create_converter()

    def create_converter(self):
        '''Create the Verto extension and converter for future use.'''
        self.verto_extension = VertoExtension(
            processors=self.processors,
            html_templates=self.html_templates,
            extensions=self.extensions,
            settings=self.settings,
        )
        all_extensions = self.extensions + [self.verto_extension]
        self.converter = markdown.Markdown(extensions=all_extensions)

    def convert(self, text):
        '''Return a VertoResult object after converting
        the given markdown string.

        Args:
            text: A string of Markdown text to be converted.

        Returns:
            A VertoResult object.
        '''
        self.verto_extension.clear_document_data()
        html_string = self.converter.convert(text)
        result = VertoResult(
            html_string=html_string,
            title=self.verto_extension.title,
            required_files=self.verto_extension.required_files,
            heading_tree=self.verto_extension.get_heading_tree(),
            required_glossary_terms=self.verto_extension.glossary_terms
        )
        return result

    def clear_saved_data(self):
        '''Clears data that is saved between documents. This should be
        called between conversions on unrelated documents.
        '''
        self.verto_extension.clear_saved_data()

    def update_templates(self, html_templates):
        '''Update the template dictionary with the given dictionary
        of templates, while leaving all other HTML templates (including
        any custom set templates) untouched. The updated dictionary
        will be used for converting from this point onwards.

        Args:
            html_templates: A dictionary of HTML templates to override
                existing HTML templates for processors. Dictionary
                contains processor names given as a string as keys
                mapping HTML strings as values.
                eg: {'image': '<img src={{ source }}>'}
        '''
        self.html_templates.update(html_templates)
        self.create_converter()

    def clear_templates(self):
        '''Set the template dictionary to it's original values.
        '''
        self.html_templates = {}
        self.create_converter()

    @staticmethod
    def processor_defaults():
        '''Returns a copy of the default processor set.

        Returns:
            A set of default processor names as strings.
        '''
        return set(DEFAULT_PROCESSORS)

    def update_processors(self, processors=DEFAULT_PROCESSORS):
        '''Update the processors used for conversion with the given
        set. The updated set will be used for converting from this
        point onwards. If parameter is empty, default processors will
        be used.

        Args:
            processors: A set of processor names given as strings for
                which their processors are enabled. If given, all other
                processors are skipped.
        '''
        self.processors = set(processors)
        self.create_converter()


class VertoResult(object):
    '''Object created by Verto containing the result data
    after a conversion by run.
    '''

    def __init__(self, html_string, title, required_files, heading_tree, required_glossary_terms):
        '''Create a VertoResult object.

        Args:
            html_string: A string of HTML text.
            title: The first heading encountered when converting.
            required_files: Dictionary of required file types to sets
                of paths.
            heading_tree: A tuple of HeadingNodes which represent the
                heading structure of the document.
            required_glossary_terms: A dictionary of glossary terms to
                a list of tuples containing reference text and slugs.
        '''
        self.html_string = html_string
        self.title = title
        self.required_files = required_files
        self.heading_tree = heading_tree
        self.required_glossary_terms = required_glossary_terms
