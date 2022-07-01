# Written by Prgckwb

import argparse
import glob
import math
import os
import time

import PyPDF2
import cv2
import numpy as np
from PIL import Image, ImageFile
from tqdm import tqdm

from features import calc_distances, extract_dcnn_data

ImageFile.LOAD_TRUNCATED_IMAGES = True


# Function to retrieve command line arguments
def init_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="File name of the video to be converted")
    parser.add_argument("frame", help="Number of frames to be cut from the video.", type=int)
    argument = parser.parse_args()
    return argument


# 動画ファイルからdframeごとに画像を抽出する
def cut_images(video_name, dframe):
    images = []
    video_capture = cv2.VideoCapture(video_name)

    # 動画の全フレーム数
    max_frame = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # 動画の全フレームからdframeごとに画像を切り出す
    for frame_count in tqdm(range(max_frame), desc="[Extract images from video]"):
        if frame_count % dframe == 0:
            ret, current_frame = video_capture.read()
            if ret and (frame_count == 0 or cv2.PSNR(images[-1], current_frame) < 25):
                images.append(current_frame)
        else:
            # dframe番目でないときは高速化のためフレーム画像を読み込まない
            ret = video_capture.grab()

    video_capture.release()
    return images


# Function to detect image duplicates and remove them.
# To detect duplicates in a double loop, use the image list once the duplicates of adjacent frames are removed.
def remove_duplicate_PSNR(imgs):
    delete_index = set()
    imgs_length = len(imgs)
    # count = imgs_length
    for i in tqdm(range(imgs_length - 1), desc="[Remove duplicate images]"):
        for j in tqdm(range(i + 1, imgs_length), leave=False):
            if cv2.PSNR(imgs[i], imgs[j]) > 25:
                delete_index.add(j)
        # count += imgs_length

    delete_index = sorted(list(delete_index))
    delete_index.reverse()

    for i in delete_index:
        imgs.pop(i)

    return imgs


def remove_duplicate(images, data_dir, video_name, frame):
    data_path = f"{data_dir}/{video_name}_f{frame}.npy"

    if os.path.exists(data_path):
        data = np.load(data_path)
    else:
        data = extract_dcnn_data(images, video_name=video_name, frame=frame, can_save=True)

    delete_index = set()
    n = len(images)

    for i in tqdm(range(n - 1, 1, -1), desc="[Remove duplicate images]"):
        for j in tqdm(range(i - 1, 0, -1), leave=False):
            if calc_distances(data, i, j) < 100:
                delete_index.add(j)

    delete_index = sorted(list(delete_index))
    delete_index.reverse()

    for i in delete_index:
        images.pop(i)

    return images


# Convert a numpy array to an Image array in the Pillow module to generate individual PDF files.
def convert_img2pdf(images, output_dir, img_filename):
    out_dir_name = f"{output_dir}/{img_filename}"
    os.makedirs(out_dir_name, exist_ok=True)

    # 画像の枚数が10の何乗か？
    images_num = math.floor(math.log10(len(images)))

    for i, image in enumerate(tqdm(images, desc="[Generate split PDF files]")):
        file_name_count = str(i).zfill(images_num + 1)
        filename = f'{out_dir_name}/{img_filename}_{file_name_count}.pdf'
        # filename = f'{output_dir}/{img_filename}_{file_name_count}.png'
        img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img.convert("RGB").save(filename)


def merge_pdfs(output_dir, img_filename):
    # Merge disparate PDF files into one PDF file
    out_dir_name = f"{output_dir}/{img_filename}"
    file_list = sorted(glob.glob(f"{out_dir_name}/{img_filename}*.pdf"))

    merger = PyPDF2.PdfFileMerger()
    for pdf_file in tqdm(file_list, desc="[Combine into a single PDF file]"):
        merger.append(pdf_file)
    merger.write(f'{img_filename}.pdf')
    print(f'\nFile: {output_dir}/{img_filename}_*.pdf has been created.')
    print(f'File: {img_filename}.pdf has been created.')
    merger.close()


def main():
    # Start point for measurement of execution time
    start = time.perf_counter()

    # Getting command line arguments
    args = init_argument()
    video_file = args.input_file
    frame = args.frame
    output_dir = './output'
    video_filename = video_file.split('.')[0]

    # If the directory specified as the output destination does not exist, create it.
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    # images: A list of images extracted from the video.
    images = cut_images(video_file, frame)

    # Recheck for duplicate images and delete them if they exist.
    images = remove_duplicate(images, video_name=video_filename, data_dir="DCNN_data", frame=frame)
    convert_img2pdf(images, output_dir, video_filename)

    merge_pdfs(output_dir, video_filename)

    # End point for measurement of execution time
    end = time.perf_counter()

    print('Execution time: {:.3f}s'.format(end - start))


if __name__ == '__main__':
    main()
