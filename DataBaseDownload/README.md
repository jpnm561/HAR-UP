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


## Instructions

To download our data base, you will need these programs in the same path (if you don't wan't to make changes in the code). You should start by opening the **Downloader_pydrive.py** program and use it to select which files, subjects, activities and trials you wish to download.

In the following sections, you'll find a more detailed explanation of how to use the available funcitons and what to expect from them.

## Directory arrangement

Our downloader arranges the downloaded files in the following manner:

    downloader(path)

  Outputs:

    ParentFolder\Subject#\Activity#\Trial#\Subject#Activity#Trial#.csv


### Data Set



### Features



#### Choosing a time window

By default, features are calculated for three time windows:

- 1&0.5

- 2&1

- 3&1.5

These time windows can be altered when calling the function **downloadFeatures()**. In the following line there's an example showing how to call the function to get features for two windows: 1 second windows, taken every 0.5 seconds; and 2 second windows taken every second.


    downloadFeatures(path,t_window = ['1&0.5','2&1'])


This will result in:


    ParentFolder\Subject#\Activity#\Trial#\Subject#Activity#Trial#Features1&0.5.csv
                                          \Subject#Activity#Trial#Features2&1.csv


## Choosing subjects, activities and trials

By default, features are taken for **17 subjects**, each with **11 activities** and **3 trials** per activity. These numbers can be modified in the function's input. It is important to note that the program is built in a way that only allows to call these objects in order, so for example, if you wanted to get the features of subjects 1, 2, 3, 7, 10 and 11 you would have to call three times the function, and specifiy that you don't want a single output file (because this would erase the previous outputs).


    extraction(d_base_path,features_path, n_sub=[1,3], single_f=False)
    extraction(d_base_path,features_path, n_sub=[7,7], single_f=False)
    extraction(d_base_path,features_path, n_sub=[10,11], single_f=False)
    

To recap:


  For subjetcts:
  
    n_sub = [start, end] 


  For activities:
  
    n_act = [start, end]


  For trials:
  
    n_trl = [start, end]

It should be noted that **start** and **end** both refer to integer numbers.

