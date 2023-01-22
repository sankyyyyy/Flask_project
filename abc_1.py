import base64
import qrcode
import os
import json

username="sanket"
slot=10
data = {"username":username,"slot":slot}

data = json.dumps(data)
def my_qr1(data):
    img = qrcode.make(data)
    # print(img)
    img.save('myqrcode.png')
    # abc = convert_to_binary('C:\\Users\\sanke\\OneDrive\\Desktop\\faee\\LineUp\\myqrcode.png')
    # abc = convert_to_binary("./myqrcode.png")
    # print(abc)
    # os.remove("./myqrcode.png")
    # binary_to_file(abc)

    # print(abc)
my_qr1(data)