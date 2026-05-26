from pathlib import Path

from scripts.cryocore.skill_pack_check import check_skill_pack


ROOT = Path(__file__).resolve().parents[1]


def test_skill_pack_index_passes() -> None:
    summary = check_skill_pack(ROOT / "skills/index.yaml")
    assert summary["ok"] is True, summary["errors"]
    assert summary["skill_count"] >= 7

