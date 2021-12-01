# ImageExtractor
A program that extracts image files from video files.
OpenCV is used as an external module.

## Prerequisite
- An environment for running Python 3
- OpenCV module

## Usage
If you don't have OpenCV in your environment, you can install it as follows
### Conda (Recommend)
```
conda install opencv
```

### Pip
```
pip3 install opencv-python
```

### Run
ex) Extract the video file "sample.mp4" to the "output" folder in the same directory as an image every 180 frames.
```
python3 main.py sample.mp4 ./output 180
```

## Note
- If you cannot run it, check if main.py exists in the current directory.
- If the execution time is long, it may be due to the following
  - The frame specification number is too small.
  - The video is too long.
  - Video quality is too high.

