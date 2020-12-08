# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 11:43:57 2019

@author: nicolid
"""

from moalib import DarwinAPI
import pandas as pd
from io import BytesIO

#### How to use it ####

#the following website explains how the API works
#https://developer.opentext.com/webaccess/#url=%2Fawd%2Fresources%2Farticles%2F6102%2Fcontent%2Bserver%2Brest%2Bapi%2B%2Bquick%2Bstart%2Bguide%23TOC_3&tab=501      
       
#create object    
Dw = DarwinAPI.Darwin()   

#example get contents of a folder
contents_of_folder=Dw.json_to_DF(Dw.folder_get_items('197219060'))
        

#example get metadata of items
attributes_raw=Dw.get_file_attributes('249140043')
attributes_raw.headers 
#example
attributes_raw.headers['Content-Type']
additional_attributes=Dw.json_to_DF(Dw.get_file_attributes('249140043'))
additional_attributes['name'][0]
#example get mime type of item
MimeType=Dw.get_mime_type(Dw.get_file_content('249140043'))


#example - open Excel
workbook=Dw.open_excel(Dw.get_file_content('249140043'))
data=workbook.worksheets[0].values
cols=next(data)[:]
DF=pd.DataFrame(data,columns=cols)

workbook=Dw.open_excel(Dw.get_file_content('245303711'))
file=Dw.get_file_content('245303711')
file.text
fp=BytesIO(file.content)


contents_of_folder=Dw.json_to_DF(Dw.folder_get_items('245247671'))
#example - open sql, html, txt
sql=Dw.get_file_content(contents_of_folder['id'][0]).text
html=Dw.get_file_content(contents_of_folder['id'][2]).text

