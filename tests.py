# -*- coding: utf-8 -*-
import os.path
import unittest
import sys

import cprofread
import cprofscan


# *.prof files format depends on python version
if sys.version_info[0] < 3:
    TEST_FILE_PATH_1 = "stats_1_python2.prof"
    TEST_FILE_PATH_2 = "stats_2_python2.prof"
else:
    TEST_FILE_PATH_1 = "stats_1_python3.prof"
    TEST_FILE_PATH_2 = "stats_2_python3.prof"


TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'testfiles')


class CProfReadTest(unittest.TestCase):
    def test_simple_print(self):
        prof_file = os.path.join(TEST_FILES_DIR, TEST_FILE_PATH_1)
        cprofread.main(prof_file)
        cprofread.main(prof_file, 10)


class CProfScanTest(unittest.TestCase):
    def test_simple_run(self):
        prof_file = os.path.join(TEST_FILES_DIR, TEST_FILE_PATH_1)
        cprofscan.main([prof_file])


if __name__ == '__main__':
    unittest.main()
