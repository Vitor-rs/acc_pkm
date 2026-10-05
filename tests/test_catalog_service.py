"""
Tests for core.catalog_service
"""
import json
from pathlib import Path

from core.catalog_service import (
    reindex_catalog,
)


def test_catalog_lifecycle(tmp_path: Path):
    lake_dir = tmp_path / "_lake"
    lake_dir.mkdir(parents=True)
    catalog_html = tmp_path / "_lake_catalog.html"
    catalog_jsonl = tmp_path / "documents.jsonl"

    # Create dummy markdown file with frontmatter
    md_file = lake_dir / "2026-03-01_Test_Paper.md"
    md_file.write_text(
        "---\n"
        "title: \"Test Academic Article\"\n"
        "date: '2026-03-01'\n"
        "tags: [metodologia, teste]\n"
        "type: paper\n"
        "---\n\n"
        "# Test Academic Article\n\nThis is a sample document for catalog testing.\n",
        encoding="utf-8"
    )

    # Reindex
    items = reindex_catalog(lake_dir, catalog_html, catalog_jsonl)
    assert len(items) == 1
    assert items[0]["titulo"] == "Test Academic Article"
    assert "metodologia" in items[0]["tags"]
    assert catalog_html.exists()
    assert catalog_jsonl.exists()

    # Verify JSONL content
    lines = catalog_jsonl.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["filename"] == "2026-03-01_Test_Paper.md"
    assert data["media_type"] == "md"

    # Verify HTML content
    html_content = catalog_html.read_text(encoding="utf-8")
    assert "Test Academic Article" in html_content
    assert "<!DOCTYPE html>" in html_content
