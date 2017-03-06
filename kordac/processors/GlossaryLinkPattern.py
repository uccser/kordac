from kordac.processors.utils import check_argument_requirements, parse_argument
from markdown.util import etree
import markdown.inlinepatterns
import re


class GlossaryLinkPattern(markdown.inlinepatterns.Pattern):
    """Return a glossary link element from the given match

    Matches:
        {glossary-link term="super-serious-term"}Super Serious Term{glossary-link end}
    Returns:
        <p>
         <a class="glossary-term" data-glossary-term="super-serious-term">
          Super Serious Term
         </a>
        </p>
    """

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ext = ext
        self.processor = 'glossary-link'
        self.pattern = self.ext.processor_info['glossary-link']['pattern']
        self.compiled_re = re.compile('^(.*?){}(.*)$'.format(self.pattern), re.DOTALL | re.UNICODE) # TODO raw string prefix
        self.template = self.ext.jinja_templates[self.processor]
        self.required_parameters = self.ext.processor_info[self.processor]['required_parameters']
        self.optional_parameters = self.ext.processor_info[self.processor]['optional_parameter_dependencies']
        self.ext_glossary_terms = ext.glossary_terms
        self.unique_slugify = ext.custom_slugify

    def handleMatch(self, match):

        text = match.group('text')
        arguments = match.group('args')
        check_argument_requirements(self.processor, arguments, self.required_parameters, self.optional_parameters)

        term = parse_argument('term', arguments)
        reference = parse_argument('reference-text', arguments)

        context = dict()
        context['term'] = term
        context['text'] = text

        if reference is not None:
            identifier = self.unique_slugify('glossary-' + term)
            self.ext_glossary_terms[term].append((reference, identifier))
            context['id'] = identifier

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)

        return node
