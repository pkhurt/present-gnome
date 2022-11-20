import unittest
import main
from io import StringIO
from csv import reader  # this should import your custom parser instead

class GnomeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.in_mem_csv = StringIO("""\
        name1, nameadress1
        name2, nameadress2
        name3, nameadress3
        name4, nameadress4""")  # in python 2.7, put a 'u' before the test string
        self.test_reader = reader(self.in_mem_csv, delimiter=',', quotechar='|')

    def test_read_csv(self):
        name_list = main.read_csv(self.in_mem_csv)

        self.assertTrue(type(name_list) == list)
        self.assertEqual(len(name_list), 4)

    def test_sanity_check_names(self):
        name_list = main.read_csv(self.in_mem_csv)
        self.assertTrue(main.sanity_check_names(name_list))

    def test_get_random_letter(self):
        self.assertTrue(type(main.get_random_letter()), str)


if __name__ == '__main__':
    unittest.main()
