import mysql.connector
import pandas as pd


def connect_to_mysql(host, user, password, database):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def get_titles_from_url_table(host, user, password, database):
    connection = connect_to_mysql(host, user, password, database)
    cursor = connection.cursor()

    try:
        # Fetch titles from the "URL" table
        select_query = "SELECT title FROM URL"
        cursor.execute(select_query)
        data = cursor.fetchall()

        # Convert the data to a list of titles
        titles = [row[0] for row in data]

        return titles

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the connection
        cursor.close()
        connection.close()


def split_and_store_keywords(host="localhost", user="root", password="", database="project"):
    connection = connect_to_mysql(host, user, password, database)
    cursor = connection.cursor()

    try:
        # Get titles from the "URL" table
        titles = get_titles_from_url_table(host, user, password, database)

        if titles:
            # Split titles into keywords and store them in the "keywords" table
            for title in titles:
                keywords = title.split()

                # Insert keywords into the "keywords" table
                for keyword in keywords:
                    # Check if the keyword already exists in the table
                    select_query = "SELECT * FROM keywords WHERE keyword = %s"
                    cursor.execute(select_query, (keyword,))
                    existing_data = cursor.fetchall()

                    if not existing_data:
                        # If the keyword doesn't exist, insert it into the table
                        insert_query = "INSERT INTO keywords (keyword, occurrence) VALUES (%s, 1)"
                        cursor.execute(insert_query, (keyword,))
                    else:
                        # If the keyword already exists, update its occurrence count
                        update_query = "UPDATE keywords SET occurrence = occurrence + 1 WHERE keyword = %s"
                        cursor.execute(update_query, (keyword,))

            # Commit the changes
            connection.commit()

            print("Keywords stored in the 'keywords' table successfully.")

        else:
            print("No titles found in the 'URL' table.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        cursor.close()
        connection.close()


def get_keywords_as_dataframe(host="localhost", user="root", password="", database="project"):
    connection = connect_to_mysql(host, user, password, database)
    cursor = connection.cursor()

    try:
        # Fetch keywords from the "keywords" table
        select_query = "SELECT * FROM keywords"
        cursor.execute(select_query)
        data = cursor.fetchall()

        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame(data, columns=["id", "keyword", "occurrence"])

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the connection
        cursor.close()
        connection.close()
