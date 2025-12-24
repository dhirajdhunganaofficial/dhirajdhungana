from flask import Flask, render_template, request, redirect, url_for

import sendEmail,createQRCode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Dhiraj Dhungana', alert=False)

@app.route('/oldSite')
def oldSite():
    return render_template('oldSite.html')

@app.route("/contactInformation", methods=['POST'])
def notifyAboutContactInformation():
    name=request.form['Full Name']
    email=request.form['Email']
    phoneNumber=request.form['Phone Number']
    subject=request.form['Subject']
    message=request.form['Message']
    sendEmail.sendEmail(name,email,phoneNumber,subject,message)
    # return render_template('index.html', title='Dhiraj Dhungana', alert=True)
    return redirect(url_for('index'))

@app.route('/qrCode')
def qrCode():
    return render_template('qrCode.html', title='QR Code Generator')

@app.route("/qrCode", methods=['POST'])
def generateQRCode():
    url=request.form['url']
    qrCode = createQRCode.generateQRCode(url)
    return render_template('qrCode.html', qrCode = qrCode)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)