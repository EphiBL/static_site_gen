import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_basic(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        expected = "Hello"
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()