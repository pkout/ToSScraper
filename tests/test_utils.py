import shutil
import tempfile
import unittest
from pathlib import Path

import utils

class TestUtils(unittest.TestCase):

    def test_ensure_creates_dir_creates_dir_if_it_doesnt_exist(self):
        dir_path = Path(tempfile.gettempdir()) / 'test_utils_ensure_dir_exists_ensures_dir_exists'

        if dir_path.exists():
            dir_path.rmdir()

        utils.ensure_dir_exists(dir_path)

        self.assertTrue(dir_path.exists())
        shutil.rmtree(dir_path)

    def test_ensure_creates_dir_does_nothing_if_dir_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            utils.ensure_dir_exists(tmpdir)
            self.assertTrue(Path(tmpdir).exists())