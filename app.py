import mysql.connector
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

def get_database_connection():
    try:
        my_db = mysql.connector.connect(
            host="sql.freedb.tech",
            user="freedb_images",
            password="gEzze6ZHjU#M4e2",
            database="freedb_image_data"
        )
        return my_db
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        image_data = request.get_data()
        nparr = np.frombuffer(image_data, np.uint8)
        print("-",nparr)
        
        # Generate a filename with the current datetime
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S") + '.jpg'
        
        # Save the image to the database
        try:
            my_db = get_database_connection()
            my_cursor = my_db.cursor()
            sql = "INSERT INTO images (name, image_data) VALUES (%s, %s)"
            val = (filename, nparr.tobytes())
            my_cursor.execute(sql, val)
            my_db.commit()
            
            return 'Image uploaded and saved successfully'
        except mysql.connector.Error as error:
            print("Error while saving image to the database", error)
            return 'An error occurred while uploading the image'



@app.route('/')
def index():
    return render_template('index.html')








 
# main driver function
if __name__ == '__main__':


    app.run() # , port=8100, ssl_context='adhoc'
