import mysql.connector
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
my_db = mysql.connector.connect(
  host="sql.freedb.tech",
  user="freedb_images",
  password="gEzze6ZHjU#M4e2",
  database="freedb_image_data"
)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        image_data = request.get_data()
        nparr = np.frombuffer(image_data, np.uint8)
        
        # Generate a filename with the current datetime
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S") + '.jpg'
        
        # Save the image to the database
        my_cursor = my_db.cursor()
        sql = "INSERT INTO images (name, image_data) VALUES (%s, %s)"
        val = (filename, nparr.tobytes())
        my_cursor.execute(sql, val)
        my_db.commit()
        
        return 'Image uploaded and saved successfully'


@app.route('/')
def index():
    return render_template('index.html')








 
# main driver function
if __name__ == '__main__':


    app.run() # , port=8100, ssl_context='adhoc'