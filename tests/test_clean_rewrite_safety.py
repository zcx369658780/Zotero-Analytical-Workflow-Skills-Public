from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


FETCH = load_module(
    "clean_rewrite_safety_fetch",
    "skills/zotero-data-fetcher/scripts/zotero_fetch.py",
)


class _Response:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self) -> bytes:
        return json.dumps({"synthetic": True}).encode("utf-8")


class CleanRewriteSafetyTests(unittest.TestCase):
    def test_template_headings_are_not_embedded_in_product_python(self):
        template = (ROOT / "templates" / "论文精读模板.md").read_text(encoding="utf-8")
        headings = [
            line.removeprefix("## ").strip()
            for line in template.splitlines()
            if line.startswith("## ")
        ]
        self.assertEqual(len(headings), 8)

        product_paths = (
            "skills/zotero-collection-manager/scripts/batch_import_collection.py",
            "skills/zotero-collection-manager/scripts/deep_read_collection.py",
            "skills/zotero-collection-manager/scripts/template_renderer.py",
        )
        for relative_path in product_paths:
            source = (ROOT / relative_path).read_text(encoding="utf-8")
            for heading in headings:
                with self.subTest(path=relative_path, heading=heading):
                    self.assertNotIn(heading, source)

    def test_http_json_uses_timeout_and_identifying_headers(self):
        captured = {}

        def fake_urlopen(request, timeout):
            captured["headers"] = {key.casefold(): value for key, value in request.header_items()}
            captured["timeout"] = timeout
            return _Response()

        with mock.patch.object(FETCH.urllib.request, "urlopen", side_effect=fake_urlopen):
            result = FETCH.http_json("https://example.invalid/synthetic")

        self.assertEqual(result, {"synthetic": True})
        self.assertEqual(captured["timeout"], 8.0)
        self.assertTrue(captured["headers"].get("user-agent"))
        self.assertEqual(captured["headers"].get("accept"), "application/json")


if __name__ == "__main__":
    unittest.main()
