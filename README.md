# ImageExtractor

A program that extracts image files from video files. OpenCV, PyPDF2 and pillow are used as an external module.

## Prerequisite

- An environment for running Python 3
- Module
    - OpenCV
    - PyPDF2
    - pillow

## Usage

If you don't have OpenCV in your environment, you can install it as follows

### Conda (Recommend)

```
conda install opencv
conda install -c conda-forge pypdf2  
conda install pillow
```

### Run
First, navigate to the directory that contains main.py. When you call main.py with the python command, give the file name (path name) of the video you want to convert and the number of frames to extract from the video as command line arguments in this order.


ex) Extract the video file **sample.mp4** as an image every **180**
frames.

```
python3 main.py sample.mp4 180
```

## Note

- If you cannot run it, check if main.py exists in the current directory.
- If the execution time is long, it may be due to the following
    - The frame specification number is too small.
    - The video is too long.
    - Video quality is too high.

  ex) Under my PC's execution environment, extracting a video of 42 minutes in length with a size of 640x480 every 180
  frames took about 20 seconds before the program finished.

