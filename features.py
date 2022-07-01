# 特徴量抽出用スクリプト
# 事前に使うだけで実際のCGIプログラムには関係しない

import glob

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms
from tqdm import tqdm

images_path_list = [img for img in sorted(glob.glob(f"output/*.png"))]

device = "cpu"

if torch.cuda.is_available():
    device = "cuda"
elif torch.has_mps:
    device = "mps"


def extract_dcnn_hist(img_path, transform, model):
    img = Image.open(img_path)
    img = transform(img).unsqueeze(0)
    img = img.to(device)
    output = model(img)

    return output


def extract_dcnn_data(data_dir="data", isSaved=False):
    # model = models.vgg16(pretrained=True)
    model = models.vgg16(weights=models.VGG16_Weights.DEFAULT)

    # 最終層を取り除く
    layers = list(model.classifier.children())[:-2]
    model.classifier = nn.Sequential(*layers)

    # 推論モードへ
    model.eval()

    model = model.to(device)

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        )
    ])

    all_data = []
    for i, image in enumerate(tqdm(images_path_list)):
        data = extract_dcnn_hist(image, transform, model)
        data = data.to('cpu').detach().numpy().copy()
        all_data.append(data)

    all_data = np.array(all_data)
    print(all_data.shape)

    if isSaved:
        np.save(f"{data_dir}/DCNN", all_data)
        return
    else:
        return all_data


def compare(index=0):
    images_list = glob.glob("output/*.png")
    data = np.load("data/DCNN.npy")
    distance = []

    for i in range(len(images_list)):
        d = np.sqrt((data[index][0] - data[i][0]) ** 2)
        distance.append(d.sum())
    distance = np.array(distance)  / np.max(distance)
    distance = list(distance)

    dict = []
    for i, x in enumerate(distance):
        dict.append({"index": i, "num": x})

    for x in dict:
        print(x)


def calc_distances(data, idx1, idx2):
    dis = np.sqrt((data[idx1][0] - data[idx2][0]) ** 2)
    dis = dis.sum()
    return dis


if __name__ == '__main__':
    # print(np.load("data/DCNN.npy").shape)
    extract_dcnn_data(isSaved=True)
    compare(index=44)
