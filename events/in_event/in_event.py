import json

lastData = ""

def extract_qr_code(qr_code):
    global lastData
    dataToExtract = qr_code
    if dataToExtract != lastData:
        dataToExtract = json.loads(dataToExtract)
        lastData = dataToExtract
    print(dataToExtract)