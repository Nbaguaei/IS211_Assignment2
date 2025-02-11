import argparse
import urllib.request
import logging
import datetime
import csv

def downloadData(url):
    """Downloads the data from the given URL."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        logging.error(f"Error downloading data: {e}")
        return None

def processData(file_content):
    """Processes the CSV file content and returns a dictionary mapping ID to (name, birthday)."""
    personData = {}
    logger = logging.getLogger("assignment2")
    lines = file_content.splitlines()
    reader = csv.reader(lines)
    next(reader)  
    
    for line_num, row in enumerate(reader, start=2):  
        try:
            person_id, name, birthday_str = row
            birthday = datetime.datetime.strptime(birthday_str, "%d/%m/%Y").date()
            personData[int(person_id)] = (name, birthday)
        except (ValueError, IndexError):
            logger.error(f"Error processing line #{line_num} for ID #{row[0] if row else 'UNKNOWN'}")
    
    return personData

def displayPerson(person_id, personData):
    """Displays a person's name and formatted birthday given their ID."""
    if person_id in personData:
        name, birthday = personData[person_id]
        print(f"Person #{person_id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that ID.")

def setup_logger():
    """Sets up logging to write errors to 'errors.log'."""
    logging.basicConfig(filename='errors.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def main(url):
    """Main program function."""
    setup_logger()
    
    csvData = downloadData(url)
    if not csvData:
        print("Failed to retrieve data. Exiting.")
        return
    
    personData = processData(csvData)
    
    while True:
        try:
            user_input = input("Enter an ID to lookup (0 or negative to exit): ")
            user_id = int(user_input)
            if user_id <= 0:
                break
            displayPerson(user_id, personData)
        except ValueError:
            print("Invalid input. Please enter a valid numeric ID.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
