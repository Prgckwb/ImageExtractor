import cv2
import numpy as np


def detect_square1():
    # 画像を読み込む。
    gray = cv2.imread('output/mit_005.png', cv2.IMREAD_GRAYSCALE)
    # gray = cv2.imread('output/mit_005.png', cv2.IMREAD_GRAYSCALE)

    # 輪郭抽出
    # OpenCV 3 の場合
    # contours = cv2.findContours(
    #     binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    contours = cv2.findContours(
        gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # 一番面積が大きい輪郭を選択する。
    max_cnt = max(contours, key=lambda x: cv2.contourArea(x))

    # 黒い画像に一番大きい輪郭だけ塗りつぶして描画する。
    out = np.zeros_like(gray)
    mask = cv2.drawContours(out, [max_cnt], -1, color=255, thickness=-1)

    # 背景画像と前景画像を合成
    result = np.where(mask == 255, gray, out)

    cv2.imwrite('out.png', result)


if __name__ == '__main__':
    detect_square1()
