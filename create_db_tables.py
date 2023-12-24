import mysql.connector

def connect_to_mysql(host, user, password):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS project")
    cursor.execute("USE project")

def create_url_table(cursor):
    create_url_table_query = """
    CREATE TABLE IF NOT EXISTS URL (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url VARCHAR(255) NOT NULL,
        title VARCHAR(255),
        scraped BOOLEAN,
        splitted BOOLEAN
    )
    """
    cursor.execute(create_url_table_query)

def create_keywords_table(cursor):
    create_keywords_table_query = """
    CREATE TABLE IF NOT EXISTS keywords (
        id INT AUTO_INCREMENT PRIMARY KEY,
        keyword VARCHAR(255) NOT NULL,
        occurrence INT
    )
    """
    cursor.execute(create_keywords_table_query)

def create_superfluous_table(cursor):
    create_superfluous_table_query = """
    CREATE TABLE IF NOT EXISTS superfluous (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(255) NOT NULL
    )
    """
    cursor.execute(create_superfluous_table_query)

def create_changes_table(cursor):
    create_changes_table_query = """
    CREATE TABLE IF NOT EXISTS changes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        old_keyword VARCHAR(255) NOT NULL,
        new_keyword VARCHAR(255) NOT NULL
    )
    """
    cursor.execute(create_changes_table_query)


def main():
    # Replace these values with your MySQL server credentials
    host = "localhost"
    user = "root"
    password = ""

    connection = connect_to_mysql(host, user, password)
    cursor = connection.cursor()

    create_database(cursor)
    create_url_table(cursor)
    create_keywords_table(cursor)
    create_superfluous_table(cursor)
    create_changes_table(cursor)

    connection.commit()
    cursor.close()
    connection.close()

    print("Databases and tables created successfully.")


if __name__ == "__main__":
    main()
