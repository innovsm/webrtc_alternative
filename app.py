
from spare_parts import *
import numpy as np
import cv2
from deepface import DeepFace
from datetime import datetime
from flask import Flask, render_template, request
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

"""  
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

"""



@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST' and np.random.randint(0, 100) % 2 == 0:  # take  half of the request

        image_data = request.get_data()
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # emotion extraction must come here
        try:
            print("1")
            emotion = DeepFace.analyze(img, actions = ['emotion'])
            data_1 = emotion
            print("2")
            #print(emotion)
            dict_1 = {'angry': 0, 'disgust' : 0,'fear' : 0, 'happy' : 0, 'sad' : 0,'surprise' : 0,'neutral': 0}
            for i in data_1:
                dict_1[i['dominant_emotion']] += 1
            # inserting data into database
            print(data_1)
            insert_emotion_data(dict_1['angry'], dict_1['disgust'], dict_1['fear'], dict_1['happy'], dict_1['sad'], dict_1['surprise'], dict_1['neutral'])

            #cv2.imwrite("alfa/{}.jpg".format(count),img)
      
        except:
            pass
        

        return ""
     

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/beta')
def get_plot():
    plot_html,  dataframe = create_emotion_plot()
    final_result_calculated = calculate_attention_status(dataframe)

    return render_template("plot.html", plot_html=plot_html, final_result =final_result_calculated)
    


@app.route('/completed')

def alfa_index():
    return render_template('completed.html')









 
# main driver function
if __name__ == '__main__':


    app.run('0.0.0.0', debug=True,port=8100, ssl_context='adhoc' ) # , port=8100, ssl_context='adhoc'
