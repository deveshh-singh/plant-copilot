"""Names, units and comments for the C-MAPSS tables (bronze and silver).

Sensor mnemonics, descriptions and units follow Saxena, Goebel, Simon and Eklund (2008),
"Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation", PHM 2008,
Table 2 (D-009). The dataset facts in `DATASETS` come from the readme shipped with the
NASA C-MAPSS turbofan data. Engine counts are never stored here: they are computed from
the data in `cmapss.to_datasets`.

Every column of every table has a comment; the comments become Unity Catalog comments,
which is what the Text2SQL agent reads to understand the tables.
"""

# (raw column, silver name, description, unit), in file order s1..s21.
SENSORS: list[tuple[str, str, str, str]] = [
    ("s1", "t2", "Total temperature at fan inlet", "°R"),
    ("s2", "t24", "Total temperature at LPC outlet", "°R"),
    ("s3", "t30", "Total temperature at HPC outlet", "°R"),
    ("s4", "t50", "Total temperature at LPT outlet", "°R"),
    ("s5", "p2", "Pressure at fan inlet", "psia"),
    ("s6", "p15", "Total pressure in bypass-duct", "psia"),
    ("s7", "p30", "Total pressure at HPC outlet", "psia"),
    ("s8", "nf", "Physical fan speed", "rpm"),
    ("s9", "nc", "Physical core speed", "rpm"),
    ("s10", "epr", "Engine pressure ratio (P50/P2)", "–"),
    ("s11", "ps30", "Static pressure at HPC outlet", "psia"),
    ("s12", "phi", "Ratio of fuel flow to Ps30", "pps/psi"),
    ("s13", "nrf", "Corrected fan speed", "rpm"),
    ("s14", "nrc", "Corrected core speed", "rpm"),
    ("s15", "bpr", "Bypass ratio", "–"),
    ("s16", "farb", "Burner fuel-air ratio", "–"),
    ("s17", "htbleed", "Bleed enthalpy", "–"),
    ("s18", "nf_dmd", "Demanded fan speed", "rpm"),
    ("s19", "pcnfr_dmd", "Demanded corrected fan speed", "rpm"),
    ("s20", "w31", "HPT coolant bleed", "lbm/s"),
    ("s21", "w32", "LPT coolant bleed", "lbm/s"),
]

OP_SETTINGS = ["op_setting_1", "op_setting_2", "op_setting_3"]

# dataset -> (operating conditions, fault modes), from the C-MAPSS readme.
DATASETS: dict[str, tuple[int, str]] = {
    "FD001": (1, "HPC degradation"),
    "FD002": (6, "HPC degradation"),
    "FD003": (1, "HPC degradation, fan degradation"),
    "FD004": (6, "HPC degradation, fan degradation"),
}

_OP_COMMENT = (
    "Operational setting {n} of 3. Together the three settings define the flight condition "
    "(commonly read as altitude, Mach number and throttle resolver angle)."
)
_OPS = {name: _OP_COMMENT.format(n=i) for i, name in enumerate(OP_SETTINGS, start=1)}

_DATASET = "C-MAPSS subset: FD001, FD002, FD003 or FD004."
_SPLIT = "train (engines run until failure) or test (series stops some time before failure)."
_UNIT = "Engine number within its dataset and split file (1-based)."
_ENGINE_ID = "Unique engine key: dataset_split_unit, e.g. FD001_train_007."
_CYCLE = "Operating cycle number of the engine, starting at 1."

TABLE_COMMENTS: dict[str, str] = {
    "cmapss_raw": (
        "Bronze: NASA C-MAPSS turbofan run-to-failure readings exactly as in the text files, "
        "one row per engine per cycle, with raw sensor names s1..s21."
    ),
    "datasets": (
        "One row per C-MAPSS subset (FD001-FD004): operating conditions, fault modes and "
        "engine counts."
    ),
    "engines": "One row per simulated turbofan engine: its dataset, split, length and true RUL.",
    "sensor_readings": (
        "One row per engine per operating cycle: operational settings, the 21 sensor "
        "readings (paper mnemonics) and remaining useful life (RUL) in cycles."
    ),
}

COLUMN_COMMENTS: dict[str, dict[str, str]] = {
    "cmapss_raw": {
        "source_file": "Path of the text file the row was read from.",
        "dataset": _DATASET,
        "split": _SPLIT,
        "unit": _UNIT,
        "cycle": _CYCLE,
        **_OPS,
        **{raw: f"{desc} ({unit}); silver name {name}." for raw, name, desc, unit in SENSORS},
    },
    "datasets": {
        "dataset": _DATASET,
        "operating_conditions": "Number of distinct operating conditions in the subset.",
        "fault_modes": "Fault modes simulated in the subset (HPC = high-pressure compressor).",
        "train_engines": "Number of engines in the training split, counted from the data.",
        "test_engines": "Number of engines in the test split, counted from the data.",
    },
    "engines": {
        "engine_id": _ENGINE_ID,
        "dataset": _DATASET,
        "split": _SPLIT,
        "unit": _UNIT,
        "total_cycles": "Number of cycles recorded for the engine (its last cycle number).",
        "true_rul": (
            "Test engines only: true remaining useful life in cycles after the last recorded "
            "cycle (from RUL_FD00x.txt). Null for train engines, which run to failure."
        ),
    },
    "sensor_readings": {
        "dataset": _DATASET,
        "split": _SPLIT,
        "engine_id": _ENGINE_ID,
        "unit": _UNIT,
        "cycle": _CYCLE,
        **_OPS,
        **{name: f"{desc} ({unit}); raw column {raw}." for raw, name, desc, unit in SENSORS},
        "rul": (
            "Remaining useful life in cycles at this cycle. Train: last cycle - cycle. "
            "Test: true RUL + last recorded cycle - cycle."
        ),
    },
}
