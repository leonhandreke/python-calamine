from pathlib import Path

import pytest
from python_calamine import CalamineWorkbook

PATH = Path(__file__).parent / "data"


# NOTE: "hyperlinks_escaped.xlsx" from tafia/calamine
def test_hyperlinks_xlsx():
    reader = CalamineWorkbook.from_object(PATH / "hyperlinks_escaped.xlsx")

    hyperlinks = reader.get_sheet_by_name("Links").hyperlinks

    assert hyperlinks is not None
    assert [
        (h.range, h.target, h.location, h.displayed_text, h.tooltip) for h in hyperlinks
    ] == [
        (
            ((0, 0), (0, 0)),
            "https://example.com/search?q=a&page=2",
            None,
            None,
            None,
        ),
        (((0, 1), (1, 2)), "mailto:foo@example.com", None, None, "Email Foo"),
        (
            ((1, 0), (1, 0)),
            "https://www.rust-lang.org/",
            None,
            '"Rust" <home> &amp;',
            "Rust & Cargo",
        ),
        (((2, 0), (2, 0)), None, "'R&D'!B5", "Sheet2 B5", None),
        (((3, 0), (3, 0)), "file:///Book2.xlsx", None, None, None),
        (((4, 0), (4, 0)), "file:///..\\Sales\\Book2.xlsx", None, None, None),
        (((5, 0), (5, 0)), "file:///C:\\Temp\\Book1.xlsx", None, None, None),
        (((6, 0), (6, 0)), "file:///Book2.xlsx", "Sheet1!A1", None, None),
        (((7, 0), (7, 0)), "file:///Book2.xlsx", "'Sales Data'!A1:G5", None, None),
    ]


def test_hyperlinks_xlsx_empty():
    reader = CalamineWorkbook.from_object(PATH / "hyperlinks_escaped.xlsx")

    assert [] == reader.get_sheet_by_name("Sheet2").hyperlinks


@pytest.mark.parametrize("file", ["base.ods", "base.xls", "base.xlsb"])
def test_hyperlinks_not_supported(file):
    reader = CalamineWorkbook.from_object(PATH / file)

    assert None is reader.get_sheet_by_index(0).hyperlinks
