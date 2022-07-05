import glob
import os
from pathlib import Path  # TODO: パス操作を移植する

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms
from tqdm import tqdm


def get_device():
    device = "cpu"

    if torch.cuda.is_available():
        device = "cuda"
    elif torch.has_mps:
        device = "mps"

    return device


def predict(img_path, transform, model, device):
    img = Image.fromarray(img_path)
    # img = Image.open(img_)
    img = transform(img).unsqueeze(0)
    img = img.to(device)
    output = model(img)

    return output


def extract_dcnn_data(images, video_name, frame, data_dir, can_save=False):
    device = get_device()
    weights = models.VGG16_Weights.DEFAULT
    model = models.vgg16(weights=weights)

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
    for i, image in enumerate(tqdm(images, desc="[Extract DCNN Features]")):
        data = predict(image, transform, model, device)
        data = data.to('cpu').detach().numpy().copy()
        all_data.append(data)

    all_data = np.array(all_data)

    if can_save:
        os.makedirs(data_dir, exist_ok=True)
        np.save(f"{data_dir}/{video_name}_f{frame}", all_data)

    return all_data


def compare(index=40):
    images_list = glob.glob("output/*.png")
    data = np.load("DCNN_data/01_MIT_DCNN.npy")
    distance = []

    for i in range(len(images_list)):
        d = np.sqrt((data[index][0] - data[i][0]) ** 2)
        distance.append(d.sum())
    distance = np.array(distance)  # / np.max(distance)
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
    pass
