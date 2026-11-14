import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unittest


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = set()
        self.title_parts = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)


class IndexHtmlTests(unittest.TestCase):
    def setUpClass():
        pass

    @classmethod
    def load_document(cls, file_path):
        cls.html = file_path.read_text(encoding="utf-8")
        cls.parser = DocumentParser()
        cls.parser.feed(cls.html)

    def test_has_html5_doctype(self):
        self.assertRegex(self.html, re.compile(r"<!doctype\s+html\s*>", re.IGNORECASE))

    def test_has_required_elements(self):
        self.assertTrue({"html", "head", "body", "title"} <= self.parser.tags)

    def test_title_is_not_empty(self):
        self.assertTrue("".join(self.parser.title_parts).strip())


def main():
    parser = argparse.ArgumentParser(description="Проверка HTML-файла index.")
    parser.add_argument("--file", required=True, type=Path, help="Путь к HTML-файлу")
    args = parser.parse_args()

    file_path = args.file
    if not file_path.is_file():
        parser.error(f"Файл не найден: {file_path}")

    IndexHtmlTests.load_document(file_path)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IndexHtmlTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
