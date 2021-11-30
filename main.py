import argparse
import os

import cv2
# コマンドライン引数を取り出す関数
import numpy as np


def init_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="File name of the video to be converted")
    parser.add_argument("output_path", help="Path of the image file to be output")
    parser.add_argument("frame", help="Number of frames to be cut from the video.", type=int)
    argument = parser.parse_args()
    return argument


# 動画ファイル名と切り出すフレーム数を指定して画像を取り出す関数
def cut_images(movie_filename, dframe):
    images = []
    cap = cv2.VideoCapture(movie_filename)
    i = 0
    while cap.isOpened():
        ret, current_frame = cap.read()
        if not ret:
            print("Extract Finished!!")
            break

        if i % dframe == 0:
            images.append(current_frame)

        i += 1
    cap.release()
    return images


# ターミナルからの実行方法
# % python3 main.py (変換したい動画ファイル名) (画像を保存したいディレクトリ名)
# ex) python3 main.py sample.mp4 ./output
if __name__ == '__main__':

    # ターミナルでコマンドライン引数がなかった時の例外処理
    # IDEで実行した場合はsample.mp4をファイル名とする
    args = init_argument()
    mov_filename = args.input_file
    output_dir = args.output_path
    dframe = args.frame

    # 出力先で指定したフォルダが存在しなかったら作る
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    # 切り出した画像を保存しておくリスト
    images = cut_images(mov_filename, dframe)
    print(type(images))
    print(np.shape(images))

    j = 0
    for image in images:
        cv2.imwrite(f'{output_dir}/sample{j}.jpg', image)
        j += 1
