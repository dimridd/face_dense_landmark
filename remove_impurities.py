import pandas as pd
import csv
import re
import torchvision.transforms.functional as FT
import numpy as np
from PIL import Image
import cv2


df = pd.read_csv("impure_csv_output/impureCsvOutput.csv", "w")

points_data = []
for idx, row in df.iterrows():
    data = []
    row = list(row)[0].split('","')

    for col_idx in range(len(row)):

        if col_idx == len(row) - 1:
            str_ = row[col_idx].split('"')
            bbox = str_[1]
            str_ = str_[0]
        elif col_idx == 0:
            str_ = row[col_idx].split('"')
            image_name = str_[0]
            str_ = str_[1]
            data.append(image_name)
        else:
            str_ = row[col_idx]

        temp = re.findall(r"\d+", str_)
        res = list(map(int, temp))

        if col_idx == len(row) - 1:
            temp = re.findall(r"\d+", bbox)
            res = list(map(int, temp))
        data.append(res)
    points_data.append(data)


class maxLen:
    def __init__(self, list_):
        self.list_ = list_

    def __len__(self):

        return max([len(sublist) for sublist in self.list_ if isinstance(sublist, list)]) - 1


class equalizeList:
    def __init__(self, max_len):
        self.max_len = max_len

    def __getitem__(self, idx):

        img_data = points_data[idx]
        bbox = img_data[-1]
        landmark_points = img_data[:-1]

        if len(landmark_points) < self.max_len:
            added_length = self.max_len - len(landmark_points)
            added_points = landmark_points[-added_length:]
            landmark_points.extend(added_points)
        landmark_points.append(bbox)

        return landmark_points


sample_size = len(points_data)
max_len = len(maxLen(points_data))


"""
writing final output
"""
data_file = open("pure_csv_output/finalCsvOutput" + '.csv', 'w')
header = ["imagePath"]

for idx in range(max_len-1):
    header.append("p{}".format(idx + 1))

header.append("top")
header.append("left")
header.append("width")
header.append("height")

point_data = []

final = [header]

for idx in range(sample_size):
    img_data = equalizeList(max_len)[idx]

    bbox = img_data[-1]
    landmark_points = img_data[:-1]

    x = bbox[0]
    y = bbox[1]
    w = bbox[2]
    h = bbox[3]

    landmark_points.append(x)
    landmark_points.append(y)
    landmark_points.append(w)
    landmark_points.append(h)

    print("image data{} added".format(idx+1))
    final.append(landmark_points)


with data_file:
    # create the csv writer object
    csv_writer = csv.writer(data_file)

    csv_writer.writerows(final)
