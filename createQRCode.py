# install library for QR code by: pip install qrcode[pil] -- [pil] additional dependencies
import base64
import io

import  qrcode

def generateQRCode(url):

    url=url.strip()
    print(url)
    file_path = "qrcode.png"

    qr = qrcode.QRCode()
    qr.add_data(url)

    img = qr.make_image()

    #encoding to Base64
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    img.save(file_path)

    return img_base64

