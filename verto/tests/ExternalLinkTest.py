import markdown
import re
from unittest.mock import Mock
from verto.processors.ExternalLinkPattern import ExternalLinkPattern
from verto.tests.ProcessorTest import ProcessorTest


class ExternalLinkTest(ProcessorTest):
    '''Tests to check the 'external-link' pattern works as intended.
    This class is unique to other processors as it overrides
    default markdown behaviour in certain situations.
    '''

    def __init__(self, *args, **kwargs):
        '''Set processor name in class for asset file retrieval.'''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'external-link'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_ignore_http_schema(self):
        '''Tests that external links starting with http are matched.'''
        test_string = self.read_test_file(self.processor_name, 'http_schema.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'http_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_http_text(self):
        '''Tests that relative links are not matched.'''
        test_string = self.read_test_file(self.processor_name, 'http_text.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'http_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_https_schema(self):
        '''Tests that external links starting with https are matched.'''
        test_string = self.read_test_file(self.processor_name, 'https_schema.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'https_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_https_text(self):
        '''Tests that relative links are not matched.'''
        test_string = self.read_test_file(self.processor_name, 'https_text.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'https_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ftp_schema(self):
        '''Tests that external links starting with ftp are matched.'''
        test_string = self.read_test_file(self.processor_name, 'ftp_schema.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'ftp_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_ftp_text(self):
        '''Tests that relative links are not matched.'''
        test_string = self.read_test_file(self.processor_name, 'ftp_text.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'ftp_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ftps_schema(self):
        '''Tests that external links starting with ftps are matched.'''
        test_string = self.read_test_file(self.processor_name, 'ftps_schema.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'ftps_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_ftps_text(self):
        '''Tests that relative links are not matched.'''
        test_string = self.read_test_file(self.processor_name, 'ftps_text.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'ftps_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_mailto_schema(self):
        '''Tests that external links starting with mailto are matched.'''
        test_string = self.read_test_file(self.processor_name, 'mailto_schema.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'mailto_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_mailto_text(self):
        '''Tests that relative links are not matched.'''
        test_string = self.read_test_file(self.processor_name, 'mailto_text.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'mailto_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_news_schema(self):
        '''Tests that external links starting with news are matched.'''
        test_string = self.read_test_file(self.processor_name, 'news_schema.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'news_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_news_text(self):
        '''Tests that relative links are not matched.'''
        test_string = self.read_test_file(self.processor_name, 'news_text.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'news_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_www_text(self):
        '''Tests that links similar to a match are not matched.'''
        test_string = self.read_test_file(self.processor_name, 'www_text.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'www_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_long_path(self):
        '''Tests that long paths with less than 31 characters work.'''
        test_string = self.read_test_file(self.processor_name, 'long_path.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'long_path_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_query_parameter(self):
        '''Tests that paths with query parameter work.'''
        test_string = self.read_test_file(self.processor_name, 'query_parameter.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'query_parameter_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_query_parameters(self):
        '''Tests that paths with multiple query parameters work.'''
        test_string = self.read_test_file(self.processor_name, 'multiple_query_parameters.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_query_parameters_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_trailing_question_mark(self):
        '''Tests paths with trailing question marks.'''
        test_string = self.read_test_file(self.processor_name, 'trailing_question_mark.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'trailing_question_mark_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_links(self):
        '''Tests that multiple links are processed.'''
        test_string = self.read_test_file(self.processor_name, 'multiple_links.md')

        processor = ExternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_links_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)
