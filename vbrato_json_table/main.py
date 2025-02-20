import csv
import json
import sys

DATA_FOLDER = './data/'

# Function to capitalize the first letter of each word
def capitalize_label(label):
    return ' '.join(word.capitalize() for word in label.split())

def main():

    # Default file names
    input_file = 'input_data.csv'
    output_file = 'output_data.json'

    # Check if command-line arguments are provided
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    input_file = DATA_FOLDER + input_file
    output_file = DATA_FOLDER + output_file

    # Read the CSV data and convert it to JSON
    table_content = []
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table_content.append({
                "code": row['genre'].lower(),
                "label": capitalize_label(row['genre'])
            })

    # Write the JSON data to the output file
    output_data = {
        "tableName": "genres",
        "tableContent": table_content
    }
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(output_data, jsonfile, indent=4)

    print(f"Data converted and saved to {output_file}")

if __name__ == "__main__":
    main()
