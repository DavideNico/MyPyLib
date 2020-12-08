
print("\n#\n# testing module tns ...")
print("\n")

import moalib
import unittest

global verbosity
verbosity=0

tnso = moalib.tns()
tnso.get_tns_by_name

test_data = [{'name': 'MOPDB', 'host': 'mopdb-db.zonelog.unix.ecb.de', 'port': '1521', 'service_name': 'mopdb.prd.tns', 'sid': None}]
    

class test_tns(unittest.TestCase):
    
    def test_mopdb_tns(self):
        global verbosity
        if verbosity>=2:
            print("test_mopdb_tns")
        # test that MOPDB TNS is as expected
        self.assertEqual(tnso.get_tns_by_name("MOPDB"), test_data)
        # test that default TNS is the same as MOPDB TNS
        self.assertEqual(tnso.get_tns_by_name(), test_data)
        # test that default TNS is the same as MOPDB TNS
        self.assertEqual(tnso.get_tns_by_name(), tnso.get_tns_by_name("MOPDB"))
    
    def test_notfound_dbname(self):
        global verbosity
        if verbosity>=2:
            print("test_notfound_dbname")
        with self.assertRaises(Exception):
            tnso.get_tns_by_name("jibberish")
    
    def test_mopdb_connection_string(self):
        global verbosity
        if verbosity>=2:
            print("test_mopdb_connection_string")
        expected_out = test_data[0]['host'] + ":" + test_data[0]['port'] + "/" + test_data[0]['service_name']
        self.assertEqual(tnso.get_connection_string("MOPDB"), expected_out)
        self.assertEqual(tnso.get_connection_string(), expected_out)

    def test_nonempty_tns_files(self):
        global verbosity
        if verbosity>=2:
            print("test_nonempty_tns_files")
        self.assertNotEqual(tnso.get_all_tns(), [])
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
