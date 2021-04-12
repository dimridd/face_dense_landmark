import cv2
import numpy as np
import csv
import math


video_name = "dataset/faces/face1.mp4"
video_name1 = "dataset/samples/sample1.mp4"

data_file = open("impure_csv's/data_set1" + '.csv', 'w')
header = ["imagePath"]

for idx in range(701):
    header.append("p{}".format(idx + 1))

header.append("top")
header.append("left")
header.append("width")
header.append("height")

point_data = []

final = [header]

# Create an object to read
# from camera
video = cv2.VideoCapture(video_name)
video1 = cv2.VideoCapture(video_name1)

frameRate = video.get(5) / 4

# We need to check if camera
# is opened previously or not
if not video.isOpened():
    print("Error reading video {}".format(video_name))

if not video1.isOpened():
    print("Error reading video file {}".format(video_name1))


# We need to set resolutions.
# so, convert them from float to integer.
# frame_width = int(video.get(3))
# frame_height = int(video.get(4))
#
# size = (frame_width, frame_height)

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.

# (".mp4", "mp4v")
# (".avi", "MJPG")
# result = cv2.VideoWriter('video.mp4',
#                          cv2.VideoWriter_fourcc(*'mp4v'),
#                          fps=29, frameSize=size)

img_idx = 0

while True:
    ret, frame = video.read()
    ret1, frame1 = video1.read()

    frameId = video.get(1)  # current frame number

    if ret:
        image = frame
        image1 = frame1

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        white_px = np.asarray([255, 255, 255])
        black_px = np.asarray([0, 0, 0])

        (row, col) = thresh.shape
        img_array = np.array(image)

        for r in range(row):
            for c in range(col):
                px = gray[r][c]
                if not all(px == black_px):
                    img_array[r][c] = white_px

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        erosion = cv2.erode(img_array, kernel, iterations=1)

        gray = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, 0)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        contour = max(contours, key=cv2.contourArea)

        # cv2.drawContours(image1, [contour], 0, (0, 255, 0), 3)

        x, y, w, h = cv2.boundingRect(contour)
        # cv2.rectangle(image1,(x,y),(x+w,y+h),(0,255,0),2)

        # Display the frame
        # saved in the file
        if frameId % math.ceil(frameRate) == 0:

            imagePath = "nitin/" + "image_{}.jpg".format(img_idx)
            cv2.imwrite(imagePath, image1)

            point_data.append(imagePath)
            for point in contour:
                point_data.append(list(point[0]))
            img_idx += 1

            point_data.append(x)
            point_data.append(y)
            point_data.append(w)
            point_data.append(h)

            print("file {} processed".format(img_idx))

            final.append(point_data)
        point_data = []
    else:
        break
    #     # Press S on keyboard
    #     # to stop the process
    #     if cv2.waitKey(1) & 0xFF == ord('s'):
    #         break
    # else:
    #     break

with data_file:
    # create the csv writer object
    csv_writer = csv.writer(data_file)

    csv_writer.writerows(final)

# # When everything done, release
# # the video capture and video
# # write objects
# video.release()
# result.release()

# # Closes all the frames
# cv2.destroyAllWindows()

# print("The video was successfully saved")
