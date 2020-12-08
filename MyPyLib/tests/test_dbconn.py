
print("\n#\n# testing module dbconn ...")
print("\n")

import moalib
import unittest
import pandas as pd

global verbosity
verbosity=0

#construct expected output
d = {'EXAMPLE' : pd.Series(['it works'], index=[0])}
sql_df = pd.DataFrame(d)


mopdb = moalib.dbconn()



class test_dbconn(unittest.TestCase):
    
    def test_mopdb_query(self):
        global verbosity
        if verbosity>=2:
            print("test_mopdb_query")
        global sql_df
        sql_query="select 'it works' as example from dual"
        #run query on MOPDB, store in a pandas object and print output in console
        actual = pd.read_sql(sql_query,mopdb.conn)
        expected = sql_df
        # test that MOPDB TNS is as expected
        self.assertEqual(actual['EXAMPLE'][0], expected['EXAMPLE'][0])
    
    
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
