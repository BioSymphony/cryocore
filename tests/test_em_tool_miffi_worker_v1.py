"""Offline adapter contract checks; tiny fixtures are not scientific evidence."""
import argparse
import json
from pathlib import Path
import pickle
import subprocess
import sys

import pytest

from scripts.cryocore import em_tool_miffi_worker_v1 as worker


class TensorFixture:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return self.values


def result_fixture():
    scores = [.25] * 4 + [.5] * 2 + [1 / 3] * 3 + [.5] * 2
    return {"mic_list": [Path("a.mrc")],
            "mic_pred_confidence": TensorFixture([[scores]]),
            "outputs": TensorFixture([[[0.] * 11]]),
            "combined_preds": TensorFixture([[[0, 0, 0, 0]], [[0, 0, 0, 0]]])}


def export_fixture(tmp_path, value):
    native = tmp_path / "fresh-native.pkl"
    native.write_bytes(pickle.dumps(value))
    return worker.export_native(native, ["a.mrc"], tmp_path)


def test_native_command_uses_original_mrc_plain_text_and_exact_full_model(tmp_path):
    args = argparse.Namespace(input_dir=tmp_path, model_name="miffi_no_ps_v1",
                              pixel_size=.885, checkpoint=tmp_path / "model.pt",
                              batch_size=2, num_workers=2, gpu_id=0, use_cpu=False)
    cmd = worker.native_command(args, tmp_path / "cohort.txt", tmp_path / "native")
    assert cmd[:3] == [sys.executable, "-m", "miffi.inference"]
    assert cmd[cmd.index("--fm") + 1] == str(args.checkpoint)
    assert cmd[cmd.index("--pixel-size") + 1] == "0.885"
    assert "--no-ps" in cmd
    assert "--sd" not in cmd
    assert "--use-cpu" not in cmd
    args.model_name = "miffi_v1"
    assert "--no-ps" not in worker.native_command(args, tmp_path / "c", tmp_path / "n")


def test_native_fourier_and_pixel_size_rules_are_declared():
    native = worker.preprocessing([4096, 4096], .885, False)
    assert native["fourier_crop_shape_yx"] == [2416, 2416]
    assert native["channel_count"] == 2
    assert native["training_pixel_size_mismatch"] is False
    assert "not squared" in native["spectrum_transform"]
    binned = worker.preprocessing([4096, 2048], 3.54, False)
    assert binned["transpose"] is True
    assert binned["square_split_count"] == 2
    assert binned["fourier_crop_shape_yx"] == [2048, 2048]
    assert binned["training_pixel_size_mismatch"] is True
    assert worker.preprocessing([2048, 2048], 3.54, True)["channel_count"] == 1


def test_export_preserves_all_native_probabilities_and_logits(tmp_path):
    counts = export_fixture(tmp_path, result_fixture())
    assert counts == {"micrograph_count": 1, "split_count": 1, "score_rows": 11}
    safe = json.loads((tmp_path / "predictions.json").read_text())
    assert safe["policy"] == "advisory_only_no_rejection_or_deletion"
    assert len((tmp_path / "micrograph_filter_scores.csv").read_text().splitlines()) == 12


@pytest.mark.parametrize("failure", ["wrong_input", "bad_probability", "nonfinite_logit", "bad_split"])
def test_export_rejects_wrong_cohort_or_invalid_scores(tmp_path, failure):
    result = result_fixture()
    if failure == "wrong_input":
        result["mic_list"] = [Path("different.mrc")]
    elif failure == "bad_probability":
        result["mic_pred_confidence"].values[0][0][0] = 2
    elif failure == "nonfinite_logit":
        result["outputs"].values[0][0][0] = float("nan")
    elif failure == "bad_split":
        result["combined_preds"].values[1][0][0] = 10
    with pytest.raises(ValueError):
        export_fixture(tmp_path, result)
    assert not (tmp_path / "predictions.json").exists()


def test_pinned_git_head_alone_does_not_allow_changed_upstream_code(tmp_path, monkeypatch):
    (tmp_path / "miffi").mkdir()
    (tmp_path / "miffi" / "__init__.py").write_text("raise RuntimeError('changed')")
    monkeypatch.setattr(subprocess, "check_output", lambda *a, **k: worker.SOURCE_COMMIT)
    with pytest.raises(ValueError, match="source bytes changed"):
        worker.verify_source(tmp_path)


def test_native_timeout_kills_process_and_retains_log(tmp_path):
    receipt = worker.run_native([sys.executable, "-c", "import time; print('start', flush=True); time.sleep(30)"],
                                tmp_path, {}, tmp_path / "native.log", 1)
    assert receipt["timed_out"] is True
    assert receipt["returncode"] != 0
    assert "start" in (tmp_path / "native.log").read_text()
    assert receipt["elapsed_seconds"] < 10


def test_failed_checkpoint_writes_failure_manifest_without_loading_pickle(tmp_path, monkeypatch):
    monkeypatch.setattr(worker, "verify_source", lambda p: {"commit": worker.SOURCE_COMMIT})
    checkpoint = tmp_path / "model.pt"
    checkpoint.write_bytes(b"wrong-checkpoint")
    out = tmp_path / "output"
    code = worker.main(["--input-dir", str(tmp_path), "--checkpoint", str(checkpoint),
                        "--source-dir", str(tmp_path), "--output-dir", str(out),
                        "--checkpoint-sha256", "0" * 64, "--model-name", "miffi_v1",
                        "--pixel-size", ".885"])
    assert code == 1
    manifest = json.loads((out / "miffi_qc_manifest.json").read_text())
    assert manifest["status"] == "failed"
    assert "Checkpoint does not match" in manifest["error"]
    assert "execution" not in manifest
    with pytest.raises(FileExistsError):
        worker.main(["--input-dir", str(tmp_path), "--checkpoint", str(checkpoint),
                     "--source-dir", str(tmp_path), "--output-dir", str(out),
                     "--checkpoint-sha256", "0" * 64, "--model-name", "miffi_v1", "--pixel-size", ".885"])
