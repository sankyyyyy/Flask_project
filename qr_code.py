import base64
import qrcode
import os
import json

def convert_to_binary(filename):
    with open(filename,'rb') as file:
        return file.read()

def binary_to_file(binary_data):
    data = base64.b64encode(binary_data)
    data = data.decode('UTF-8')
    return data


def my_qr(data):
    data = json.dumps(data)
    img = qrcode.make(data)
    img.save('myqrcode.png')
    mydata = convert_to_binary("./myqrcode.png")
    os.remove("./myqrcode.png")
    return mydata
