# Camera OF files


In this section you'll find the necessary files to work with our **optical flow** files from both cameras. Images were taken with a 640x480 pixel
format. From these images, the optical flow was stored in csv files, stating changes in *u* and *v* axis. To work with these files, we
joined them as lines, stating their timestamps. However, these file proved to be heavy, so a resize was made to work with them, changing 
the image size to 20x20 pixels, taking only the magnitude of the *u* and *v* changes.

## resizeOF.py

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



## Tagging the data

Because the optical flow files were not tagged, the resutling csv files will not be tagged. However, if you have tagged associated data you can get the correct tags from them. In our case, our [Data Set](https://drive.google.com/file/d/1JBGU5W2uq9rl8h7bJNt2lN4SjfZnFxmQ/view) can be used to get the corresponding tags for each timestamp.

The **tag_tracker.py** program was built to adress this issue.



