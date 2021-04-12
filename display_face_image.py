import pandas as pd
import csv
import re
import torchvision.transforms.functional as FT
import numpy as np
from PIL import Image
import cv2

df = pd.read_csv("pure_csv_output/finalCsvOutput.csv", "w")

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

# for img_data in points_data:
img_no = 20
image = Image.open(points_data[img_no][0].split(",")[0])
image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

points = points_data[img_no][1:]
bbox = points[-1]
landmarks = points[1:-1]

x = bbox[0]
y = bbox[1]
w = bbox[2]
h = bbox[3]

cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

for idx in np.r_[:len(landmarks):8]:
    cv2.circle(image, (landmarks[idx][0], landmarks[idx][1]), 2, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
cv2.imshow("image", image)
cv2.waitKey(0)
