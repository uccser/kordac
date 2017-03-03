import unittest
import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.HeadingBlockProcessor import HeadingBlockProcessor
from kordac.tests.ProcessorTest import ProcessorTest
from kordac.utils.HeadingNode import HeadingNode

class HeadingTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'heading'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_example_blank(self):
        test_string = self.read_test_file(self.processor_name, 'example_blank.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_blank_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = self.kordac_extension.get_heading_tree()
        self.assertIsNone(tree)

    def test_single_heading(self):
        test_string = self.read_test_file(self.processor_name, 'example_single_heading.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_single_heading_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = self.kordac_extension.get_heading_tree()
        expected_tree = (
            HeadingNode(title='Heading One',
                                        title_slug='heading-one',
                                        level=1,
                                        children=()
            ),
        )
        self.assertTupleEqual(tree, expected_tree)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, True], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = self.kordac_extension.get_heading_tree()
        expected_tree = (HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1',
                                    level=1,
                                    children=(
                                        HeadingNode(
                                            title='This is an H2',
                                            title_slug='this-is-an-h2',
                                            level=2,
                                            children=(
                                                HeadingNode(
                                                    title='This is an H6',
                                                    title_slug='this-is-an-h6',
                                                    level=6,
                                                    children=()
                                                ),
                                            )
                                        ),
                                    )
                        ),
                    )
        self.assertTupleEqual(tree, expected_tree)


    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, True, True, True, True, True], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = kordac_extension.get_heading_tree()
        expected_tree = (HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1',
                                    level=1,
                                    children=(
                                        HeadingNode(
                                            title='This is an H2',
                                            title_slug='this-is-an-h2',
                                            level=2,
                                            children=(
                                                HeadingNode(
                                                    title='This is an H4',
                                                    title_slug='this-is-an-h4',
                                                    level=4,
                                                    children=()
                                                ),
                                            )
                                        ),
                                    )
                        ),
                        HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1-2',
                                    level=1,
                                    children=(
                                        HeadingNode(
                                            title='This is an H3',
                                            title_slug='this-is-an-h3',
                                            level=3,
                                            children=(
                                                HeadingNode(
                                                    title='This is an H6',
                                                    title_slug='this-is-an-h6',
                                                    level=6,
                                                    children=()
                                                ),
                                            )
                                        ),
                                    )
                        ),
                        HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1-3',
                                    level=1,
                                    children=()
                        ),
                    )

        self.assertTupleEqual(tree, expected_tree)

    def test_multiple_roots_zero_level(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_roots_zero_level.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, True, True, True, True, True], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_roots_zero_level_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = kordac_extension.get_heading_tree()
        expected_tree = (HeadingNode(title='This is an H4',
                                    title_slug='this-is-an-h4',
                                    level=4,
                                    children=()
                        ),
                        HeadingNode(title='This is an H2',
                                    title_slug='this-is-an-h2',
                                    level=2,
                                    children=(
                                        HeadingNode(
                                            title='This is an H3',
                                            title_slug='this-is-an-h3',
                                            level=3,
                                            children=()
                                        ),
                                    )
                        ),
                        HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1',
                                    level=1,
                                    children=(
                                        HeadingNode(
                                            title='This is an H3',
                                            title_slug='this-is-an-h3-2',
                                            level=3,
                                            children=()
                                        ),
                                        HeadingNode(title='This is an H2',
                                                    title_slug='this-is-an-h2-2',
                                                    level=2,
                                                    children=(
                                                        HeadingNode(title='This is an H4',
                                                                    title_slug='this-is-an-h4-2',
                                                                    level=4,
                                                                    children=()
                                                        ),
                                                    )
                                        ),
                                    )
                        ),
                    )
        self.assertTupleEqual(tree, expected_tree)
