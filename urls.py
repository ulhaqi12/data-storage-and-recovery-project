import mysql.connector
import pandas as pd

from scraper import scrape_title


def connect_to_mysql(host, user, password, database):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def get_url_table_as_dataframe(host="localhost", user="root", password="", database="project"):
    connection = connect_to_mysql(host, user, password, database)
    cursor = connection.cursor()

    # Fetch all rows from the "URL" table
    select_query = "SELECT * FROM URL"
    cursor.execute(select_query)
    data = cursor.fetchall()

    # Get column names
    column_names = [desc[0] for desc in cursor.description]

    # Create a DataFrame
    df = pd.DataFrame(data, columns=column_names)

    # Close the connection
    cursor.close()
    connection.close()

    return df


def insert_url_entry(url="", title="", scraped=False, splitted=False):
    # Replace these values with your MySQL server credentials
    host = "localhost"
    user = "root"
    password = ""
    database = "project"

    connection = connect_to_mysql(host, user, password, database)
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO URL (url, title, scraped, splitted)
    VALUES (%s, %s, %s, %s)
    """
    values = (url, title, scraped, splitted)
    cursor.execute(insert_query, values)

    connection.commit()
    cursor.close()
    connection.close()

    print("URL entry added successfully.")


def get_not_scrapped_urls_from_database(host="localhost", user="root", password="", database='project'):
    connection = connect_to_mysql(host, user, password, database)
    cursor = connection.cursor()

    try:
        # Fetch the URLs from the "URL" table
        select_query = "SELECT url FROM URL WHERE  scraped=0"
        cursor.execute(select_query)
        data = cursor.fetchall()

        # Convert the data to a list of URLs
        url_list = [row[0] for row in data]

        return url_list

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the connection
        cursor.close()
        connection.close()


def scrape_all_urls(host="localhost", user="root", password="", database="project"):
    urls = get_not_scrapped_urls_from_database()
    print(urls)

    url_title_dict = {}

    for url in urls:
        url_title_dict[url] = scrape_title(url)

    print(url_title_dict)

    connection = connect_to_mysql(host, user, password, database)
    cursor = connection.cursor()

    try:
        for url, title in url_title_dict.items():
            # Update the title in the "URL" table for the specific URL
            update_query = "UPDATE URL SET title = %s, scraped=True WHERE url = %s"
            values = (title, url)
            cursor.execute(update_query, values)

        # Commit the changes
        connection.commit()

        print("Titles updated successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        cursor.close()
        connection.close()
