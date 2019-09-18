# Camera OF files


In this section you'll find the necessary files to work with our **optical flow** files from both cameras. Images were taken with a 640x480 pixel
format. From these images, the optical flow was stored in csv files, stating changes in *u* and *v* axis. To work with these files, we
joined them as lines, stating their timestamps. However, these file proved to be heavy, so a resize was made to work with them, changing 
the image size to 20x20 pixels, taking only the magnitude of the *u* and *v* changes.

## Directory arrangement



## Tagging the data

Because the optical flow files were not tagged, the resutling csv files will not be tagged. However, if you have tagged associated data you can get the correct tags from them. In our case, our [Data Set](https://drive.google.com/file/d/1JBGU5W2uq9rl8h7bJNt2lN4SjfZnFxmQ/view) can be used to get the corresponding tags for each timestamp.


## Choosing subjects, activities, trials and cameras

