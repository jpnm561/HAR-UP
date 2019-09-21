# Data Base Download

## Setting up the environment and Google Drive's API

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


## The programs

- **Downloader_pydrive.py**: The program used to download the data base. This can be used to download the synchronized csv files, the zipped images, the features csv files, the camera optical flow files (zipped) and the cameras' features (csv files).

- **pDrive_functions.py**: A file with functions to search and download files, from Google Drive.

- **createFolder**: A function that checks if a needed directory exists, if not, it makes it.

- **Decompressor.py**: A file with functions to decompress zip files. Useful when wokring with Camera#.zip and Camera#_OF.zip


## Instructions

To download our data base, you will need these programs in the same path (if you don't wan't to make changes in the code). You should start by opening the **Downloader_pydrive.py** program and use it to select which files, subjects, activities and trials you wish to download.

In the following sections, you'll find a more detailed explanation of how to use the available funcitons and what to expect from them.

## Directory arrangement

Our downloader arranges the downloaded files in the following manner:

    path = 'ParentFolder//'
    
    dataBaseDownload(path)
    featureDownload(path)

  Outputs:

    ParentFolder\
                \Subject#\
                         \Activity#\
                                   \Trial#\
                                          \downloadedFile(1)
                                          ...
                                          \donwnloadedFile(i)

## Choosing which files to download

### Choosing subjects, activities and trials

By default, downloads are done for the **17 subjects**, each with **11 activities** and **3 trials** per activity. However, the number of subjects, activities and trials you wish to download can be modified when calling the **dataBaseDownload** and **featureDownload** functions. It is important to note that the program is built in a way that only allows to call these objects in order, so for example, if you wanted to get the data set for subjects 1, 2, 3, 7, 10 and 11 you would have to call three times the function:


    dataBaseDownload(path, n_sub=[1,3])
    dataBaseDownload(path, n_sub=[7,7])
    dataBaseDownload(path, n_sub=[10,11])


To make changes, you can modify...


  ...for subjetcts:
  
    n_sub = [start, end] 


  ...for activities:
  
    n_act = [start, end]


  ...for trials:
  
    n_trl = [start, end]

It should be noted that **start** and **end** both refer to integer numbers.

### Downloading the Data Set

With our downloader, you'll be able to choose which elements from our data set to download. These all have synchonized timestamps and are tagged, showing which activity is happening for every timestamp. The data set can be separated in:

- csv files containing sensor data from 5 IMUs, an ECG and 6 infrared.

- zip files containing picture-frames from recorded video, from two cameras (side and front view).


By default, all csv and zip files (from both cameras) are downloaded. However, you can modify this when calling the **dataBaseDownload** function.

#### Example

- Default download

      dataBaseDownload('ParentFolder//')

  Outputs:

      ParentFolder\
                  \Subject#\
                           \Activity$\
                                     \Trial%\
                                            \Subject#Activity$Trial%.csv
                                            \Subject#Activity$Trial%Camera1.zip
                                            \Subject#Activity$Trial%Camera2.zip

- Avoiding csv files

 Running the next line would indicate that no csv files are to be downloaded, and only the zipped images would be downloaded. 
 
      dataBaseDownload('ParentFolder//', csv_files = False)

  Outputs:

      ParentFolder\
                  \Subject#\
                           \Activity$\
                                     \Trial%\
                                            \Subject#Activity$Trial%Camera1.zip
                                            \Subject#Activity$Trial%Camera2.zip

 - Avoiding images

  If you don't want to download any images, the function can be called as:

      dataBaseDownload('ParentFolder//', cameras = False)


 - Choosing a camera
 
  Or if you only want to download one of the camera's you can input:

   - - For Camera 1 (side view):
  ``` 
          dataBaseDownload(csv_files=False, n_cam=[1,1])
  ```  
   - - For Camera 2 (front view):
   ```
          dataBaseDownload(csv_files=False, n_cam=[2,2])
   ```

### Downloading Features

When using this program, you can select which feature elements to download. These all have synchonized timestamps, a tag indicating the current activity (per timestamp). The feature data set can be separated in:

- csv files containing features from the sensor data (5 IMUs, an ECG and 6 infrared) taken in different time-windows. These can be found for 1 second windows taken every 0.5 seconds, 2 second windows taken every second, and 3 second windows taken every 1.5 seconds.

- csv files containing optical flow files (for both cameras in a single file) that have been resized to a 20x20 pixel size.

- csv files containig the mean (a single feature) taken from the resized OF camera files in different time-windows. These can be found for 1 second windows taken every 0.5 seconds, 2 second windows taken every second, and 3 second windows taken every 1.5 seconds.

- zip files containing optical flow files taken from both cameras. These files consist of more zip files with csv files that show changes in *u* and *v* for each time-stamp. You can download data from both cameras (side and front view).


By default, all csv files are downloaded (zipped OF files are avoided on purpose). However, you can modify this when calling the **featureDownload** function.


#### Example

- Default download

      featureDownload('ParentFolder//')

  Outputs:

      ParentFolder\
                  \Subject#\
                           \Activity$\
                                     \Trial%\
                                            \Subject#Activity$Trial%Features1&0.5.csv
                                            \Subject#Activity$Trial%Features2&1.csv
                                            \Subject#Activity$Trial%Features3&1.5.csv
                                            \CameraFeaturesSubject#Activity$Trial%.csv
                                            \Subject#Activity$Trial%CameraFeatures1&0.5.csv
                                            \Subject#Activity$Trial%CameraFeatures2&1.csv
                                            \Subject#Activity$Trial%CameraFeatures3&1.5.csv

- Choosing time-windows

 If you would like to choose only some of the time-windows, you can modify the **t_window** array. For example, if you only wanted to download  *1 second windows taken every 0.5 seconds* and *2 second windows taken every second*, you can input:

      featureDownload('ParentFolder//',t_window = ['1&0.5','2&1'])

  Outputs:

      ParentFolder\
                  \Subject#\
                           \Activity$\
                                     \Trial%\
                                            \Subject#Activity$Trial%Features1&0.5.csv
                                            \Subject#Activity$Trial%Features2&1.csv
                                            \CameraFeaturesSubject#Activity$Trial%.csv
                                            \Subject#Activity$Trial%CameraFeatures1&0.5.csv
                                            \Subject#Activity$Trial%CameraFeatures2&1.csv


- Avoiding features taken from sensor data

      featureDownload('ParentFolder//', csv_files=False)

  Outputs:

      ParentFolder\
                  \Subject#\
                           \Activity$\
                                     \Trial%\
                                            \CameraFeaturesSubject#Activity$Trial%.csv
                                            \Subject#Activity$Trial%CameraFeatures1&0.5.csv
                                            \Subject#Activity$Trial%CameraFeatures2&1.csv
                                            \Subject#Activity$Trial%CameraFeatures3&1.5.csv

- Avoiding resized camera OF files:

      featureDownload('ParentFolder//', cameras=False)

  Outputs:

      ParentFolder\
                  \Subject#\
                           \Activity$\
                                     \Trial%\
                                            \Subject#Activity$Trial%Features1&0.5.csv
                                            \Subject#Activity$Trial%Features2&1.csv
                                            \Subject#Activity$Trial%Features3&1.5.csv
                                            \Subject#Activity$Trial%CameraFeatures1&0.5.csv
                                            \Subject#Activity$Trial%CameraFeatures2&1.csv
                                            \Subject#Activity$Trial%CameraFeatures3&1.5.csv

- Avoiding features taken from the resized OF camera files:

      featureDownload('ParentFolder//', feat_cam_OF=False)

  Outputs:

      ParentFolder\
                  \Subject#\
                           \Activity$\
                                     \Trial%\
                                            \Subject#Activity$Trial%Features1&0.5.csv
                                            \Subject#Activity$Trial%Features2&1.csv
                                            \Subject#Activity$Trial%Features3&1.5.csv

- Allowing Camera OF zip files:

      featureDownload('ParentFolder//', Complete_OF=True)

  Outputs:

      ParentFolder\
                  \Subject#\
                           \Activity$\
                                     \Trial%\
                                            \Subject#Activity$Trial%Features1&0.5.csv
                                            \Subject#Activity$Trial%Features2&1.csv
                                            \Subject#Activity$Trial%Features3&1.5.csv
                                            \CameraFeaturesSubject#Activity$Trial%.csv
                                            \Subject#Activity$Trial%CameraFeatures1&0.5.csv
                                            \Subject#Activity$Trial%CameraFeatures2&1.csv
                                            \Subject#Activity$Trial%CameraFeatures3&1.5.csv
                                            \Subject#Activity$Trial%Camera1_OF.zip
                                            \Subject#Activity$Trial%Camera2_OF.zip
                                
   - - You can choose which camera data to download by modifying the **n_cam** array variable. See the example section in the **Downloading the Data Set** section for more information.
