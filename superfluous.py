import mysql.connector
import pandas as pd


def connect_to_mysql(host="localhost", user="root", password="", database='project'):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def insert_word_into_superfluous(word=""):
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # Insert the word into the "superfluous" table
        insert_query = "INSERT INTO superfluous (word) VALUES (%s)"
        values = (word,)
        cursor.execute(insert_query, values)

        # Commit the changes
        connection.commit()

        print(f"Word '{word}' inserted into 'superfluous' table successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        cursor.close()
        connection.close()


def get_superfluous_words_as_dataframe():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # Fetch the superfluous words from the "superfluous" table
        select_query = "SELECT word FROM superfluous"
        cursor.execute(select_query)
        data = cursor.fetchall()

        # Convert the data to a list of superfluous words
        superfluous_words = [row[0] for row in data]

        # Create a DataFrame
        df = pd.DataFrame({"Superfluous Word": superfluous_words})

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the connection
        cursor.close()
        connection.close()
