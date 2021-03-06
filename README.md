# ImageExtractor

A program that extracts image files from video files. OpenCV, PyPDF2 and pillow are used as an external module.

## Prerequisite
Under correction due to specification change.

## Usage
Under correction due to specification change

### Run
First, navigate to the directory that contains main.py. When you call main.py with the python command, give the file name (path name) of the video you want to convert and the number of frames to extract from the video as command line arguments in this order.


ex) Extract the video file **sample.mp4** as an image every **180**
frames.

```
python3 main.py sample.mp4 180
```

As a result, a PDF file containing the extracted images will be generated in the directory where the python command was executed, and their individual PDF files in the output folder.

## Note

- If you cannot run it, check if main.py exists in the current directory.
- If the execution time is long, it may be due to the following
    - The frame specification number is too small.
    - The video is too long.
    - Video quality is too high.

[//]: # (  ex&#41; Under my PC's execution environment, extracting a video of 42 minutes in length with a size of 640x480 every 180)

[//]: # (  frames took about 20 seconds before the program finished.)

