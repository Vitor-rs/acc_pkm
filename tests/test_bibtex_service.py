"""
Tests for core.bibtex_service
"""
from pathlib import Path

from core.bibtex_service import (
    add_entries_to_bib,
    audit_master_bib,
    extract_citekeys,
    extract_dois,
    parse_bibtex_entries,
)

SAMPLE_BIB_1 = """@article{smith2024ai,
  title={AI in Academic Research},
  author={Smith, John and Doe, Jane},
  journal={Journal of PKM},
  year={2024},
  doi={10.1000/182}
}"""

SAMPLE_BIB_2 = """@book{creswell2018research,
  title={Research Design: Qualitative, Quantitative, and Mixed Methods Approaches},
  author={Creswell, John W. and Creswell, J. David},
  year={2018},
  publisher={SAGE Publications}
}"""


def test_extract_citekeys():
    keys = extract_citekeys(SAMPLE_BIB_1 + "\n" + SAMPLE_BIB_2)
    assert keys == ["smith2024ai", "creswell2018research"]


def test_extract_dois():
    dois = extract_dois(SAMPLE_BIB_1)
    assert "10.1000/182" in dois


def test_parse_bibtex_entries():
    combined = SAMPLE_BIB_1 + "\n\n" + SAMPLE_BIB_2
    parsed = parse_bibtex_entries(combined)
    assert len(parsed) == 2
    assert "smith2024ai" in parsed
    assert "creswell2018research" in parsed
    assert "@article{smith2024ai" in parsed["smith2024ai"]


def test_add_entries_to_bib_deduplication(tmp_path: Path):
    bib_file = tmp_path / "test_master.bib"

    # 1. Add first entry
    added_1 = add_entries_to_bib([SAMPLE_BIB_1], bib_file, header_comment="% Test Entry 1")
    assert added_1 == 1
    assert bib_file.exists()

    # 2. Add duplicate entry - should be skipped
    added_2 = add_entries_to_bib([SAMPLE_BIB_1], bib_file)
    assert added_2 == 0

    # 3. Add second new entry
    added_3 = add_entries_to_bib([SAMPLE_BIB_2], bib_file)
    assert added_3 == 1

    # 4. Audit
    audit = audit_master_bib(bib_file)
    assert audit["total_entries"] == 2
    assert audit["unique_keys"] == 2
    assert len(audit["duplicate_keys"]) == 0
