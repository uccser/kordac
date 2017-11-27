import markdown
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.ImageTagBlockProcessor import ImageTagBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.tests.ProcessorTest import ProcessorTest


class ImageTagTest(ProcessorTest):
    '''The image tag processor is a simple tag with a multitude of
    different possible arguments that modify output slightly.
    Internally linked file features need to be considered
    when testing images, such that required files are modified
    and need to be checked to see if updated correctly.
    '''

    def __init__(self, *args, **kwargs):
        '''Set processor name and tag argument in class for file names.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'image-tag'
        self.tag_argument = 'image'
        self.ext = Mock()
        self.ext.jinja_templates = {
            'image': ProcessorTest.loadJinjaTemplate(self, 'image'),
            'relative-file-link': ProcessorTest.loadJinjaTemplate(self, 'relative-file-link')
        }
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.required_files = defaultdict(set)

    def test_caption(self):  # should not be matched
        '''Tests to ensure that an image with a caption is ignored.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, False, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'caption_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_no_caption(self):
        '''Tests to ensure that an image with no caption is rendered correctly and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'no_caption.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_caption_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'pixel-diamond.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_caption_false(self):
        '''Tests caption argument is ignored when set to false and that expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'caption_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'cats.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_source_hover_no_caption(self):
        '''Tests that multiple arguments are rendered correctly when no caption argument is included and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'source_hover_no_caption.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'source_hover_no_caption_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'finite-state-automata-no-trap-example.png',
            'finite-state-automata-trap-added-example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_alt_hover_caption_false(self):
        '''Tests that multiple arguments are rendered correctly when caption argument is false and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'alt_hover_caption_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'alt_hover_caption_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'finite-state-automata-no-trap-example.png',
            'finite-state-automata-trap-added-example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_multiple_images_captions_false(self):
        '''Tests to ensure that multiple internally reference images produce the desired output and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_images_captions_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, True, False, True, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_images_captions_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'the-first-image.png',
            'Lipsum.png',
            'pixel-diamond.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_external_image(self):
        '''Tests that external images are processed and that the expected images are unchanged.
        '''
        test_string = self.read_test_file(self.processor_name, 'external_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'external_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_hover_text(self):
        '''Tests that argument for hover-text produces expected output and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_hover_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_hover_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_alt(self):
        '''Tests that argument for alt produces expected output and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_alt.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_alt_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_source(self):
        '''Tests that argument for source produces expected output and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_source.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_source_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_left(self):
        '''Tests that argument for align produces expected output when set to left and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_left.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_left_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_right(self):
        '''Tests that argument for align produces expected output when set to right and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_right.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_right_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_center(self):
        '''Tests that argument for align produces expected output when set to center and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_center.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_center_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_caption_link_error(self):
        '''Tests that ArgumentMissingError is raised when caption-link argument is give but a caption is not provided.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_link_error.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_align_undefined_error(self):
        '''Tests that ArgumentValueError is raised when undefined align value is given.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_undefined_error.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_image_in_numbered_list(self):
        '''Test image rendered correctly in numbered list.
        '''
        test_string = self.read_test_file(self.processor_name, 'image_in_numbered_list.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, True, False], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'image_in_numbered_list_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    # #~
    # # Doc Tests
    # #~

    def test_doc_example_basic(self):
        '''Basic example of common usage.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_doc_example_override_html(self):
        '''Basic example showing how to override the html-template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_doc_example_2_override_html(self):
        '''Basic example showing how to override the html-template for relative files in a specific file only.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_2_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_2_override_html_template.html', strip=True)
        link_template = self.read_test_file(self.processor_name, 'doc_example_2_override_link_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template, 'relative-file-link': link_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_2_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)
