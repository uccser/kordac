import sys
import unittest
import optparse
from verto.tests.ConfigurationTest import ConfigurationTest
from verto.tests.SmokeTests import SmokeFileTest, SmokeDocsTest
from verto.tests.BlockquoteTest import BlockquoteTest
from verto.tests.BoxedTextTest import BoxedTextTest
from verto.tests.ButtonLinkTest import ButtonLinkTest
from verto.tests.CommentTest import CommentTest
from verto.tests.ConditionalTest import ConditionalTest
from verto.tests.FrameTest import FrameTest
from verto.tests.GlossaryLinkTest import GlossaryLinkTest
from verto.tests.HeadingTest import HeadingTest
from verto.tests.ImageInlineTest import ImageInlineTest
from verto.tests.ImageTagTest import ImageTagTest
from verto.tests.ImageContainerTest import ImageContainerTest
from verto.tests.JinjaTest import JinjaTest
from verto.tests.InteractiveTagTest import InteractiveTagTest
from verto.tests.InteractiveContainerTest import InteractiveContainerTest
from verto.tests.PanelTest import PanelTest
from verto.tests.RelativeLinkTest import RelativeLinkTest
from verto.tests.ExternalLinkTest import ExternalLinkTest
from verto.tests.RemoveTest import RemoveTest
from verto.tests.RemoveTitleTest import RemoveTitleTest
from verto.tests.SaveTitleTest import SaveTitleTest
from verto.tests.ScratchTest import ScratchTest
from verto.tests.ScratchInlineTest import ScratchInlineTest
from verto.tests.StyleTest import StyleTest
from verto.tests.TableOfContentsTest import TableOfContentsTest
from verto.tests.VideoTest import VideoTest
from verto.tests.HtmlParserTest import HtmlParserTest
from verto.tests.MarkdownOverrideTest import MarkdownOverrideTest


def parse_args():
    '''Parses the arguments for running the test suite, these are
    useful for developing when parts of verto are known to fail.
    '''
    opts = optparse.OptionParser(
        usage='Run the command `python -m verto.tests.start_tests` from the level above the verto directory.',
        description='Verifies that Verto is functional compared to the testing suite.')
    opts.add_option(
        '--travis',
        action='store_true',
        help='Enables skipping suites on failure. To be used by continuous integration system.',
        default=False
    )
    opts.add_option(
        '--no_smoke',
        action='store_true',
        help='Skips smoke tests, should be used for local development only.',
        default=False
    )
    opts.add_option(
        '--no_system',
        action='store_true', help='Skips system tests, should be used for local development only.',
        default=False
    )
    opts.add_option(
        '--no_unit',
        action='store_true',
        help='Skips unit tests, should be used for local development only.',
        default=False
    )
    options, arguments = opts.parse_args()

    return options, arguments


def smoke_suite():
    '''Builds the smoke tests.
    '''
    return unittest.TestSuite((
        unittest.makeSuite(SmokeDocsTest),
        unittest.makeSuite(SmokeFileTest),
    ))


def system_suite():
    '''Builds specific system tests.
    '''
    return unittest.TestSuite((
        unittest.makeSuite(ConfigurationTest)
    ))


def unit_suite():
    '''Builds unittests. (Not really unittests).
    '''
    return unittest.TestSuite((
        unittest.makeSuite(BlockquoteTest),
        unittest.makeSuite(BoxedTextTest),
        unittest.makeSuite(ButtonLinkTest),
        unittest.makeSuite(CommentTest),
        unittest.makeSuite(ConditionalTest),
        unittest.makeSuite(FrameTest),
        unittest.makeSuite(GlossaryLinkTest),
        unittest.makeSuite(HeadingTest),
        unittest.makeSuite(ImageInlineTest),
        unittest.makeSuite(ImageTagTest),
        unittest.makeSuite(ImageContainerTest),
        unittest.makeSuite(InteractiveTagTest),
        unittest.makeSuite(InteractiveContainerTest),
        unittest.makeSuite(JinjaTest),
        unittest.makeSuite(PanelTest),
        unittest.makeSuite(SaveTitleTest),
        unittest.makeSuite(ScratchTest),
        unittest.makeSuite(ScratchInlineTest),
        unittest.makeSuite(StyleTest),
        unittest.makeSuite(RelativeLinkTest),
        unittest.makeSuite(ExternalLinkTest),
        unittest.makeSuite(RemoveTest),
        unittest.makeSuite(RemoveTitleTest),
        unittest.makeSuite(TableOfContentsTest),
        unittest.makeSuite(VideoTest),

        unittest.makeSuite(HtmlParserTest),
        unittest.makeSuite(MarkdownOverrideTest),
    ))


if __name__ == '__main__':
    options, arguments = parse_args()

    runner = unittest.TextTestRunner()

    smoke_result = None
    if not options.no_smoke:
        print('Running Smoke Tests')
        smoke_result = runner.run(smoke_suite())
        print()

    if options.travis and smoke_result and not smoke_result.wasSuccessful():
        print('Skipping other test-suites.')
        sys.exit(1)

    system_result = None
    if not options.no_system:
        print('Running System Tests')
        system_result = runner.run(system_suite())
        print()

    unit_result = None
    if not options.no_unit:
        print('Running Unit Tests')
        unit_result = runner.run(unit_suite())
        print()

    if (smoke_result is not None and not smoke_result.wasSuccessful()) or (system_result is not None and not system_result.wasSuccessful()) or (unit_result is not None and not unit_result.wasSuccessful()):
        sys.exit(1)
