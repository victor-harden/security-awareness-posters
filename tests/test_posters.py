import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import poster_gen


class PosterTests(unittest.TestCase):
    def test_every_topic_builds_valid_svg(self):
        for topic in poster_gen.TOPICS:
            svg = poster_gen.build_svg(topic)
            root = ET.fromstring(svg)
            self.assertTrue(root.tag.endswith("svg"))

    def test_headline_escaped(self):
        svg = poster_gen.build_svg("phishing")
        self.assertIn("Check before you click", svg)

    def test_unknown_topic(self):
        with self.assertRaises(KeyError):
            poster_gen.build_svg("nope")

    def test_theme_colors(self):
        light = poster_gen.build_svg("mfa", "light")
        dark = poster_gen.build_svg("mfa", "dark")
        self.assertIn("#ffffff", light)
        self.assertIn("#0f172a", dark)

    def test_cli_single(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "poster.svg"
            code = poster_gen.main(["--topic", "backups", "--out", str(out)])
            self.assertEqual(code, 0)
            ET.fromstring(out.read_text())

    def test_cli_all(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "posters"
            code = poster_gen.main(["--all", "--out-dir", str(out_dir)])
            self.assertEqual(code, 0)
            self.assertEqual(len(list(out_dir.glob("*.svg"))), len(poster_gen.TOPICS))

    def test_cli_list(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(poster_gen.main(["--list"]), 0)
        self.assertIn("mfa", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
