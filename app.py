
from flask import Flask,render_template
from flask import request
import numpy as np
import cv2
from flask import Flask, request
# app.py
from flask import Flask, render_template, request
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        image_data = request.get_data()
        nparr = np.frombuffer(image_data, np.uint8)
        
        # Decode image using OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Save image using OpenCV
        #cv2.imshow("incoming_image", img)
        cv2.imwrite('flask_app/static/image.png', img)

        return 'Image uploaded and saved successfully'


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/image")
def show_image():
    return render_template('alfa.html')






 
# main driver function
if __name__ == '__main__':
    app.debug = False
    app.run() # , port=8100, ssl_context='adhoc'
