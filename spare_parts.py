import mysql.connector
from datetime import datetime
import pytz

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
