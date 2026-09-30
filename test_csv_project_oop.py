import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


class CSVProjectOOPTests(unittest.TestCase):
    def test_csv_loader_uses_script_directory_for_relative_paths(self):
        project_dir = Path(__file__).resolve().parent

        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            try:
                spec = importlib.util.spec_from_file_location("csv_project_oop", project_dir / "csv_project_oop.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                analyzer = module.CSVAnalyzer("employees.csv")
                self.assertTrue(analyzer.load())
                self.assertIsNotNone(analyzer.data)
            finally:
                os.chdir(project_dir)


if __name__ == "__main__":
    unittest.main()
