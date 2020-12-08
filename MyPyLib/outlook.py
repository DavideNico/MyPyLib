# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 11:39:43 2018

@author: geladar

MS Outlook Python API
This module introduces a class for all mail handling
1. Settign up the outlook API for python scripts
2. Accessing folders, mails
 2.1 with some browsing functionality
3. Drafting emails
4. Sending emails
"""

"""
Modified on Mon Aug 26 2019
@contributor: nicolid

Fixed GetFirst function. It now returns the first email of the folder.
Before it was not properly working because of missing sorting.

Modified on Wed Nov 06 2019
@contributor: nicolid


functions added:
    _get_all_smtp_address
    SentOnBehalfOfName 
    get_emails_from_recipients
    
emails can be sent now from different address. 

Added few examples at the end of the function


"""

# imports
import win32com.client

#%%
class outlook():
    '''
    API for MS Outlook
    '''
    def __init__(self):
        # Outlook Client and Email of Current User
        self._client = win32com.client.Dispatch('Outlook.Application')
        self._namespace = self._client.GetNamespace('MAPI')
        self.user_address = self._namespace.Session.CurrentUser.AddressEntry.GetExchangeUser().PrimarySmtpAddress
        self.root = self._namespace.Folders[self.user_address]
        self.folders = self._all_folders(email_address=None)  
        self.all_addresses=self._get_all_smtp_address()
        self.PR_SMTP_ADDRESS = "http://schemas.microsoft.com/mapi/proptag/0x39FE001E"

    def _get_all_smtp_address(self):
        '''
        Returns a list of all stmp addresses        
        '''
        smtp_addresses=list()
        for smtp_address in self._namespace.Folders:            
            smtp_addresses.append(smtp_address.Name)
        return sorted(smtp_addresses)

    def _get_user_name(self):
        '''
        returns a tuple name and surname of the user by deconstructing their 
        email address
        '''
        name, surname = self.user_address.split('.')[0], self.user_address.split('.')[1].split('@')[0]
        return name, surname
    

    def user_name_surname(self):
        name, surname = self._get_user_name()
        return '{0} {1}'.format(name, surname)
        
    def _all_folders(self,email_address):
        '''
        Return a list of all Outlook folders
        '''
        folders = list()        
        
        def _subfolder(folder):
            '''
            Checks whether folder has subfolders
            If yes, returns a list of subfolders and calls subfolder func for items in list
            If no, returns None
            '''
            
            if folder.Folders:
                folders.append( (folder.Name,folder) )
                for folder in folder.Folders:
                    _subfolder(folder)
            else:
                folders.append( (folder.Name, folder) )
                pass
        if (email_address is None): 
            _subfolder(self.root)
        else:
            _subfolder(self._namespace.Folders[email_address])
    
        return folders
           
    def folder_browser(self, folder_name,email_address=None):
        '''
        return a folder object that matches the folder_name arg
        the default email address where the messages are searched will be the primary address
        defined int he init function (most likely your personal account)
        '''
        if (email_address is None):
            for name, folder in self.folders:
                if folder.Name.lower() in folder_name.lower():
                    return folder
        else:            
            for name, folder in self._all_folders(email_address=email_address):
                if folder.Name.lower() in folder_name.lower():
                    return folder

    def messages(self, folder_name):
        '''
        returns a generator of mails for the specified folder object
        '''
        folder = self.folder_browser(folder_name)
        
        return (i for i in folder.Items)

    def GetFirst(self, folder_name):
        '''
        return the first email in the specified folder
        '''
        folder = self.folder_browser(folder_name).Items
        folder.Sort("[ReceivedTime]",True)
        return folder.GetFirst()
    
    def SentOnBehalfOfName(self,smtpAddress):
        '''
        It checks if the email can be sent with the selected address
        If the address does not exist in your Outlook your personal 
        account will be used
        '''
        SendonBehalfOf=None
        for i in self.all_addresses:
            if (i == smtpAddress):
                SendonBehalfOf=i
        if SendonBehalfOf is not None:
            return SendonBehalfOf
        else:
            return self.user_address
        
    def get_emails_from_recipients(self,messages_in_folder):
        '''
        returns a list of tuples for each recipient in an email
        (emailAddress, Friendly Name) -> ('Benjamin.Franklin@ecb.europa.eu', 'Franklin, Benjamin') 
        
        PR_SMTP_ADDRESS is a static http address defined in the init function  
        
        messages_in_folder is an Items object
        
        '''
        SmtpList = [(recipient.PropertyAccessor.GetProperty(self.PR_SMTP_ADDRESS),recipient.Name) for email in messages_in_folder for recipient in email.Recipients]
        return SmtpList
    
    def draft_mail(self, to='', cc='', subject='', body='', attachments=None, sender=None):
        '''
        wrapper function for drafting emails
        '''
        mail = self._client.CreateItem(0)
        mail.SentOnBehalfOfName=self.SentOnBehalfOfName(sender)
        mail.To = to
        mail.CC = cc
        mail.Subject = subject
        mail.HTMLBody = body
        if attachments is not None:
            mail.Attachments.Add(Source=attachments)
        mail.Display(True)

# End of OutlookApi script
        
#%%
        
#################################
###          EXAMPLES         ###
#################################
        
###################################################################################       
##create the Outlook Object which connect to your outlook and get some information# 
##see __init__ function                                                           #
###################################################################################
#Outlook=outlook()
#
#Outlook.folders
#abo=Outlook._namespace.Folders['mos-support@ecb.int']
#Outlook._all_folders(email_address='mos-support@ecb.int')
######################################
## list of addresses in your Outlook #
######################################
#Outlook.all_addresses
        

#################   
## draft emails #
#################
#Outlook.draft_mail(to='someone',cc='someone',body='HTML body')

################################
##Get first email in a folder ##
################################
#Outlook.GetFirst('Inbox').Subject
#Outlook.GetFirst('Inbox').body
#Outlook.GetFirst('Inbox').To
#Outlook.GetFirst('Inbox').SentOnBehalfOfName
#Outlook.GetFirst('Inbox').HTMLBody
#etc..

#########################################    
##Browse folder. What there is inside? ##
#########################################
#Messages_in_folder=Outlook.folder_browser('Inbox','mos-support@ecb.int').Items
#Messages_in_folder.Sort("[ReceivedTime]",True)
#i=0
#for item in Messages_in_folder:
#    print(item.Subject) #item.body etc..
#    i += 1
#    if i==10:
#        break 

###################################################    
##Get email of recipients for emails in a folder ##
###################################################
#Outlook=outlook()
#
#Messages_in_folder=Outlook.folder_browser('write here the name of the folder').Items
#Messages_in_folder.Sort("[ReceivedTime]",True)
#
#Outlook.get_emails_from_recipients(Messages_in_folder)


