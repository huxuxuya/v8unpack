import os
import sys
import unittest

sys.path.append("../../src/")
from v8unpack.container_reader import extract as container_extract, decompress_and_extract
from v8unpack.decoder import decode
from v8unpack.file_organizer import FileOrganizer


class TestFileOrganizerCE(unittest.TestCase):
    def setUp(self) -> None:
        self.current_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.current_dir, 'data')
        self.temp_dir = os.path.join(self.data_dir, 'temp')

    def test_extract(self):
        src_filename = os.path.join(self.data_dir, 'apam_add_ws_old.cf')
        dest_dir0 = os.path.join(self.temp_dir, 'apam-ws-0')
        dest_dir1 = os.path.join(self.temp_dir, 'apam-ws-1')
        dest_dir2 = os.path.join(self.temp_dir, 'apam-ws-2')
        dest_dir3 = os.path.join(self.temp_dir, 'apam-ws-3')
        container_extract(src_filename, dest_dir0, False, False)
        decompress_and_extract(dest_dir0, dest_dir1)
        decode(dest_dir1, dest_dir2)
        FileOrganizer.pack(dest_dir2, dest_dir3)


