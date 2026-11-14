import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unittest


INDEX = Path(__file__).resolve().parent.parent / "my_art_web" / "index.html"


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = set()
        self.in_title = False
        self.title_parts = []

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)


class IndexHtmlTests(unittest.TestCase):
    index = INDEX

    @classmethod
    def setUpClass(cls):
        if not cls.index.is_file():
            raise FileNotFoundError(f"Файл не найден: {cls.index}")
        cls.html = cls.index.read_text(encoding="utf-8")
        cls.parser = DocumentParser()
        cls.parser.feed(cls.html)

    def test_has_html5_doctype(self):
        self.assertRegex(self.html, re.compile(r"<!doctype\s+html\s*>", re.IGNORECASE))

    def test_has_required_elements(self):
        self.assertTrue({"html", "head", "body", "title"} <= self.parser.tags)

    def test_title_is_not_empty(self):
        self.assertTrue("".join(self.parser.title_parts).strip())


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--file", required=True, type=Path)
    args, _ = argument_parser.parse_known_args()
    IndexHtmlTests.index = args.file
    unittest.main(argv=[sys.argv[0]], verbosity=2)
