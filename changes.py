import mysql.connector
import pandas as pd


def connect_to_mysql(host="localhost", user="root", password="", database="project"):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def insert_changes_into_table(old_keyword="", new_keyword=""):
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # Insert the changes into the "changes" table
        insert_query = "INSERT INTO changes (old_keyword, new_keyword) VALUES (%s, %s)"
        values = (old_keyword, new_keyword)
        cursor.execute(insert_query, values)

        # Commit the changes
        connection.commit()

        print(f"Changes '{old_keyword}' to '{new_keyword}' inserted into 'changes' table successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        cursor.close()
        connection.close()


def get_changes_table_as_dataframe():
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # Fetch data from the "changes" table
        select_query = "SELECT * FROM changes"
        cursor.execute(select_query)
        data = cursor.fetchall()

        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame(data, columns=["id", "old_keyword", "new_keyword"])

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the connection
        cursor.close()
        connection.close()
