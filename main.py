# Written by Prgckwb

import argparse
import math
import os
import time

import PyPDF2
import cv2
from PIL import Image


# TODO: プログレスバーをtqdmに移植
# TODO: 類似度検索手法を改善

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
    saved_images = []
    video_capture = cv2.VideoCapture(movie_filename)
    max_frame = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)

    frame_count = 0
    while video_capture.isOpened():
        print('\r - Cutting now... {:.3f}%'.format(frame_count * 100.0 / max_frame), end='')

        if frame_count % dframe == 0:
            ret, current_frame = video_capture.read()
            if ret and (frame_count == 0 or cv2.PSNR(saved_images[-1], current_frame) < 25):
                saved_images.append(current_frame)
        else:
            ret = video_capture.grab()

        if not ret:
            print()
            break

        frame_count += 1
    video_capture.release()
    return saved_images


# Function to detect image duplicates and remove them.
# To detect duplicates in a double loop, use the image list once the duplicates of adjacent frames are removed.
def remove_duplicate(imgs):
    delete_index = set()
    imgs_length = len(imgs)
    count = imgs_length
    for i in range(imgs_length - 1):
        for j in range(i + 1, imgs_length):
            print('\r - Deleting duplicate images... {:.3f}%'.format(
                100.0 * count / (imgs_length * (imgs_length - 1))),
                end='')
            if cv2.PSNR(imgs[i], imgs[j]) > 25:
                delete_index.add(j)
        count += imgs_length

    print()
    delete_index = sorted(list(delete_index))
    delete_index.reverse()

    for i in delete_index:
        imgs.pop(i)

    return imgs


def merge_pdfs(file_count, output_dir, img_filename):
    # Merge disparate PDF files into one PDF file
    merger = PyPDF2.PdfFileMerger()
    for i in range(file_count):
        print('\r - Creating Combined PDF File now... {:.3f}%'.format((i + 1) * 100.0 / file_count), end='')
        merger.append(f'{output_dir}/{img_filename}_{i}.pdf')
    merger.write(f'{img_filename}.pdf')
    print(f'\nFile: {output_dir}/{img_filename}_*.pdf has been created.')
    print(f'File: {img_filename}.pdf has been created.')
    merger.close()


def convert_img2pdf(images, output_dir, img_filename):
    # Convert a numpy array to an Image array in the Pillow module to generate individual PDF files.
    file_count = 0

    # 画像の枚数が10の何乗か？
    images_num = math.floor(math.log10(len(images)))
    for image in images:
        print('\r - Converting Image Array to PDF Files now... {:.3f}%'.format((file_count + 1) * 100.0 / len(images)),
              end='')
        # filename = f'{output_dir}/{img_filename}_{file_count}.pdf'
        file_name_count = str(file_count).zfill(images_num + 1)
        filename = f'{output_dir}/{img_filename}_{file_name_count}.png'
        img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img.convert("RGB").save(filename)
        file_count += 1

    print()
    return file_count


def main():
    # Start point for measurement of execution time
    start = time.perf_counter()

    # Getting command line arguments
    args = init_argument()
    mov_filename = args.input_file
    frame = args.frame
    output_dir = './output'
    img_filename = mov_filename.split('.')[0]

    # If the directory specified as the output destination does not exist, create it.
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    # images: A list of images extracted from the video.
    images = cut_images(mov_filename, frame)

    # Recheck for duplicate images and delete them if they exist.
    images = remove_duplicate(images)
    file_count = convert_img2pdf(images, output_dir, img_filename)

    # merge_pdfs(file_count, output_dir, img_filename)

    # End point for measurement of execution time
    end = time.perf_counter()

    print('Execution time: {:.3f}s'.format(end - start))


if __name__ == '__main__':
    main()
