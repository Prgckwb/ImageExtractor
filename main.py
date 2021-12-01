# Written by Prgckwb

import argparse
import os
import time

import PyPDF2
import cv2
from PIL import Image


# Function to retrieve command line arguments
def init_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="File name of the video to be converted")
    parser.add_argument("frame", help="Number of frames to be cut from the video.", type=int)
    argument = parser.parse_args()
    return argument


# Function to extract an image by specifying the video file name and the number of frames to be cut out.
# Remove duplicate images using PSNR method and return image list.
# The value of "25" is used as the threshold to identify the same image by the PSNR method.
def cut_images(movie_filename, dframe):
    images = []
    cap = cv2.VideoCapture(movie_filename)
    max_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    i = 0
    while cap.isOpened():
        print('\r - Cutting now... {:.3f}%'.format(i * 100.0 / max_frame), end='')

        if i % dframe == 0:
            ret, current_frame = cap.read()
            if ret and (i == 0 or cv2.PSNR(images[-1], current_frame) < 25):
                images.append(current_frame)
        else:
            ret = cap.grab()

        if not ret:
            print()
            break

        i += 1
    cap.release()
    return images


if __name__ == '__main__':
    # Start point for measurement of execution time
    start = time.perf_counter()

    # Getting command line arguments
    args = init_argument()
    mov_filename = args.input_file
    output_dir = './output'
    dframe = args.frame
    img_filename = mov_filename.split('.')[0]

    # If the directory specified as the output destination does not exist, create it.
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    # images: A list of images extracted from the video.
    # j: Index to use for image file names
    images = cut_images(mov_filename, dframe)

    file_count = 0
    for image in images:
        print('\r - Converting JPG Files to PDF Files now... {:.3f}%'.format((file_count + 1) * 100.0 / len(images)),
              end='')
        filename = f'{output_dir}/{img_filename}_{file_count}.pdf'
        img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img.convert("RGB").save(filename)
        file_count += 1

    print()
    merger = PyPDF2.PdfFileMerger()
    for i in range(file_count):
        print('\r - Creating Combined PDF File now... {:.3f}%'.format((i + 1) * 100.0 / file_count), end='')
        merger.append(f'{output_dir}/{img_filename}_{i}.pdf')
    merger.write(f'{img_filename}.pdf')
    print(f'\nFile: {output_dir}/{img_filename}_*.pdf has been created.')
    print(f'File: {img_filename}.pdf has been created.')
    merger.close()

    # End point for measurement of execution time
    end = time.perf_counter()
    print('Execution time: {:.3f}s'.format(end - start))
