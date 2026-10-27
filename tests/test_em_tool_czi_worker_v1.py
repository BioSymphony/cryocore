import importlib.util
import json
import os
import struct
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("worker", Path(__file__).resolve().parents[1] / "scripts/cryocore/em_tool_czi_worker_v1.py")
w = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(w)


def ident(path):
    return {"path": str(path), "sha256": w.digest(path)}


def mrc(path):
    header = bytearray(1024)
    struct.pack_into("<4i", header, 0, 4, 3, 1, 2)
    header[208:212] = b"MAP "
    path.write_bytes(header + bytes(48))


class WorkerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.p = Path(self.tmp.name)
        self.input = self.p / "input.mrc"
        mrc(self.input)
        self.ref = self.p / "reference.star"
        self.ref.write_text("# Input file: input.mrc ; Number of micrographs: 1\n# Pixel size: 0.885 Angstroms ; acceleration voltage: 200 keV ; spherical aberration: 2.7 mm ; amplitude contrast: 0.1\n# Box size: 512 pixels\n1 12100 9900 0 0 0.5 4\n")
        self.bin = self.p / "fake"
        self.bin.write_text('''#!/usr/bin/env python3
import pathlib, sys
if '--version' in sys.argv:
 print('GCtfFind version 1.2.5')
else:
 out = pathlib.Path(sys.argv[sys.argv.index('-OutDir') + 1])
 (out / 'input_CTF.mrc').write_bytes(pathlib.Path(sys.argv[sys.argv.index('-InMrc') + 1]).read_bytes())
 (out / 'CTF.txt').write_text('# result\\ninput.mrc 0 10000 12000 40 0 0.6 4 0.89 0 0 0 0\\n')
 print('native evidence')
''')
        os.chmod(self.bin, 0o755)
        self.params = {"pixel_size_angstrom": 0.885, "voltage_kv": 200, "cs_mm": 2.7, "amplitude_contrast": 0.1, "tile_size": 512, "defocus_center_range_angstrom": [15000, 10000], "ast_ratio_center_range": [0.05, 0.1], "ast_angle_center_range_deg": [0, 180], "extra_phase_center_range_deg": [0, 0]}
        self.manifest = {"tool": "gctffind", "binary": ident(self.bin), "source_commit": w.COMMITS["gctffind"], "expected_version": w.VERSIONS["gctffind"], "parameters": self.params, "items": [{"id": "one", "input": ident(self.input), "reference": {"identity": ident(self.ref), "metadata": {k: self.params[k] for k in w.CTF_META}, "differences": ["Different fit algorithms"], "min_defocus_angstrom": 9900, "max_defocus_angstrom": 12100}}]}
        self.man = self.p / "manifest.json"
    def tearDown(self):
        self.tmp.cleanup()
    def save(self):
        self.man.write_text(json.dumps(self.manifest))
    def test_native_evidence_and_comparison(self):
        self.save()
        report = w.run(self.man, self.p / "result")
        item = report["items"][0]
        self.assertEqual(item["difference_angstrom"], {"min_defocus_angstrom": 100, "max_defocus_angstrom": -100})
        self.assertEqual(item["input"]["dimensions"]["shape"], [1, 3, 4])
        self.assertTrue((self.p / "result/one/native.log").is_file())
        self.assertIn("-Defocus", item["command"])
    def test_rejects_hash_mismatch_and_metadata_mismatch(self):
        self.manifest["items"][0]["input"]["sha256"] = "0" * 64
        self.save()
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            w.run(self.man, self.p / "result")
        self.manifest["items"][0]["input"] = ident(self.input)
        self.manifest["items"][0]["reference"]["metadata"]["voltage_kv"] = 300
        self.save()
        with self.assertRaisesRegex(ValueError, "metadata mismatch"):
            w.run(self.man, self.p / "result")
        self.assertFalse((self.p / "result").exists())
    def test_no_success_for_missing_output(self):
        self.bin.write_text("#!/bin/sh\nif [ \"$1\" = --version ]; then echo 'GCtfFind version 1.2.5'; fi\n")
        self.manifest["binary"] = ident(self.bin)
        self.save()
        with self.assertRaises(FileNotFoundError):
            w.run(self.man, self.p / "result")
        self.assertTrue((self.p / "result/one/native.log").exists())
    def test_native_trajectory_frame_continuity(self):
        aln = self.p / "motion.aln"
        aln.write_text("setting\nglobalShift\n stackID 0\n 0 1 2\n 1 4 6\nlocalShift\n")
        star = self.p / "relion.star"
        star.write_text("data_global_shift\nloop_\n_rlnMicrographFrameNumber #1\n 1 0 0\n 2 -3 -4\ndata_local_motion_model\n")
        a = w.trajectory(aln, "globalShift", "localShift")
        b = w.trajectory(star, "data_global_shift", "data_local_motion_model")
        self.assertEqual(w.trajectory_summary(a, 2)["endpoint_displacement_angstrom"], 10)
        self.assertEqual(w.trajectory_summary(b, 2)["endpoint_displacement_angstrom"], 10)
        aln.write_text("globalShift\n0 0 0\n2 1 1\n")
        with self.assertRaisesRegex(ValueError, "discontinuous"):
            w.trajectory(aln, "globalShift", "localShift")

    def test_motion_command_preserves_explicit_inputs(self):
        p = {"input_flag": "-InTiff", "gain": ident(self.input), "gain_rotation": 1, "gain_flip": 2, "gain_inverse": 0, "throw": 0, "trunc": 0, "ftbin": 1, "pixel_size_angstrom": 0.885, "voltage_kv": 200, "frame_dose_e_per_a2": 0, "initial_dose_e_per_a2": 0, "iterations": 5, "tolerance": 0.1, "bfactor": 100, "patch": [0, 0], "group": [1, 1]}
        cmd = w.command("motioncor3", "/tool", "/input.tiff", self.p, p)
        self.assertEqual(cmd[cmd.index("-FmDose") + 1], "0")
        self.assertEqual(cmd[cmd.index("-Patch") + 1:cmd.index("-Patch") + 3], ["0", "0"])
        self.assertEqual(cmd[cmd.index("-Gain") + 1], str(self.input.resolve()))

    def test_public_ctf_example_runs_with_supplied_identities(self):
        root = Path(__file__).resolve().parents[1]
        self.manifest = json.loads((root / "examples/native-tool-comparison/gctffind.json").read_text())
        self.manifest["binary"] = ident(self.bin)
        self.manifest["items"][0]["input"] = ident(self.input)
        self.manifest["items"][0]["reference"]["identity"] = ident(self.ref)
        self.save()
        report = w.run(self.man, self.p / "result")
        self.assertEqual(report["status"], "complete")
        self.assertEqual(len(report["items"]), 1)

    def test_public_motion_example_builds_complete_native_command(self):
        root = Path(__file__).resolve().parents[1]
        example = json.loads((root / "examples/native-tool-comparison/motioncor3.json").read_text())
        params = example["parameters"]
        params["gain"] = ident(self.input)
        cmd = w.command(example["tool"], str(self.bin), "movie.tiff", self.p, params)
        self.assertEqual(cmd[1:3], ["-InTiff", "movie.tiff"])
        self.assertEqual(cmd[cmd.index("-FmDose") + 1], "0")
        self.assertEqual(cmd[cmd.index("-Gain") + 1], str(self.input.resolve()))


if __name__ == "__main__":
    unittest.main()
