import cv2
import imutils
import pytesseract
import pandas as pd
import json
from server.post import full_data_post_request
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
index = ["color", "color_name", "hex", "R", "G", "B"]
data = pd.read_csv("./color.csv", names=index, header=None)
CAM_ID = 1


def recognize_color(R, G, B):
    minimum = 10000
    color_name = ""
    for i in range(len(data)):
        d = abs(R - int(data.loc[i, "R"])) + abs(G -
                                                 int(data.loc[i, "G"])) + abs(B - int(data.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            color_name = data.loc[i, "color_name"]
    return color_name


def extract_plate_number_with_color(data):
    id = {
        "twoFirstDigits": "",
        "vehicleColor": "",
        "block": "", "slotId": "",
        "fourLastDigits": ""
        }
    id["twoFirstDigits"] = data[0][:2]
    id["vehicleColor"] = data[1]
    id["block"] = CAM_ID
    id["slotId"] = 2
    id["fourLastDigits"] = data[0][-4:]
    print("extract: ", id)
    # full_data_post_request(id)

def Detection():
    PATH = "./car_img.jpg"
    image = cv2.imread(PATH)
    image = imutils.resize(image, width=600)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 170, 200)
    cnt, _ = cv2.findContours(
        edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img1 = image.copy()
    cv2.drawContours(img1, cnt, -1, (0, 255, 0), 3)
    cnt = sorted(cnt, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCnt = None
    img2 = image.copy()
    cv2.drawContours(img2, cnt, -1, (0, 255, 0), 3)
    for c in cnt:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            new_img = gray[y:y + h, x:x + w]
            b, g, r = img2[y+2, x]
            b = int(b)
            g = int(g)
            r = int(r)
            cv2.imwrite('Cropped Images-Text/Croped.png', new_img)
            carColor = recognize_color(r, g, b)
            break
    data = []
    Plate_num = pytesseract.image_to_string(new_img, lang='eng')
    if len(Plate_num) > 6:
        Plate_num = ''.join(e for e in Plate_num if e.isalnum())

    data.append(Plate_num)
    data.append(carColor)
    extract_plate_number_with_color(data)

Detection()