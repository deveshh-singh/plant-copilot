"""Tests for scripts/fetch_cmapss.py. Tiny fake zips in tmp_path; never the network."""

import hashlib
import io
import zipfile

import pytest

from scripts.fetch_cmapss import (
    EXPECTED_FILES,
    MissingFilesError,
    extract_nested,
    find_cmapss_files,
    manifest,
)


def _fake_contents() -> dict[str, bytes]:
    # One line per unit number, so each file has a known, different line count.
    return {name: b"1 2 3\n" * (i + 1) for i, name in enumerate(EXPECTED_FILES)}


def _write_zip(path, members: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in members.items():
            zf.writestr(name, data)


def _zip_bytes(members: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    return buf.getvalue()


def test_expected_files_are_the_twelve():
    assert len(EXPECTED_FILES) == 12
    assert "train_FD001.txt" in EXPECTED_FILES
    assert "RUL_FD004.txt" in EXPECTED_FILES


def test_extract_flat_zip_keeps_only_the_twelve(tmp_path):
    members = {f"CMAPSSData/{n}": d for n, d in _fake_contents().items()}
    members["CMAPSSData/readme.txt"] = b"ignore me"
    members["CMAPSSData/Damage Propagation Modeling.pdf"] = b"%PDF"
    src = tmp_path / "src.zip"
    _write_zip(src, members)
    out = tmp_path / "out"

    extract_nested(src, out)

    assert sorted(p.name for p in out.iterdir()) == sorted(EXPECTED_FILES)


def test_extract_nested_zip(tmp_path):
    inner = _zip_bytes(_fake_contents())
    src = tmp_path / "outer.zip"
    _write_zip(src, {"6. Turbofan/CMAPSSData.zip": inner, "6. Turbofan/readme.txt": b"x"})
    out = tmp_path / "out"

    extract_nested(src, out)

    assert sorted(p.name for p in out.iterdir()) == sorted(EXPECTED_FILES)
    assert (out / "train_FD001.txt").read_bytes() == _fake_contents()["train_FD001.txt"]


def test_find_cmapss_files_returns_all_twelve(tmp_path):
    for name, data in _fake_contents().items():
        (tmp_path / name).write_bytes(data)

    found = find_cmapss_files(tmp_path)

    assert set(found) == set(EXPECTED_FILES)
    assert found["test_FD003.txt"] == tmp_path / "test_FD003.txt"


def test_find_cmapss_files_names_the_missing_file(tmp_path):
    # A5: the fake zip is built without one file; the check must name it.
    contents = _fake_contents()
    del contents["test_FD002.txt"]
    src = tmp_path / "src.zip"
    _write_zip(src, contents)
    out = tmp_path / "out"
    extract_nested(src, out)

    with pytest.raises(MissingFilesError, match="test_FD002.txt"):
        find_cmapss_files(out)


def test_manifest_records_bytes_sha256_and_lines(tmp_path):
    p = tmp_path / "RUL_FD001.txt"
    data = b"112\n98\n69\n"
    p.write_bytes(data)

    m = manifest({"RUL_FD001.txt": p})

    assert m == {
        "RUL_FD001.txt": {
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "lines": 3,
        }
    }
