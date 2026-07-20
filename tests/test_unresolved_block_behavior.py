from __future__ import annotations

import ast
import importlib.util
import inspect
from datetime import datetime
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
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


BATCH = load_module(
    "behavior_contract_batch_import",
    "skills/zotero-collection-manager/scripts/batch_import_collection.py",
)
DEEP = load_module(
    "behavior_contract_deep_read",
    "skills/zotero-collection-manager/scripts/deep_read_collection.py",
)
FETCH = load_module(
    "behavior_contract_zotero_fetch",
    "skills/zotero-data-fetcher/scripts/zotero_fetch.py",
)


class FrozenDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 7, 21, 9, 30, 45, tzinfo=tz)


def fictional_payload(*, with_fulltext: bool = False) -> dict:
    attachments = []
    if with_fulltext:
        attachments.append(
            {
                "key": "PDF2002",
                "contentType": "application/pdf",
                "path": "<fictional-pdf-path>",
                "fulltext_cache": (
                    "Introduction. Northwind is a fictional region used for this study. "
                    "Method. The model compares housing supply and employment. "
                    "Data. The fictional sample contains constructed regional records. "
                    "Results. Flexible supply improves employment adjustment in the model. "
                    "Conclusion. The fictional exercise illustrates the stated mechanism. "
                )
                * 18,
            }
        )
    return {
        "item": {
            "key": "FIC2002" if with_fulltext else "FIC1001",
            "itemType": "journalArticle",
            "data": {
                "title": (
                    "Housing Constraints in Northwind"
                    if with_fulltext
                    else "Migration &amp; Work in Fictional Harbor"
                ),
                "date": "2025",
                "publicationTitle": "Journal of Fictional Regions",
                "creators": [
                    {"firstName": "Avery", "lastName": "Example", "creatorType": "author"}
                ],
            },
        },
        "attachments": attachments,
        "notes": [],
        "annotations": [],
    }


def assert_ordered(testcase: unittest.TestCase, text: str, fragments: list[str]) -> None:
    positions = [text.index(fragment) for fragment in fragments]
    testcase.assertEqual(positions, sorted(positions))


def isolated_renderer_exit_code(script_name: str, function_name: str, template_text: str | None) -> int:
    with tempfile.TemporaryDirectory() as temp_dir:
        isolated_root = Path(temp_dir)
        shutil.copytree(ROOT / "skills", isolated_root / "skills")
        if template_text is not None:
            template_dir = isolated_root / "templates"
            template_dir.mkdir()
            (template_dir / "论文精读模板.md").write_text(template_text, encoding="utf-8")

        script = (
            isolated_root
            / "skills"
            / "zotero-collection-manager"
            / "scripts"
            / script_name
        )
        invocation = f"""
import importlib.util
import sys
spec = importlib.util.spec_from_file_location("isolated_renderer", {str(script)!r})
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
payload = {{
    "item": {{"key": "FIC3003", "data": {{"title": "Synthetic Template Case"}}}},
    "attachments": [{{
        "key": "PDF3003",
        "contentType": "application/pdf",
        "fulltext_cache": "Introduction. Synthetic evidence. Conclusion. Synthetic result. " * 80,
    }}],
    "notes": [],
    "annotations": [],
}}
getattr(module, {function_name!r})(payload, "Synthetic Collection")
"""
        completed = subprocess.run(
            [sys.executable, "-c", invocation],
            cwd=isolated_root,
            capture_output=True,
            text=True,
            check=False,
        )
        return completed.returncode


class InferHelperContractTests(unittest.TestCase):
    def test_public_signatures(self):
        self.assertEqual(str(inspect.signature(BATCH.infer_theme)), "(title: 'str') -> 'str'")
        self.assertEqual(
            str(inspect.signature(BATCH.infer_methodology)),
            "(title: 'str', abstract: 'str', fulltext: 'str') -> 'str'",
        )
        self.assertEqual(
            str(inspect.signature(BATCH.infer_core_variable)),
            "(title: 'str', abstract: 'str') -> 'str'",
        )

    def test_complete_theme_keyword_matrix(self):
        cases = [
            ("HANK policy in Fictional Harbor", "异质主体宏观模型与政策传导"),
            ("Migration in Fictional Harbor", "人口迁移与空间劳动力配置"),
            ("Commuting in Fictional Harbor", "人口迁移与空间劳动力配置"),
            ("Housing in Northwind", "住房约束与空间资源错配"),
            ("Spatial policy in Northwind", "空间结构与宏观经济政策"),
            ("Geography of Northwind", "空间结构与宏观经济政策"),
            ("Monetary policy in Northwind", "货币政策传导与区域异质性"),
            ("Climate shocks in Northwind", "气候冲击与宏观经济"),
            ("A Quiet Fictional Archipelago", "空间宏观经济与异质性分析"),
        ]
        for title, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(BATCH.infer_theme(title), expected)

    def test_complete_theme_precedence(self):
        ordered = [
            ("hank", "异质主体宏观模型与政策传导"),
            ("migration", "人口迁移与空间劳动力配置"),
            ("housing", "住房约束与空间资源错配"),
            ("spatial", "空间结构与宏观经济政策"),
            ("monetary", "货币政策传导与区域异质性"),
            ("climate", "气候冲击与宏观经济"),
        ]
        for index, (_, expected) in enumerate(ordered):
            title = "Fictional " + " ".join(keyword for keyword, _ in ordered[index:])
            with self.subTest(priority=index + 1):
                self.assertEqual(BATCH.infer_theme(title), expected)
                self.assertEqual(BATCH.infer_theme(title), BATCH.infer_theme(title))

    def test_complete_methodology_keyword_matrix(self):
        cases = [
            ("gravity", "引力模型与迁移流估计"),
            ("hank", "HANK模型与政策冲击分析"),
            ("dynamic spatial", "动态空间一般均衡模型"),
            ("spatial general equilibrium", "动态空间一般均衡模型"),
            ("deep learning", "深度学习近似动态规划"),
            ("neural", "深度学习近似动态规划"),
            ("difference-in-differences", "准实验识别与计量估计"),
            ("instrument", "准实验识别与计量估计"),
            ("model", "结构模型与数值模拟"),
            ("descriptive fictional essay", "文献综述或理论分析"),
        ]
        for keyword, expected in cases:
            with self.subTest(keyword=keyword):
                self.assertEqual(
                    BATCH.infer_methodology("Northwind Study", f"Uses {keyword} evidence.", ""),
                    expected,
                )

    def test_complete_methodology_precedence(self):
        ordered = [
            ("gravity", "引力模型与迁移流估计"),
            ("hank", "HANK模型与政策冲击分析"),
            ("dynamic spatial", "动态空间一般均衡模型"),
            ("deep learning", "深度学习近似动态规划"),
            ("difference-in-differences", "准实验识别与计量估计"),
            ("model", "结构模型与数值模拟"),
        ]
        for index, (_, expected) in enumerate(ordered):
            abstract = "Fictional study using " + " and ".join(
                keyword for keyword, _ in ordered[index:]
            )
            with self.subTest(priority=index + 1):
                self.assertEqual(BATCH.infer_methodology("Northwind", abstract, ""), expected)

    def test_methodology_fulltext_8000_character_boundary(self):
        inside = "x" * 7993 + "gravity"
        outside = "x" * 8000 + "gravity"
        self.assertEqual(len(inside), 8000)
        self.assertEqual(
            BATCH.infer_methodology("Northwind", "Fictional evidence", inside),
            "引力模型与迁移流估计",
        )
        self.assertEqual(
            BATCH.infer_methodology("Northwind", "Fictional evidence", outside),
            "文献综述或理论分析",
        )

    def test_complete_core_variable_keyword_matrix(self):
        cases = [
            ("migration", "迁移流、城市便利性和就业机会"),
            ("commuting", "通勤联系、本地就业弹性和福利"),
            ("housing", "住房供给、价格约束和就业增长"),
            ("monetary", "货币政策冲击、收入分布和消费响应"),
            ("hank", "家庭异质性、资产分布和政策传导"),
            ("unclassified fictional measure", "空间分布、异质性和政策响应"),
        ]
        for keyword, expected in cases:
            with self.subTest(keyword=keyword):
                self.assertEqual(
                    BATCH.infer_core_variable("Northwind Study", f"Tracks {keyword}."),
                    expected,
                )

    def test_complete_core_variable_precedence(self):
        ordered = [
            ("migration", "迁移流、城市便利性和就业机会"),
            ("commuting", "通勤联系、本地就业弹性和福利"),
            ("housing", "住房供给、价格约束和就业增长"),
            ("monetary", "货币政策冲击、收入分布和消费响应"),
            ("hank", "家庭异质性、资产分布和政策传导"),
        ]
        for index, (_, expected) in enumerate(ordered):
            abstract = "Fictional study of " + " and ".join(
                keyword for keyword, _ in ordered[index:]
            )
            with self.subTest(priority=index + 1):
                self.assertEqual(BATCH.infer_core_variable("Northwind", abstract), expected)


class NoteRendererContractTests(unittest.TestCase):
    MAJOR_SECTIONS = [
        "## 基本信息",
        "## 一句话摘要",
        "## 研究对象",
        "## 研究方法",
        "## 数据来源",
        "## 研究结论",
        "## 我的判断",
    ]

    def test_public_signatures(self):
        self.assertEqual(
            str(inspect.signature(BATCH.make_note)),
            "(payload: 'dict[str, Any]', collection: 'str') -> 'str'",
        )
        self.assertEqual(
            str(inspect.signature(DEEP.make_deep_note)),
            "(payload: 'dict[str, Any]', collection: 'str') -> 'str'",
        )

    def test_first_pass_synthetic_golden_structure_and_determinism(self):
        payload = fictional_payload()
        with mock.patch.object(BATCH, "datetime", FrozenDateTime):
            first = BATCH.make_note(payload, "Fictional Mobility")
            second = BATCH.make_note(payload, "Fictional Mobility")

        self.assertEqual(first, second)
        self.assertTrue(first.startswith("---\n"))
        self.assertTrue(first.endswith("\n"))
        self.assertIn("# Migration & Work in Fictional Harbor", first)
        self.assertIn('reading_stage: "初录入"', first)
        self.assertIn('evidence_level: "E0"', first)
        self.assertIn("citation_eligible: false", first)
        self.assertIn("zotero://select/library/items/FIC1001", first)
        self.assertNotIn("zotero://open-pdf/", first)
        assert_ordered(self, first, self.MAJOR_SECTIONS)

    def test_deep_read_synthetic_golden_structure_and_determinism(self):
        payload = fictional_payload(with_fulltext=True)
        with mock.patch.object(DEEP, "datetime", FrozenDateTime):
            first = DEEP.make_deep_note(payload, "Fictional Housing")
            second = DEEP.make_deep_note(payload, "Fictional Housing")

        self.assertEqual(first, second)
        self.assertTrue(first.endswith("\n"))
        self.assertIn("# Housing Constraints in Northwind", first)
        self.assertIn('reading_stage: "二次精读"', first)
        self.assertIn('evidence_level: "E2"', first)
        self.assertIn('citation_status: "candidate_needs_human_verification"', first)
        self.assertIn("human_verified: false", first)
        self.assertIn("zotero://select/library/items/FIC2002", first)
        self.assertIn("zotero://open-pdf/library/items/PDF2002?page=1", first)
        assert_ordered(self, first, self.MAJOR_SECTIONS)

    def test_missing_or_malformed_template_fails_closed(self):
        malformed = "# Synthetic malformed template without required structure\n"
        renderers = [
            ("batch_import_collection.py", "make_note"),
            ("deep_read_collection.py", "make_deep_note"),
        ]
        for script_name, function_name in renderers:
            for case, template_text in (("missing", None), ("malformed", malformed)):
                with self.subTest(renderer=function_name, case=case):
                    self.assertNotEqual(
                        isolated_renderer_exit_code(script_name, function_name, template_text),
                        0,
                        "renderer accepted a missing or malformed authorized template",
                    )

    def test_product_python_does_not_embed_runtime_template_skeleton(self):
        template = (ROOT / "templates" / "论文精读模板.md").read_text(encoding="utf-8")
        skeleton = [
            line
            for line in template.splitlines()
            if line.startswith(("## ", "### ", "| 项目 |", "> 用 1 句话", "- **方法类型**"))
        ]
        self.assertTrue(skeleton)
        for path in sorted((ROOT / "skills").glob("**/*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            strings = [
                node.value
                for node in ast.walk(tree)
                if isinstance(node, ast.Constant) and isinstance(node.value, str)
            ]
            for fragment in skeleton:
                with self.subTest(path=path.relative_to(ROOT), fragment=fragment):
                    self.assertFalse(
                        any(fragment in value for value in strings),
                        f"product Python embeds runtime template skeleton: {fragment}",
                    )


class MetadataNormalizationContractTests(unittest.TestCase):
    def test_public_signatures(self):
        expected = {
            "clean_doi": "(value: 'str | None') -> 'str | None'",
            "crossref_lookup": "(doi: 'str | None', email: 'str | None') -> 'dict[str, Any] | None'",
            "crossref_title_search": "(title: 'str | None', email: 'str | None') -> 'dict[str, Any] | None'",
            "openalex_lookup": "(doi: 'str | None', title: 'str | None', email: 'str | None') -> 'dict[str, Any] | None'",
            "unpaywall_lookup": "(doi: 'str | None', email: 'str | None') -> 'dict[str, Any] | None'",
            "add_online_supplements": "(payload: 'dict[str, Any]', email: 'str | None', skip_unpaywall: 'bool' = False) -> 'dict[str, Any]'",
        }
        for name, signature in expected.items():
            with self.subTest(name=name):
                self.assertEqual(str(inspect.signature(getattr(FETCH, name))), signature)

    def test_doi_abstract_and_title_normalization(self):
        self.assertEqual(FETCH.clean_doi(" https://doi.org/10.5555/FICTION.7. "), "10.5555/FICTION.7")
        self.assertIsNone(FETCH.clean_doi("  "))
        self.assertEqual(
            FETCH.abstract_from_openalex({"Northwind": [1], "Trade": [0]}),
            "Trade Northwind",
        )
        self.assertEqual(FETCH.normalize_title("<i>Northwind</i>: Trade!"), "northwind trade")
        self.assertEqual(FETCH.title_similarity("Northwind: Trade!", "Northwind Trade"), 1.0)
        self.assertTrue(FETCH.title_matches("Northwind: Trade!", "Northwind Trade"))
        self.assertFalse(FETCH.title_matches("Northwind Trade", "Southern Health"))

    def test_crossref_success_and_failure_are_normalized(self):
        response = {
            "message": {
                "DOI": "10.5555/fiction.7",
                "title": ["Northwind Trade"],
                "container-title": ["Fictional Review"],
                "publisher": "Example Press",
                "type": "journal-article",
                "published-online": {"date-parts": [[2025, 2, 3]]},
                "abstract": "<jats:p>Synthetic abstract.</jats:p>",
                "URL": "https://example.invalid/work",
            }
        }
        with mock.patch.object(FETCH, "http_json", return_value=response):
            result = FETCH.crossref_lookup("10.5555/fiction.7", "reader@example.invalid")
        self.assertEqual(
            result,
            {
                "DOI": "10.5555/fiction.7",
                "title": "Northwind Trade",
                "container_title": "Fictional Review",
                "publisher": "Example Press",
                "type": "journal-article",
                "published_year": 2025,
                "abstract": "Synthetic abstract.",
                "url": "https://example.invalid/work",
            },
        )
        with mock.patch.object(FETCH, "http_json", side_effect=TimeoutError("synthetic timeout")):
            self.assertIsNone(FETCH.crossref_lookup("10.5555/fiction.7", None))

    def test_openalex_success_and_failure_are_normalized(self):
        response = {
            "id": "https://openalex.org/WFIC7",
            "doi": "https://doi.org/10.5555/fiction.7",
            "title": "Northwind Trade",
            "publication_year": 2025,
            "type": "article",
            "open_access": {"is_oa": True, "oa_status": "gold"},
            "abstract_inverted_index": {"Northwind": [1], "Trade": [0]},
            "primary_location": {"landing_page_url": "https://example.invalid/landing"},
            "locations": [],
        }
        with mock.patch.object(FETCH, "http_json", return_value=response):
            result = FETCH.openalex_lookup("10.5555/fiction.7", None, None)
        self.assertEqual(result["abstract"], "Trade Northwind")
        self.assertEqual(result["oa_status"], "gold")
        self.assertEqual(result["locations"], [])
        with mock.patch.object(FETCH, "http_json", side_effect=ValueError("synthetic JSON error")):
            self.assertIsNone(FETCH.openalex_lookup(None, "Northwind Trade", None))

    def test_unpaywall_success_failure_and_required_email(self):
        response = {
            "doi": "10.5555/fiction.7",
            "doi_url": "https://doi.org/10.5555/fiction.7",
            "title": "Northwind Trade",
            "year": 2025,
            "is_oa": True,
            "oa_status": "green",
            "best_oa_location": {"url": "https://example.invalid/copy"},
            "oa_locations": [],
        }
        with mock.patch.object(FETCH, "http_json", return_value=response):
            result = FETCH.unpaywall_lookup("10.5555/fiction.7", "reader@example.invalid")
        self.assertEqual(result["oa_status"], "green")
        self.assertIsNone(FETCH.unpaywall_lookup("10.5555/fiction.7", None))
        with mock.patch.object(FETCH, "http_json", side_effect=TimeoutError("synthetic timeout")):
            self.assertIsNone(
                FETCH.unpaywall_lookup("10.5555/fiction.7", "reader@example.invalid")
            )

    def test_oa_locations_are_ordered_and_deduplicated(self):
        shared = "https://example.invalid/open.pdf"
        payload = {
            "unpaywall": {
                "best_oa_location": {"url_for_pdf": shared, "license": "cc-by"},
                "oa_locations": [{"url_for_pdf": shared}],
            },
            "openalex": {
                "primary_location": {"pdf_url": "https://example.invalid/second.pdf", "is_oa": True},
                "locations": [],
            },
        }
        locations = FETCH.collect_oa_locations(payload)
        self.assertEqual([entry["source"] for entry in locations], ["unpaywall", "openalex"])
        self.assertEqual(len(locations), 2)

    def test_partial_aggregate_is_explicit_and_offline(self):
        payload = {
            "item": {"data": {"title": "Northwind Trade", "DOI": "doi:10.5555/fiction.7"}},
            "attachments": [],
            "notes": [],
            "annotations": [],
        }
        with (
            mock.patch.object(FETCH, "crossref_lookup", return_value=None),
            mock.patch.object(FETCH, "openalex_lookup", return_value=None),
            mock.patch.object(FETCH, "unpaywall_lookup", return_value=None),
        ):
            result = FETCH.add_online_supplements(payload, "reader@example.invalid")

        self.assertIs(result, payload)
        supplements = result["online_supplements"]
        self.assertEqual(supplements["doi"], "10.5555/fiction.7")
        self.assertIsNone(supplements["crossref"])
        self.assertIsNone(supplements["openalex"])
        self.assertIsNone(supplements["unpaywall"])
        self.assertEqual(supplements["oa_locations"], [])
        self.assertEqual(result["raw_data_quality"]["level"], "metadata_only")
        self.assertIn("## Metadata", result["raw_data_buffer"])

    def test_openalex_doi_title_mismatch_warns_and_retries_once_by_title(self):
        payload = {
            "item": {
                "data": {
                    "title": "Northwind Trade",
                    "DOI": "10.5555/fiction.8",
                }
            },
            "attachments": [],
            "notes": [],
            "annotations": [],
        }
        mismatched = {"id": "https://openalex.org/WBAD", "title": "Southern Health"}
        validated = {"id": "https://openalex.org/WGOOD", "title": "Northwind Trade"}
        with (
            mock.patch.object(FETCH, "crossref_lookup", return_value=None),
            mock.patch.object(FETCH, "openalex_lookup", side_effect=[mismatched, validated]) as lookup,
            mock.patch.object(FETCH, "unpaywall_lookup", return_value=None),
        ):
            result = FETCH.add_online_supplements(payload, "reader@example.invalid")

        lookup.assert_has_calls(
            [
                mock.call("10.5555/fiction.8", "Northwind Trade", "reader@example.invalid"),
                mock.call(None, "Northwind Trade", "reader@example.invalid"),
            ]
        )
        self.assertEqual(lookup.call_count, 2)
        supplements = result["online_supplements"]
        self.assertIs(supplements["openalex"], validated)
        self.assertEqual(len(supplements["warnings"]), 1)
        self.assertTrue(supplements["warnings"][0].strip())

    def test_openalex_title_only_mismatch_warns_rejects_and_does_not_retry(self):
        payload = {
            "item": {"data": {"title": "Northwind Trade"}},
            "attachments": [],
            "notes": [],
            "annotations": [],
        }
        response = {
            "results": [
                {
                    "id": "https://openalex.org/WBAD",
                    "title": "Southern Health",
                    "open_access": {"is_oa": False, "oa_status": "closed"},
                    "locations": [],
                }
            ]
        }
        with (
            mock.patch.object(FETCH, "crossref_title_search", return_value=None),
            mock.patch.object(FETCH, "unpaywall_lookup", return_value=None),
            mock.patch.object(FETCH, "http_json", return_value=response) as http_json,
        ):
            result = FETCH.add_online_supplements(payload, "reader@example.invalid")

        self.assertEqual(http_json.call_count, 1)
        supplements = result["online_supplements"]
        self.assertIsNone(supplements["doi"])
        self.assertIsNone(supplements["openalex"])
        self.assertEqual(len(supplements["warnings"]), 1)
        self.assertTrue(supplements["warnings"][0].strip())


if __name__ == "__main__":
    unittest.main()
