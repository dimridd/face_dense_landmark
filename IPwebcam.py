import urllib.request
import cv2
import numpy as np
import ssl

url = "http://25.60.230.181:8080/shot.jpg"
while True:
    # grab the url
    grab_url = urllib.request.urlopen(url)

    # convert it into array integer format
    img_read = np.array(bytearray(grab_url.read()), dtype=np.uint8)

    # decoding the image
    img = cv2.imdecode(img_read, -1)
    img_resize = cv2.resize(img, (600, 400))

    cv2.imshow('temp', img_resize)
    q = cv2.waitKey(1)
    if q == ord("q"):
        cv2.imwrite("image.jpg", img_resize)
        break

cv2.destroyAllWindows()
