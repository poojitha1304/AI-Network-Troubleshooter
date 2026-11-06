import unittest
from pathlib import Path

import app
import dashboard.dashboard as dashboard


class TestProjectPaths(unittest.TestCase):
    def test_project_paths_resolve_to_workspace_root(self):
        case_path = Path(app.resolve_project_path("data", "cases.csv"))
        result_path = Path(dashboard.resolve_project_path("results", "responsible_ai_log.csv"))

        self.assertTrue(case_path.exists())
        self.assertTrue(result_path.parent.exists())


if __name__ == "__main__":
    unittest.main()
