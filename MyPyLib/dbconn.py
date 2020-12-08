# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 17:15:54 2018

@author: geladar

MOPDB Python API
"""
import cx_Oracle, winreg, os
import re
import pkgutil
#%%


class dbconn:
    '''
    API for DB connections in Python
    '''

    def __init__(self,database_name="MOPDB"):	    
        self.db_name = database_name
        #self._creds = self.__user_credentials() #Tuple of (user, pass)
        self.conn = self.__establish_connection()

    def __HKEY_PATH(self):
        return r'Software\ECB\FRO'

    def __TNS(self):        
        tns_object = tns()
        connection_string = tns_object.get_connection_string(self.db_name)
        return connection_string
		
    def __user_credentials(self):
        '''
        Retrieve MOPDB username and password from registry
        Asks user for credentials if not found in registry
        '''
        HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER        
        try:
            FRO = winreg.OpenKey(HKEY_CURRENT_USER, self.__HKEY_PATH())
        except FileNotFoundError:
            self.__create_registry()
        try:    
            db_user = winreg.QueryValue(FRO, self.db_name + 'User')
            db_pass = winreg.QueryValue(FRO, self.db_name + 'Pass')
        except FileNotFoundError:
            self.__create_credentials()
            db_user = winreg.QueryValue(FRO, self.db_name + 'User')
            db_pass = winreg.QueryValue(FRO, self.db_name + 'Pass')
            print('')
            print('User and Password are now saved.')
        return db_user, db_pass

    def __create_registry(self):
        HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
        winreg.CreateKey(HKEY_CURRENT_USER, self.__HKEY_PATH())
        self.__user_credentials()
    
    def __create_credentials(self):
        print('Please provide your credentials to connect to {0}'.format(self.db_name))
        db_user = input('Please type your username:\n')
        db_pass = input('Please type your password:\n')
        HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER        
        FRO = winreg.OpenKey(HKEY_CURRENT_USER, self.__HKEY_PATH())
        # to be implemented:
        #  ask user whether credentials, i.e. password, can be stored in user's registry
        winreg.SetValue(FRO, self.db_name + 'User', winreg.REG_SZ , db_user)
        winreg.SetValue(FRO, self.db_name + 'Pass', winreg.REG_SZ , db_pass)
        self.__user_credentials()
        
        
    def __establish_connection(self):
        #this ensures that credentials are not manipulated during runtime:
        _creds = self.__user_credentials() 
        try:
            tc = cx_Oracle.connect(user=_creds[0], password=_creds[1], dsn=self.db_name)
        except  cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 1017:
                print("Warning: ORA-01017: invalid username/password for '{0}', user: '{1}'".format(self.db_name,_creds[0]))
                retry = input('Would you like to update your credentials? (y/N)\n').lower() == 'y'
                if retry == True:
                    self.__create_credentials()
                    return self.__establish_connection()
                else:
                    raise Exception("Error: ORA-01017: invalid username/password; logon denied for user '{0}' on '{1}'".format(_creds[0],self.db_name))
            else:
                raise Exception('Error: Database connection error: {0}'.format(e))
        return tc
    




class tns():
 
    def __init__(self):	    
        # statics
        self.__filepath_tns = os.path.join(os.path.dirname(self.__find_TNS_paths()[0]),'network\\admin\\tnsnames.ora')
        # Regex matches
        self.__tns_name = '^(.+?)\s?\=\s+\(DESCRIPTION.*'
        self.__tns_host = '.*?HOST\s?=\s?(.+?)\)'
        self.__tns_port = '.*?PORT\s?=\s?(\d+?)\)'
        self.__tns_sname = '.*?SERVICE_NAME\s?=\s?(.+?)\)'
        self.__tns_sid = '.*?SID\s?=\s?(.+?)\)'
        #init
        self.__easy_connects = []
        self.__extract_tns()
        
    def __find_TNS_paths(self):
        paths=[] 
        for p in os.environ['PATH'].split(os.pathsep):
            SearchObj=re.search('.*[0-9]+\.+[0-9]*?',p)
            if ('oracle' in p.lower() and SearchObj)  :
                paths.append(p)
        return paths

    def __find_match(self,tns_regex, y):
        x1 = re.match(tns_regex, y, re.M + re.I + re.S)
        if x1 is not None:
            x1 = x1.groups(1)[0] # Only first match is returned
            x1 = x1.strip('\n')
        return(x1)

    def get_all_tns(self):
        return self.__easy_connects
    
    def get_connection_string(self, tns_name="MOPDB"):
        db_tns = self.get_tns_by_name(tns_name)
        db_tns = db_tns[0] #only first entry is used
        #following provides the connection string in format 
        # host:port/service_name
        # e.g. mopdb-db.zonelog.unix.ecb.de:1521/mopdb.prd.tns
        connection_string = '{0}:{1}/{2}'.format(db_tns['host'], db_tns['port'], db_tns['service_name'])
        #print('returning connection string:',connection_string)
        return connection_string
    
    def get_tns_by_name(self, needle_name="MOPDB"):
        #print("TNS requested for '{0}'".format(needle_name))
        #retrieve all TNS items
        all_tns = self.get_all_tns()
        #filter for the specified TNS name
        specific_tns = list(filter(lambda all_tns: all_tns['name'].upper() == needle_name.upper(), all_tns))
        if len(specific_tns)==0:
            raise Exception("No connection found for database called: '{0}'".format(needle_name))
        #print("TNS found. Number of matches: {0}".format(len(specific_tns)))
        specific_tns = specific_tns[:1] #keeps only the first element that was found
        #return only matching TNS
        #print ("returning TNS:" ,specific_tns)
        return specific_tns
    
    def print_all_tns(self):
        print(self.get_all_tns())
    
    def __clean_tns_file(self):
        # Removing commented text
        tns_file = ''
        try:
            # try to read tnsnames.orac in Oracle folders
            tns_file = open(self.__filepath_tns, 'r').read()
        except (OSError, FileNotFoundError) as e:
            print(e)
            print("Warning: no tnsnames.ora file found - falling back on package resource 'templates/general_tns.ora'")
            
        tns_file_rsc = pkgutil.get_data('py_dgm', 'templates/general_tns.ora')
        tns_file = tns_file + tns_file_rsc.decode()
        
        tns_file = tns_file.splitlines() # splits at \r, \n, and \r\n
        
        # remove all comment lines from TNS file content
        for line in tns_file:
            if line.startswith('#'):
                 tns_file.remove(line)
                 
        self.__tns_file = tns_file
    
    def __extract_tns(self):
        self.__clean_tns_file()
        
        tnsnames = '\n'.join(self.__tns_file)
        tnsnames1 = re.split(r"(\s*\)\s*\n){3,}(\s*\n)+", tnsnames)
            
        for y in tnsnames1:
            y = '%s))' % y
            l = [self.__find_match(x, y) for x in [self.__tns_name,  self.__tns_host,  self.__tns_port,  self.__tns_sname,  self.__tns_sid  ] ]
            if l[0] == None:
                next
            else:
                d = {'name': l[0],
                    'host': l[1],
                    'port': l[2],
                    'service_name': l[3],
                    'sid': l[4]}
                self.__easy_connects.append(d)



#end of TNS class


#%%
if __name__ == '__main__':
    mopdb = dbconn("coll_shared")
    print(mopdb.db_name)
#%%
