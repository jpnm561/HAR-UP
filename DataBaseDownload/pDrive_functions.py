# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 18:39:11 2019

@author: José Pablo
"""

#A function that gets a document's (or folder's) drive id
#f_name : file name, p_id : parent id, drive : drive object being used
def fileFinder(f_name, p_id, drive):
    f_id = ''
    file_list = drive.ListFile({'q': "'" + p_id +"' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['title'] == f_name:
            f_id = file['id']
            break
    return f_id
#end of fileFinder

#A function that Downloads files from Google Drive
#f_name : file name, f_id : file id, path : directory in which to save the file, drive : the drive object being used
def fileDownloader(f_name, f_id, path, drive):
    file_d = drive.CreateFile({'id': f_id})
    file_d.GetContentFile(path + f_name)    
#end of fileDownloader
