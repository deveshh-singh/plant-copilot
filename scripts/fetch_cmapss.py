"""Download NASA C-MAPSS to data/raw/cmapss/ and optionally upload it to a UC volume.

    uv run python scripts/fetch_cmapss.py            # download (cached), extract, manifest
    uv run python scripts/fetch_cmapss.py --upload   # ...then copy the 12 files to the volume

Standard library only. The zip is kept in data/raw/ so reruns never download again.
"""

import argparse
import hashlib
import io
import json
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

URL = (
    "https://phm-datasets.s3.amazonaws.com/NASA/"
    "6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip"
)
RAW_DIR = Path("data/raw")
ZIP_PATH = RAW_DIR / "cmapss_source.zip"
OUT_DIR = RAW_DIR / "cmapss"
VOLUME_DIR = "dbfs:/Volumes/workspace/plant_bronze/raw/cmapss/"
PROFILE = "plant-copilot"

EXPECTED_FILES = tuple(
    f"{kind}_FD00{n}.txt" for kind in ("train", "test", "RUL") for n in range(1, 5)
)


class MissingFilesError(Exception):
    pass


def extract_nested(zip_path: Path, out_dir: Path) -> None:
    """Write the expected .txt files found in zip_path (or any zip inside it) to out_dir, flat."""
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        _extract_from(zf, out_dir)


def _extract_from(zf: zipfile.ZipFile, out_dir: Path) -> None:
    for info in zf.infolist():
        name = Path(info.filename).name
        if name in EXPECTED_FILES:
            (out_dir / name).write_bytes(zf.read(info))
        elif name.lower().endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(zf.read(info))) as inner:
                _extract_from(inner, out_dir)


def find_cmapss_files(directory: Path) -> dict[str, Path]:
    """Map each expected file name to its path; raise MissingFilesError naming any absent."""
    missing = [n for n in EXPECTED_FILES if not (directory / n).is_file()]
    if missing:
        raise MissingFilesError(f"missing from {directory}: {', '.join(missing)}")
    return {n: directory / n for n in EXPECTED_FILES}


def manifest(files: dict[str, Path]) -> dict[str, dict]:
    """File name -> bytes, sha256 and line count."""
    result = {}
    for name, path in files.items():
        data = path.read_bytes()
        result[name] = {
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "lines": data.count(b"\n"),
        }
    return result


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    """Download to a .part file first, so an interrupted run never leaves a half zip."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url) as resp, part.open("wb") as f:
        shutil.copyfileobj(resp, f)
    part.rename(dest)


class UploadError(Exception):
    pass


def _cli(*args: str) -> None:
    cmd = ["databricks", *args, "-p", PROFILE]
    done = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise UploadError(f"{' '.join(cmd)}\n  {done.stderr.strip()}")


def upload(files: dict[str, Path]) -> int:
    """Copy the files into the volume folder. The volume itself is created by T-002's setup."""
    _cli("fs", "mkdir", VOLUME_DIR)
    for path in files.values():
        _cli("fs", "cp", "--overwrite", str(path), VOLUME_DIR)
    return len(files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--upload", action="store_true", help="copy the 12 files to the volume")
    args = parser.parse_args(argv)

    if ZIP_PATH.exists():
        print(f"cached: {ZIP_PATH} (no download)")
    else:
        print(f"downloading {URL}")
        download(URL, ZIP_PATH)
    print(f"zip: {ZIP_PATH.stat().st_size} bytes, sha256 {sha256_of(ZIP_PATH)}")

    extract_nested(ZIP_PATH, OUT_DIR)
    try:
        files = find_cmapss_files(OUT_DIR)
    except MissingFilesError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    m = manifest(files)
    (OUT_DIR / "MANIFEST.json").write_text(json.dumps(m, indent=2) + "\n")
    for name, info in m.items():
        print(f"{name:16} {info['lines']:>7} lines")

    if args.upload:
        try:
            print(f"uploaded {upload(files)} files to {VOLUME_DIR}")
        except UploadError as e:
            print(f"error: upload failed (does the volume exist? see T-002):\n{e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
