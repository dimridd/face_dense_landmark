import re
import xml.etree.ElementTree as ET
import pandas as pd
import csv
import re
import torchvision.transforms.functional as FT
import numpy as np
from PIL import Image
import cv2
import os


df = pd.read_csv("pure_csv_output/finalCsvOutput.csv", "r")

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


dataset = ET.Element("dataset")
root = ET.Element("images")
dataset.append(root)

for img_data in points_data:

    image = img_data[0].split(",")[0]
    image = os.path.abspath(image)

    image_el = ET.SubElement(root, "image")
    image_el.set("file", image)

    points = img_data[1:]
    bbox = points[-1]

    box_el = ET.SubElement(image_el, "box")
    box_el.set("top", "{}".format(bbox[0]))
    box_el.set("left", "{}".format(bbox[1]))
    box_el.set("width", "{}".format(bbox[2]))
    box_el.set("height", "{}".format(bbox[3]))

    idx = 0
    for point in points:
        if idx == len(points)-1:
            continue
        part_el = ET.SubElement(box_el, "part")
        part_el.set("name", "{}".format(idx))
        part_el.set("x", "{}".format(point[0]))
        part_el.set("y", "{}".format(point[1]))

        idx += 1

tree = ET.ElementTree(dataset)

with open("xml_file/finalXmlOutput.xml", "wb") as files:
    tree.write(files)
