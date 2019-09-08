# Data Base Download

### Setting up the environment and Google Drive's API

In here, you can find the tools to download our data base. This is particularly useful when attempting to download the complete data base, with the images (or just when trying to **download the images**).
 
1. To do so, you'll first need to install pyDrive in your python enviroment (further information can be found in: https://pythonhosted.org/PyDrive/). This can be done by running the following command in the pyhton 
terminal:

  ```
    $ pip install PyDrive
  ```

2. After installing pyDrive, you'll need to enable Google Drive's API in your goodgle account, make a project and get your client id and client secret (these can be downloaded in a json file as 'client_secrets.json'). Instructions on how to achieve this can be followed here: https://pythonhosted.org/PyDrive/quickstart.html

3. To avoid errors, and constant authorization checks via browser, you should then make a YAML file called **'settings.yaml'** in your root directory, where the **'client_secrets.json'** should alse be stored. This YAML file should have the following content:

 ```
   client_config_backend: file
   client_config:
     client_id: #your client id should be here
     client_secret: #your client secret should be here

   save_credentials: True
   save_credentials_backend: file
   save_credentials_file: credentials.json

   get_refresh_token: True

   oauth_scope: 
       - https://www.googleapis.com/auth/drive
       - https://www.googleapis.com/auth/drive.install
 ```

Once this is done, you should be able to use the programs in this folder without issues.

### The programs

- **Downloader_pydrive.py**: The program used to download the data base. This can be used to download the synchronized csv files, the zipped images, the features csv files, the camera optical flow files (zipped) and the cameras' features (csv files).

- **pDrive_functions.py**: A file with functions to search and download files, from Google Drive.

- **createFolder**: A function that checks if a needed directory exists, if not, it makes it.

- **Decompressor.py**: A file with functions to decompress zip files. Useful when wokring with Camera#.zip and Camera#_OF.zip


