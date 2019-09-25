# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 18:39:11 2019
@author: José Pablo
"""

#Requires
#pip install PyDrive
#Having the pDrive_functions.py file nearby

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pDrive_functions import fileFinder, fileDownloader
from createFolder import createFolder


"""
*******************************************************************************
Functions
*******************************************************************************
"""

#A function to connect with Google Drive
def connect():
    gauth = GoogleAuth()
    #Creates local webserver and auto handles authentication.
    gauth.LocalWebserverAuth()
    #Reads stored credentials (if any) to avoid opening the browser
    gauth.LoadCredentialsFile('credentials.json')
    drive = GoogleDrive(gauth)  
    return gauth, drive

#A function to generate, refresh or authenticate Google Drive credentials
def refresh_gauth(gauth, drive):
    flg = False
    try:
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        gauth.SaveCredentialsFile()
        drive = GoogleDrive(gauth)
    except Exception as e:
        print('An error ocurred: ' + str(e))
        flg = True
    return gauth, drive, flg

#A function that handles downloads
def download(path,f_name,p_id,gauth,drive):
    gauth, drive, v_flg = refresh_gauth(gauth,drive)
    if v_flg:
        return gauth, drive, True
    f_id = fileFinder(f_name,p_id,drive)
    gauth, drive, v_num = refresh_gauth(gauth,drive)
    if v_flg:
        return gauth, drive, True
    print('--------Downloading:' + f_name)
    fileDownloader(f_name,f_id,path,drive)
    print('----------Download complete')
    return gauth, drive, False

#A function to handle feature downloads
def featureDownload(gral = '',
                     n_sub=[1,11],
                     n_act=[1,11],
                     n_trl=[1,3],
                     t_window=['1&0.5','2&1','3&1.5'],
                     csv_files=True,
                     cameras=True,
                     feat_cam_OF=True,
                     Complete_OF=False,
                     n_cam=[1,2]):      
    gauth, drive = connect()
    #A flag to ensure that a connection with Google Drive is made
    v_flg = False
    for i in range(n_sub[0],n_sub[1] + 1):
        sub = 'Subject' + str(i)
        print('--'+sub)
        for j in range(n_act[0],n_act[1] + 1):
            act = 'Activity' + str(j)
            print('S'+str(i)+'--'+act)
            for k in range(n_trl[0],n_trl[1] + 1):
                trl = 'Trial' + str(k)
                print('S'+str(i)+'-A'+str(j)+'--'+trl)
                path = gral + '//' + sub + '//' + act + '//' + trl + '//'
                createFolder(path)
                #Resized camera OF csv
                if cameras:
                    f_name = 'CameraFeatures'+sub+act+trl+'.csv'
                    gauth, drive, v_flg = refresh_gauth(gauth,drive)
                    if v_flg:
                        break
                    s_id = fileFinder(sub,'1XDJELfyqXSgjQg-z-s5MHG_YxsSZO5vS',drive)
                    a_id = fileFinder(act,s_id,drive)
                    gauth, drive, v_flg = download(path,f_name,a_id,gauth, drive)
                #Camera OF zip files
                if Complete_OF:
                    for l in range(n_cam[0],n_cam[1]+1):
                        f_name = sub+act+trl+'Camera'+str(l)+'_OF.zip'
                        gauth, drive, v_flg = refresh_gauth(gauth,drive)
                        if v_flg:
                            break
                        s_id = fileFinder(sub,'1ogVoukp6eEW7Chxo8LdV0vrpwEla5vAS',drive)
                        a_id = fileFinder(act,s_id,drive)
                        t_id = fileFinder(trl,a_id,drive)
                        gauth, drive, v_flg = download(path,f_name,t_id,gauth, drive)
                for twnd in t_window:
                    #Feature download (IMU Thinkgear IR) csv
                    if csv_files:
                        f_name = sub+act+trl + 'Features' + twnd + '.csv'
                        gauth, drive, v_flg = refresh_gauth(gauth,drive)
                        if v_flg:
                            break
                        s_id = fileFinder(sub,'1ogVoukp6eEW7Chxo8LdV0vrpwEla5vAS',drive)
                        a_id = fileFinder(act,s_id,drive)
                        t_id = fileFinder(trl,a_id,drive)
                        gauth, drive, v_flg = download(path,f_name,t_id,gauth, drive)
                    #Resized camera OF features (mean) csv
                    if feat_cam_OF:
                        f_name = sub+act+trl+'CameraFeatures'+twnd+'.csv'
                        gauth, drive, v_flg = refresh_gauth(gauth,drive)
                        if v_flg:
                            break
                        tw_id = fileFinder(twnd,'1LvrbxYHc-DXfxOvqWpC62bMg0uOytSNj',drive)
                        s_id = fileFinder(sub,tw_id,drive)
                        a_id = fileFinder(act,s_id,drive)
                        gauth, drive, v_flg = download(path,f_name,a_id,gauth, drive) 
    if v_flg:
        print('An error ocurred while connecting to Google Drive')

def dataBaseDownload(gral = '',
                     n_sub=[1,11],
                     n_act=[1,11],
                     n_trl=[1,3],
                     csv_files=True,
                     cameras=True,
                     n_cam=[1,2]):
    gauth, drive = connect()
    v_flg = False
    #parent folder´s id
    p_id = '1AItqj3Ue-iv7NSdR7Qta1Ez4spRjCo58'
    for i in range(n_sub[0],n_sub[1] + 1):
        sub = 'Subject' + str(i)
        print('--'+sub)
        gauth, drive, v_flg = refresh_gauth(gauth,drive)
        if v_flg:
            break
        s_id = fileFinder(sub,p_id,drive)
        if s_id == '':
            print('The folder "' + sub +'" could not be found!')
            v_flg = True
            break
        for j in range(n_act[0],n_act[1] + 1):
            act = 'Activity' + str(j)
            print('S'+str(i)+'--'+act)
            gauth, drive, v_flg = refresh_gauth(gauth,drive)
            if v_flg:
                break
            a_id = fileFinder(act,s_id,drive)
            for k in range(n_trl[0],n_trl[1] + 1):
                if v_flg:
                    break
                trl = 'Trial' + str(k)
                print('S'+str(i)+'-A'+str(j)+'--'+trl)
                path = gral + '//' + sub + '//' + act + '//' + trl + '//'
                createFolder(path)
                f_name = sub+act+trl + '.csv'
                gauth, drive, v_flg = refresh_gauth(gauth,drive)
                t_id = fileFinder(trl,a_id,drive)
                if v_flg:
                    break
                gauth, drive, v_flg = download(path,f_name,t_id,gauth, drive)
                if(cameras):
                    for l in range(n_cam[0],n_cam[1] + 1):
                        cam = 'Camera' + str(l)
                        f_name = sub+act+trl+cam+'.zip'
                        gauth, drive, v_flg = download(path,f_name,t_id,gauth, drive)
    if v_flg:
        print('An error ocurred while connecting to Google Drive')

"""
*******************************************************************************
End of functions
*******************************************************************************
"""

def main():
    parent_dir = ''
    dataBaseDownload(parent_dir)
    featureDownload(parent_dir)
    
if __name__=="__main__":
    main()
