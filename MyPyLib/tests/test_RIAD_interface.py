
print("\n#\n# testing module RIAD_interface ...")
print("\n")

import moalib
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal

global verbosity
verbosity=0


    

class test_riad_interface(unittest.TestCase):
    
    def setUp(self):
        global args, kwargs
        self.args=['IT0000101247669',None,None]
        
        self.kwargs={}
        self.kwargs['RIAD_NAME'] = self.args[1]
        self.kwargs['RIAD_CODE'] = self.args[0]
        self.kwargs['RIAD_OUID'] = self.args[2]
        
        test_data = pd.DataFrame({'OUID':[6232],
                                 'RIAD_CODE':['IT0000101247669'],
                                 'RIAD_NAME':['BARCLAYS BANK PLC'],
                                 'COUNTRY':['IT'],
                                 'ESA_SECTOR':['S125'],
                                 'ESA_SECTOR_DETAILED':['S125_I'],
                                 'COLLATERALGROUP':['IG4'],
                                 'CSPP_ASSSSMNT':[None],
                                 })
        
        fixed_order = ['OUID', 'RIAD_CODE', 'RIAD_NAME', 'COUNTRY', 'ESA_SECTOR', 'ESA_SECTOR_DETAILED', 'COLLATERALGROUP', 'CSPP_ASSSSMNT']
        test_data = test_data[fixed_order]
        
        self.expected_entty = test_data
        
    
    def test_get_riad_entity(self):
        global verbosity
        if verbosity>=2:
            print("test_get_riad_entity")
        
        actual_data = moalib.get_entity_by_kwargs(**self.kwargs)
        assert_frame_equal(actual_data, self.expected_entty)
    
    
    def test_get_entity_by_name(self):
        global verbosity
        if verbosity>=2:
            print("test_get_entity_by_name")
        
        actual_data = moalib.get_entity_by_name('BARCLAYS BANK PLC')
        actual_data = actual_data[actual_data['RIAD_CODE']=='IT0000101247669'].reset_index(drop=True)
        assert_frame_equal(actual_data, self.expected_entty)
        
        
    def test_get_riad_group_by_riad_code(self):
        global verbosity
        if verbosity>=2:
            print("test_get_riad_group_by_riad_code")
        
        actual_data_ = moalib.get_riad_group_by_riad_code('DE00001')
        actual_data = actual_data_['GH_RIAD_CODE'].iloc[1]
        self.assertEqual(actual_data,  'DE00001')
    
    
        
if __name__ == '__main__':
    
    unittest.main(verbosity=2)
