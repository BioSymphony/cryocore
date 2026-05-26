import json
from pathlib import Path

from scripts.cryocore.preflight import REQUIRED_PATHS
from scripts.cryocore.software_registry_check import REQUIRED_FIELDS, parse_registry


ROOT = Path(__file__).resolve().parents[1]


def test_required_paths_exist() -> None:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    assert missing == []


def test_registry_has_required_fields() -> None:
    entries = parse_registry(ROOT / "references/software-registry.yaml")
    assert "relion" in entries
    assert "chimerax" in entries
    assert "modelangelo" in entries
    assert "cryoatom" in entries
    assert "emdb_api" in entries
    assert "nextflow" in entries
    missing = {
        name: sorted(REQUIRED_FIELDS - fields)
        for name, fields in entries.items()
        if REQUIRED_FIELDS - fields
    }
    assert missing == {}


def test_chimerax_is_intentionally_duplicated() -> None:
    registry = (ROOT / "references/software-registry.yaml").read_text()
    shared_doc = (ROOT / "docs/chimerax-shared-posture.md").read_text()
    split_doc = (ROOT / "docs/move-duplicate-map.md").read_text()
    assert "chimerax:" in registry
    assert "Intentionally duplicated" in registry or "intentionally duplicated" in registry
    assert "intentionally duplicated" in shared_doc
    assert "ChimeraX is intentionally in both repos" in split_doc


def test_shared_tooling_doc_keeps_cryo_model_building_in_cryocore() -> None:
    tooling = (ROOT / "docs/tooling-and-licensing.md").read_text()
    assert "ChimeraX is intentionally duplicated with Structure Factory" in tooling
    assert "ModelAngelo posture" not in tooling
    assert "belongs in CryoCore" in tooling


def test_motioncor3_is_open_toolcheck() -> None:
    lane = json.loads((ROOT / "modules/lane-modules/motioncor3.toolcheck.v1.json").read_text())
    assert lane["mode"] == "toolcheck"
    assert lane["license_gate"] == "none"
    assert "required_secret_refs" not in lane


def test_active_contracts_do_not_reference_structure_factory_runtime_leaks() -> None:
    active_paths = [
        *ROOT.glob("modules/**/*.json"),
        *ROOT.glob("runpod/launch-manifests/*.json"),
        *ROOT.glob("runpod/stage-contracts/*.json"),
        *ROOT.glob("scripts/cryocore/*.py"),
    ]
    forbidden = [
        "screening-superpowers",
        "screening_fixture_run",
        "provider_adapter_dry_run",
        "gpcr-chimerax-render",
        "demos/gpcr-activation-atlas",
        "MOTIONCOR3_ACCESS_REF",
    ]
    failures = []
    for path in active_paths:
        text = path.read_text()
        for token in forbidden:
            if token in text:
                failures.append(f"{path.relative_to(ROOT)} contains {token}")
    assert failures == []


def test_public_accession_metadata_example_is_metadata_only() -> None:
    metadata = json.loads((ROOT / "examples/public-accession-metadata/metadata.json").read_text())
    assert metadata["raw_data_download_required"] is False
    assert metadata["fetch_performed"] is False
    assert "https://www.ebi.ac.uk/emdb/api/entry/EMD-43816" in metadata["source_api_endpoints"]
    assert any(url.endswith("9asj_validation.xml.gz") for url in metadata["validation_report_urls"])
