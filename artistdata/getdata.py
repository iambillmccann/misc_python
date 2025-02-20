import mysql.connector
from contextlib import closing
from env import PLANETSCALE_USER, PLANETSCALE_PASSWORD
import json
import time

# Define the connection parameters
config = {
    "user": PLANETSCALE_USER,
    "password": PLANETSCALE_PASSWORD,
    "host": "aws.connect.psdb.cloud",
    "database": "vbrato",
    "ssl_ca": "./ca-certificates.crt",  # Relative path to the SSL certificate
    "connect_timeout": 300,  # 5 minutes
    "read_timeout": 300,  # 5 minutes
}


# Function to establish a connection to the MySQL database with retries
def connect_with_retries(config, retries=3, delay=5):
    for attempt in range(retries):
        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Successfully connected to the database")
                return connection
        except mysql.connector.Error as err:
            print(f"Connection attempt {attempt + 1} failed: {err}")
            time.sleep(delay)
    raise Exception("Failed to connect to the database after multiple attempts")


def fetch_data_to_file(output_file):
    # Define the chunk size
    chunk_size = 5000

    # Initialize the starting id
    start_id = 0

    with open(output_file, "w") as f:
        f.write("[")  # Start the JSON array

        first_record = True

        while True:
            try:
                # Establish a connection to the MySQL database
                with closing(connect_with_retries(config)) as conn:
                    # Define the query to fetch records in chunks using the id column with BETWEEN clause
                    query = f"""
                    SELECT artistData
                    FROM artist
                    WHERE artistData ->> '$.spotify.identifier' IS NOT NULL
                    AND id BETWEEN {start_id} AND {start_id + chunk_size - 1}
                    ORDER BY id;
                    """

                    # Execute the query
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    if not rows:
                        break

                    for row in rows:
                        if not first_record:
                            f.write(",\n")
                        json.dump(row["artistData"], f)
                        first_record = False

                    # Update the starting id for the next chunk
                    start_id += chunk_size
                    if start_id % 20000 == 0:
                        print(f"Processed {start_id} records")

                    # Add a delay between each chunk retrieval if necessary
                    # time.sleep(1)
            except mysql.connector.Error as err:
                print(f"Query failed: {err}")
                time.sleep(5)  # Wait before retrying

        f.write("]")  # End the JSON array
        print(f"Data written to {output_file}")


if __name__ == "__main__":
    output_file = "artist_data.json"
    fetch_data_to_file(output_file)
