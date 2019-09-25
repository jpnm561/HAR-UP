# Camera OF files


In this section you'll find the necessary files to work with our **optical flow** (OF) files from both cameras. Images were taken with a 640x480 pixel
format. From these images, the optical flow was stored in csv files, stating changes in *u* and *v* axis. To work with these files, we
joined them as lines, stating their timestamps. However, these file proved to be heavy, so a resize was made to work with them, changing 
the image size to 20x20 pixels, taking only the magnitude of the *u* and *v* changes.

## Unzipping the files

Zipped files containing a Camera's OF files for a certain subject (#), activity ($), trial (%) and camera (?) contain the following files:

```
   Subject#Activity$Trial%Camera?_OF.zip/
                                        /TIMESTAMP1_u.zip/
                                                         /TIMESTAMP1_u.csv
                                        /TIMESTAMP1_v.zip/
                                                         /TIMESTAMP1_v.csv
                                        /TIMESTAMP2_u.zip/
                                                         /TIMESTAMP2_u.csv
                                        /TIMESTAMP2_v.zip/
                                                         /TIMESTAMP2_v.csv
                                        ...
                                        /TIMESTAMPn_u.zip/
                                                         /TIMESTAMPn_u.csv
                                        /TIMESTAMPn_v.zip/
                                                         /TIMESTAMPn_v.csv

```

The program **Decompressor.py** was made to ease the unzipping process. It should be noted that unzipping these files can take a while (more than an hour per subject when unzipping both cameras).

### Choosing direcotries

When running the function **Decompressor()**, you need to state the path

def Decompressor(o_dir,n_dir,
              n_sub=[1,17],
              n_act=[1,11],
              n_trl=[1,3],
              n_cam=[1,2]):

## Resizeing the files

### Directory arrangement

To use the **camOF_joiner()** function, it is necessary to state paths for the unzipped optical flow files and the path in which you want to store the resized csv files.


#### Example

If you have the following arrangement:

```
    ParentFolder\
                \UnzippedOF\
                           \Subject#\
                                    \Activity$\
                                              \Trial%\
                                                     \Subject#Activity$Trial%Camera1_OF_UZ\
                                                                                          \TIMESTAMP1_u.csv
                                                                                          \TIMESTAMP1_v.csv
                                                                                          \TIMESTAMP2_u.csv
                                                                                          \TIMESTAMP2_v.csv
                                                                                          ...
                                                                                          \TIMESTAMPn_u.csv
                                                                                          \TIMESTAMPn_v.csv
                                                                                          
```
And wish to store the resulting csv files in a folder (with the same parent folder) called *ResizedOF* you'd have to run:

```
def main():
    OF_path = 'ParentFolder//UnzippedOF//'
    resize_path = 'ParentFolder//ResizedOF//'
    camOF_joiner(OF_path,resize_path)
    print('End of task')
```
  Which outputs:

    ParentFolder\
                \ResizedOF\
                           \Subject#\
                                    \Activity$\
                                              \CameraFeaturesSubject#Activity$Trial1.csv
                                              \CameraFeaturesSubject#Activity$Trial2.csv
                                              \CameraFeaturesSubject#Activity$Trial3.csv


### Choosing subjects, activities, trials and cameras

By default, the program is run for **17 subjects**, each with **11 activities**, **3 trials** per activity and **2 cameras** for every trial. These numbers can be modified in the function's input. It is important to note that the program is built in a way that only allows to call these objects in order, so for example, if you wanted to get the features of subjects 1, 2, 3, 7, 10 and 11 you would have to call three times the function, and specifiy that you don't want a single output file (because this would erase the previous outputs).


    camOF_joiner(OF_path,resize_path, n_sub=[1,3], single_f=False)
    camOF_joiner(OF_path,resize_path, n_sub=[7,7], single_f=False)
    camOF_joiner(OF_path,resize_path, n_sub=[10,11], single_f=False)
    

To recap:


  For subjetcts:
  
    n_sub = [start, end] 


  For activities:
  
    n_act = [start, end]


  For trials:
  
    n_trl = [start, end]
    
    
  For cameras:
  
    n_cam = [start, end]

It should be noted that **start** and **end** both refer to integer numbers. Another important consideration, is that changing the camera number does not change the amount of output files, but only takes one camera into consideration (side camera or front camera).

## Tagging the data

Because the optical flow files were not tagged, the resutling csv files will not be tagged. However, if you have tagged associated data you can get the correct tags from them. In our case, our [Data Set](https://drive.google.com/file/d/1JBGU5W2uq9rl8h7bJNt2lN4SjfZnFxmQ/view) can be used to get the corresponding tags for each timestamp.

The **tag_tracker.py** program was built to adress this issue.



