
import os
import numpy as np
import cv2
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        image_data = request.get_data()
        nparr = np.frombuffer(image_data, np.uint8)
        print("-",nparr)
        
        # Decode image using OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Save image using OpenCV
        save_path = 'webrtc_alternative/static/image.png'
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        success = cv2.imwrite(save_path, img)
        if success:
            app.logger.info('Image saved successfully')
            return 'Image uploaded and saved successfully'
        else:
            app.logger.error('Failed to save image')
            return 'Failed to save'



@app.route('/')
def index():
    return render_template('index.html')

@app.route("/image")
def show_image():
    return render_template('alfa.html')






 
# main driver function
if __name__ == '__main__':
    app.debug = True
    app.run() # , port=8100, ssl_context='adhoc'
