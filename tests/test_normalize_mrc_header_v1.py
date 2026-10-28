"""Header repair must preserve native evidence and every scientific data byte."""
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/cryocore/normalize_mrc_header_v1.py"
SPEC = importlib.util.spec_from_file_location("normalize_mrc_header_v1", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

try:
    import mrcfile
    import numpy as np
except ImportError:
    mrcfile = None
    np = None


@unittest.skipIf(mrcfile is None, "Optional scientific environment requires mrcfile and numpy")
class NormalizeMrcHeaderTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.native = self.root / "native.mrc"
        self.output = self.root / "native.header-normalized.mrc"
        with mrcfile.new(self.native, overwrite=False) as mrc:
            mrc.set_data(np.arange(120, dtype=np.float32).reshape(10, 12) / 7 - 2)
            mrc.voxel_size = .885
            mrc.header.label[0] = b"Preserve this native provenance label"
            mrc.header.nlabl = 1
        raw = bytearray(self.native.read_bytes())
        raw[208:212] = b"MAP\0"
        raw[76:88] = struct.pack("<3f", 0, 0, 0)
        raw[216:220] = struct.pack("<f", 0)
        self.native.write_bytes(raw)
        self.original = bytes(raw)

    def test_repair_passes_full_validation_and_preserves_payload_and_metadata(self):
        receipt = MODULE.normalize_mrc_header(self.native, self.output)
        repaired = self.output.read_bytes()
        self.assertEqual(self.native.read_bytes(), self.original)
        self.assertEqual(repaired[1024:], self.original[1024:])
        self.assertEqual(repaired[208:212], b"MAP ")
        allowed = set(range(76, 88)) | set(range(208, 212)) | set(range(216, 220))
        changed = {i for i, (a, b) in enumerate(zip(self.original, repaired)) if a != b}
        self.assertTrue(changed)
        self.assertTrue(changed <= allowed)
        self.assertEqual(receipt["input_pixel_payload_sha256"],
                         receipt["output_pixel_payload_sha256"])
        self.assertEqual(receipt["input"]["sha256"], MODULE.digest(self.native))
        self.assertFalse(receipt["native_full_validation"]["passed"])
        self.assertTrue(receipt["derivative_full_validation"]["passed"])
        self.assertTrue(mrcfile.validate(self.output, print_file=__import__("io").StringIO()))
        with mrcfile.open(self.output, mode="r", permissive=False) as mrc:
            expected = np.frombuffer(self.original, dtype="<f4", offset=1024).reshape(10, 12)
            np.testing.assert_array_equal(mrc.data, expected)
            self.assertAlmostEqual(float(mrc.voxel_size.x), .885, places=6)
            self.assertAlmostEqual(float(mrc.header.rms), float(expected.std()), places=6)
            self.assertEqual(bytes(mrc.header.label[0]), b"Preserve this native provenance label")

    def test_existing_output_is_never_overwritten(self):
        self.output.write_bytes(b"preserved existing derivative")
        with self.assertRaises(FileExistsError):
            MODULE.normalize_mrc_header(self.native, self.output)
        self.assertEqual(self.output.read_bytes(), b"preserved existing derivative")
        self.assertEqual(self.native.read_bytes(), self.original)

    def test_same_path_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "separate, fresh"):
            MODULE.normalize_mrc_header(self.native, self.native)
        self.assertEqual(self.native.read_bytes(), self.original)

    def test_unrelated_format_defect_does_not_escape_as_repaired_output(self):
        raw = bytearray(self.original)
        raw[64:76] = struct.pack("<3i", 0, 0, 0)
        self.native.write_bytes(raw)
        before = self.native.read_bytes()
        with self.assertRaisesRegex(ValueError, "full MRC validation"):
            MODULE.normalize_mrc_header(self.native, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.native.read_bytes(), before)

    def test_unapproved_header_mutation_is_detected(self):
        original_method = mrcfile.mrcobject.MrcObject.update_header_stats

        def mutate_header(mrc):
            original_method(mrc)
            mrc.header.cella.x = 999

        with mock.patch.object(mrcfile.mrcobject.MrcObject, "update_header_stats", mutate_header):
            with self.assertRaisesRegex(ValueError, "Unapproved header change"):
                MODULE.normalize_mrc_header(self.native, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.native.read_bytes(), self.original)

    def test_pixel_mutation_is_detected(self):
        original_method = mrcfile.mrcobject.MrcObject.update_header_stats

        def mutate_pixels(mrc):
            mrc.data[0, 0] += 1
            original_method(mrc)

        with mock.patch.object(mrcfile.mrcobject.MrcObject, "update_header_stats", mutate_pixels):
            with self.assertRaisesRegex(ValueError, "pixel payload"):
                MODULE.normalize_mrc_header(self.native, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.native.read_bytes(), self.original)


if __name__ == "__main__":
    unittest.main()
