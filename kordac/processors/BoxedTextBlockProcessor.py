from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import parse_argument, etree

import kordac.processors.errors.TagNotMatchedError as TagNotMatchedError
import re

class BoxedTextBlockProcessor(BlockProcessor):
    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = 'boxed-text'
        self.p_start = re.compile(ext.tag_patterns[self.tag]['pattern_start'])
        self.p_end = re.compile(ext.tag_patterns[self.tag]['pattern_end'])
        self.template = ext.jinja_templates[self.tag]

    def test(self, parent, block):
        return self.p_start.search(block) is not None or self.p_end.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)

        start_tag = self.p_start.search(block)
        end_tag = self.p_end.search(block)

        if start_tag is None and end_tag is not None:
            raise TagNotMatchedError(self.tag, block, 'end tag found before start tag')

        blocks.insert(0, block[start_tag.end():])

        content = ''
        the_rest = None

        while len(blocks) > 0:
            block = blocks.pop(0)
            end_tag = self.p_end.search(block)
            if end_tag:
                content += block[:end_tag.start()] + '\n'
                the_rest = block[end_tag.end():]
                break
            content += block  + '\n'

        if the_rest:
            blocks.insert(0, the_rest)
        if end_tag is None:
            raise TagNotMatchedError(self.tag, block, 'no end tag found to close start tag')

        content_tree = etree.Element('content')
        self.parser.parseChunk(content_tree, content)

        content = ''
        for child in content_tree:
            content += etree.tostring(child, encoding="unicode", method="html") + '\n'

        context = dict()
        context['indented'] = parse_argument('indented', start_tag.group('args'), False)
        context['text'] = content

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
