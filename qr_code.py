import base64
import qrcode
import os


def convert_to_binary(filename):
    with open(filename,'rb') as file:
        # print(file.read())
        return file.read()

def binary_to_file(binary_data):
    data = base64.b64encode(binary_data)
    data = data.decode('UTF-8')
    # print(data)
    return data


def my_qr(data):
    img = qrcode.make(f'{data}')
    # print(img)
    img.save('myqrcode.png')
    # abc = convert_to_binary('C:\\Users\\sanke\\OneDrive\\Desktop\\faee\\LineUp\\myqrcode.png')
    abc = convert_to_binary("./myqrcode.png")
    # print(abc)
    os.remove("./myqrcode.png")
    # binary_to_file(abc)

    return abc


my_qr("a:2,b=2")
# abc = convert_to_binary('C:\\Users\\sanke\\OneDrive\\Desktop\\faee\\LineUp\\myqrcode.png')
# os.remove('C:\\Users\\sanke\\OneDrive\\Desktop\\faee\\LineUp\\myqrcode.png')
# print(abc)
# print(binary_to_file('./static/myqr.png',abc))