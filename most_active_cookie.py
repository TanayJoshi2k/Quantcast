import argparse
from datetime import datetime
import os
import logging


# Set up logging directory
LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Generate log file name with timestamp
log_file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
log_file_path = os.path.join(LOGS_DIR, log_file_name)

# Set up logging configuration
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(levelname)s: %(message)s')


def log_and_raise_error(error_message, exception_type):
    """Logs an error message and raises an exception.

    Args:
        error_message (str): The error message to log and raise.
        exception_type (Exception): The type of exception to raise.
    """
    logging.exception(error_message)
    raise exception_type(error_message)


def parse_csv_line(line):
    """Parses a line from a CSV file.

    Args:
        line (str): The line to parse from the CSV file.

    Returns:
        tuple: A tuple containing the cookie and timestamp parsed from the line.
    """
    try:
        cookie, timestamp = line.strip().split(',')
        return cookie, timestamp
    except ValueError:
        log_and_raise_error("Invalid CSV format", ValueError)


def find_most_active_cookie(file_path, target_date):
    """Finds the most active cookie for a specified day in a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        target_date (str): The target date in the format YYYY-MM-DD.

    Returns:
        list: A list of most active cookies for the specified day.
    """

    # Check if the file path ends with '.csv'
    if not file_path.endswith('.csv'):
        log_and_raise_error("File must have a '.csv' extension", ValueError)

    # Check if the file exists
    if not os.path.exists(file_path):
        log_and_raise_error("File does not exist", FileNotFoundError)

    try:
        # Parse the target date
        target_date = datetime.fromisoformat(target_date).date()
    except TypeError:
        log_and_raise_error(
            "Invalid date format. Please provide the date in the format YYYY-MM-DD.", TypeError)

    except ValueError:
        log_and_raise_error(
            "Invalid date format. Please provide the date in the format YYYY-MM-DD.", ValueError)

    # Dictionary to store cookie frequencies
    cookie_frequency = {}
    max_frequency = 0
    total_lines_processed = 0

    with open(file_path, 'r') as file:
        logging.info("File opened successfully")
        cookies_data = file.readlines()

        # Iterate through each line in the CSV file
        for line in cookies_data[1:]:
            total_lines_processed += 1
            cookie, timestamp = parse_csv_line(line)
            cookie_date = datetime.fromisoformat(timestamp).date()

            # Check if the cookie date matches the target date
            if cookie_date == target_date:
                # Increment the frequency of the cookie
                cookie_frequency[cookie] = cookie_frequency.get(cookie, 0) + 1
                max_frequency = max(max_frequency, cookie_frequency[cookie])

    # Log total lines processed
    logging.info("Total lines processed from CSV file: %d",
                 total_lines_processed)

    # If no cookies were found for the target date, return an empty list
    if not cookie_frequency:
        return []

    # Find the cookies with the maximum frequency
    most_active_cookies = [cookie for cookie,
                           frequency in cookie_frequency.items() if frequency == max_frequency]
    return most_active_cookies


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Find most active cookie for a specified day.')

    parser.add_argument(
        'file_path', type=str, help='Path to the CSV file')

    parser.add_argument('-d', '--date', type=str,
                        help='Date in the format YYYY-MM-DD', required=True)

    args = parser.parse_args()

    # Extract file path and target date from command-line arguments
    target_date, file_path = args.date, args.file_path

    # Log start of processing
    logging.info("Starting processing")

    # Find the most active cookies for the target date
    active_cookies = find_most_active_cookie(file_path, target_date)

    # Log end of processing
    logging.info("End of processing")

    if not active_cookies:
        print("No active cookies found for date:", target_date)
        logging.info("No active cookies found for date: %s", target_date)
    else:
        logging.info("Most active cookies for date %s: %s",
                     target_date, ', '.join(active_cookies))

        print("="*len(active_cookies[0]))

        # Print each active cookie on a separate line
        for cookie in active_cookies:
            print(cookie)
