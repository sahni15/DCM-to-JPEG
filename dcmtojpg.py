import numpy as np
import os
import pydicom
from PIL import Image
from flask import Flask, render_template, request

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/dcmtojpg', methods=["POST"])
def upload():
    # get the uploaded file
    target = os.path.join(APP_ROOT, 'dcm/')

    if not os.path.isdir(target):
        os.mkdir(target)

    file = request.files['upload-file']
    # print(file)
    filename = file.filename
    destination = "/".join([target, filename])
    # print(destination)
    file.save(destination)
    name = filename.replace('.dcm', '.jpeg')

    # convert the dcm file to jpeg using dcmtojpg function
    dicomtojpg(destination)

    # send the converted file to the webpage which will allow the user to download it
    return render_template('download.html', image='static/images/'+name)


if __name__ == '__main__':
    app.run(debug=True)


def dicomtojpg(file):
    # file is the uploaded file
    try:
        ds = pydicom.dcmread(file)
        shape = ds.pixel_array.shape

        # Convert to float
        image_2d = ds.pixel_array.astype(float)

        # Rescaling and normalising
        image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0

        # Convert to uint
        image_2d_scaled = np.uint8(image_2d_scaled)

        # save numpy array to a jpeg image
        im = Image.fromarray(image_2d_scaled)

        target_img = os.path.join(APP_ROOT, 'static/images/')

        if not os.path.isdir(target_img):
            os.mkdir(target_img)

        name = os.path.basename(file)
        destination = os.path.join(target_img, name.replace('.dcm', '.jpeg'))
        im.save(destination, "JPEG")
    except:
        print('Could not convert: ', file)