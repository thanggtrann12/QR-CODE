import json
from sre_constants import SUCCESS
import cv2
from pyzbar import pyzbar
from server.post import post
from car_info.plate_detection import plate_detection
last_qr_code = ""


def read_qr_codes(frame):
    barcodes = pyzbar.decode(frame)
    global last_qr_code
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        # 1
        qr_code_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, qr_code_info, (x + 6, y - 6),
                    font, 2.0, (255, 255, 255), 1)
        # 3
        if qr_code_info != "" and qr_code_info != last_qr_code:
            resp, car_info = plate_detection()
            jsonData = json.loads(qr_code_info)
            user_info = jsonData["username"]
            if user_info != "":
                if resp == SUCCESS:
                    resp = post(user_info, car_info)
                    if resp == SUCCESS:
                        print("Successfully posted")
                    else:
                        print("Error posting", resp[1])

            last_qr_code = qr_code_info
    return frame


def main():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame = read_qr_codes(frame)
        cv2.imshow('QT - QR code reader', frame)
        cv2.waitKey(1)
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
