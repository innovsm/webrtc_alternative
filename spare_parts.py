import mysql.connector
from datetime import datetime
import pytz
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# main_algo ========================================================================================

def calculate_attention_status(df):
    # Calculate neutral percentage
    neutral_percentage = df['Neutral'].sum() / df[['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']].sum().sum()

    angry_list = list(df['Angry'])
    neutral_list = list(df['Neutral'])
    happy_list = list(df['Happy'])
    disgust_list = list(df['Disgust'])
    sad_list = list(df['Sad'])
    surprise_list = list(df['Surprise'])
    fear_list = list(df['Fear'])
    angry_crossing = []
    happy_crossing = []
    disgust_crossing = []
    sad_crossing = []
    surprise_crossing = []
    fear_crossing = []

    for i in range(len(neutral_list)):
        try:
            neutral_a = neutral_list[i]
            angry_a = angry_list[i]
            happy_a = happy_list[i]
            disgust_a = disgust_list[i]
            sad_a = sad_list[i]
            surprise_a = surprise_list[i]
            fear_a = fear_list[i]

            # Angry part section
            if neutral_a > angry_a:
                angry_crossing.append(1)
            else:
                angry_crossing.append(0)

            # Happy part section
            if neutral_a > happy_a:
                happy_crossing.append(1)
            else:
                happy_crossing.append(0)

            # Disgust part section
            if neutral_a > disgust_a:
                disgust_crossing.append(1)
            else:
                disgust_crossing.append(0)

            # Sad part section
            if neutral_a > sad_a:
                sad_crossing.append(1)
            else:
                sad_crossing.append(0)

            # Surprise part section
            if neutral_a > surprise_a:
                surprise_crossing.append(1)
            else:
                surprise_crossing.append(0)

            # Fear part section
            if neutral_a > fear_a:
                fear_crossing.append(1)
            else:
                fear_crossing.append(0)

        except:
            continue

    # Generating the textual data
    total_crossings = 0
    final_list = [angry_crossing, happy_crossing, disgust_crossing, sad_crossing, surprise_crossing, fear_crossing]
    for i in final_list:
        for j in range(len(i)):
            try:
                alfa = [i[j], i[j + 1]]
                if alfa == [1, 0]:
                    total_crossings += 1
                else:
                    continue
            except:
                continue

    # Determine attention status
    if neutral_percentage > 0.5:
        if total_crossings > 5:
            attention_status = "The person is not paying attention. The number of disturbances happened in the class were {} \n".format(total_crossings)
        else:
            attention_status = "The person is paying attention \n"
    else:
        attention_status = "The person is not paying attention. The number of disturbances happened in the class were {}".format(total_crossings)

    return attention_status


# ===================================================================================================

def get_current_time():
    tz = pytz.timezone('Asia/Kolkata')  # Set the timezone to India
    current_time = datetime.now(tz)
    return current_time.strftime('%Y-%m-%d %H:%M:%S')

def insert_emotion_data(angry, disgust, fear, happy, sad, surprise, neutral):
    # Get the current time
    time = get_current_time()

    # Establish a connection to the MySQL database
    connector = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_anshu",
        password="t3guc77PZ?GnE9n",
        database="freedb_hackathon_ai"
    )

    # Create a cursor object to execute SQL queries
    cursor = connector.cursor()

    # SQL query to insert data into the "emotion" table
    insert_query = """
    INSERT INTO emotion (time, angry, disgust, fear, happy, sad, surprise, neutral)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Data to be inserted
    data = (time, angry, disgust, fear, happy, sad, surprise, neutral)

    try:
        # Execute the SQL query to insert data
        cursor.execute(insert_query, data)

        # Commit the changes to the database
        connector.commit()
        print("Data inserted successfully!")
    except Exception as e:
        # Rollback the changes if an error occurs
        connector.rollback()
        print(f"Error: {str(e)}")

    # Close the cursor and the database connection
    cursor.close()
    connector.close()


# -------------------------------------------[PLOTTING DATA] ------------------------------------------- #


import mysql.connector
import pandas as pd
import plotly.graph_objects as go

def create_emotion_plot():
    # Connect to the database
    connector = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_anshu",
        password="t3guc77PZ?GnE9n",
        database="freedb_hackathon_ai"
    )
    
    # Create a cursor to execute queries
    cursor = connector.cursor()
    
    # Execute the query to retrieve emotion data
    query = "SELECT * FROM emotion"
    cursor.execute(query)
    
    # Fetch all rows of the result
    rows = cursor.fetchall()
    
    # Close the database connection
    cursor.close()
    connector.close()
    
    # Process the data
    timestamps = []
    emotions = []
    for row in rows:
        timestamps.append(row[0])
        emotions.append(row[1:])
    
    # Convert timestamps to datetime objects
    timestamps = pd.to_datetime(timestamps)
    
    # Convert emotions to a DataFrame
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    df = pd.DataFrame(emotions, columns=emotion_labels)
    # changing datatype
    df = df.astype('float64')

    # Create the interactive plot using Plotly
    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(go.Scatter(x=timestamps, y=df[column], name=column, mode='lines', line=dict(width=1)))
    
    # Set plot title and labels
    fig.update_layout(
        title='Emotions Over Time',
        xaxis_title='Timestamp',
        yaxis_title='Intensity',
        template="plotly_dark"
    )
    
    # Convert plot to HTML string
    plot_html = fig.to_html(full_html=False)
    
    # Perform algorithm using the DataFrame
    return plot_html, df

# ============================ main_