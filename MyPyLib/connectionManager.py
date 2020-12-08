# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 13:48:33 2018

@author: geladar

Title: credentials manager
"""
import winreg

class connectionManager():
    '''
    An API for storing/retrieving passwords and connection settings
    in/from your windows local registry
    '''
    def __init__(self):
        '''
        Opening the root user key handle and storing it in class variable
        called HKEY_CURRENT_USER for use inside this class's operations
        e.g. reading/creating keys/values in a given user's registry
        '''
        self.HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
        self.software = self.openCreateKey(self.HKEY_CURRENT_USER, 'Software')
        self.connectionManager = self.openCreateKey(self.software, 'connectionManager')
            
    def openCreateKey(self, key, sub_key:str):
        '''
        Open registry key with full access rights, if it doesn't exist create it
        called by __init__()
        key     : a winreg key handle object
        sub_key : a string for the name of the key to open/create
        '''
        try:
            return winreg.OpenKey(key, sub_key, access=winreg.KEY_ALL_ACCESS)
        except Exception as e:
            print('created {}'.format(sub_key))
            return winreg.CreateKey(key, sub_key)       
 
    def connections(self):
        '''
        Returns a dictionary of connection names and their keys
        '''
        numConns = winreg.QueryInfoKey(self.connectionManager)[0]
        if numConns > 0:
            values = [winreg.EnumKey(self.connectionManager, i) for i in range(numConns)]
            return {i: self.openCreateKey(self.connectionManager, i) for i in values}
        else:
            print('There are no connections stored, store a new one')
            self.create_connection()
            
    def openConnection(self, key):
        '''
        Returns a connection string
        key     : a winreg key handle object        
        '''
        numValues = winreg.QueryInfoKey(key)[1]
        values = {winreg.EnumValue(key, i)[0]: winreg.EnumValue(key, i)[1] for i in range(numValues)}
        return '{}/{}@{}:{}/{}'.format(values['username'], values['password'], values['ip'], values['port'], values['service'])        
            
    def create_connection(self):
        '''
        Creates and stores a new connection in registry
        '''
        val_nms = ['connection_name', 'username', 'password', 'ip', 'service', 'port']
        conn = {val_nm: input('Enter {}:\n'.format(val_nm)) for val_nm in val_nms}
        key = self.openCreateKey(self.connectionManager, conn['connection_name'])
        for value_name, value in conn.items():
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value)