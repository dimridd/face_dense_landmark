"""
USAGE:
    python3 merge_file.py 14-01-2020.txt 07-01-2020.txt
"""

import os
import sys
import re
import csv
import pandas as pd


input_folder = "impure_csv's"

input_lst = os.listdir(input_folder)
if not len(input_lst):
    print("Empty Directory: " + input_folder)

df = [[]] * len(input_lst)
idx = 0

points_data = []
for lst in input_lst:

    try:
        if lst.split(".")[1] == "csv":
            df[idx] = pd.read_csv(os.path.join(input_folder, lst), "r")
            if idx == 0:
                head = list(df[idx].keys())
                points_data = [head[0].split(",")]
    except OSError as e:
            print('Not A Valid Format', e)

    for index, row in df[idx].iterrows():
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

                x = res[0]
                y = res[1]
                w = res[2]
                h = res[3]

                data.append(x)
                data.append(y)
                data.append(w)
                data.append(h)
                break
            data.append(res)
        points_data.append(data)
    idx += 1

data_file = open("impure_csv_output/impureCsvOutput" + '.csv', 'w')
with data_file:
    # create the csv writer object
    csv_writer = csv.writer(data_file)

    csv_writer.writerows(points_data)
