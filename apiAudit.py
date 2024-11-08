import os
import re
import csv
from datetime import datetime
import time
from tqdm import tqdm  # Progress bar library

# Define the function to scan PHP files for URLs with '://api.', associated headers, and request body
def scan_php_files_for_api_urls(directory='.'):
    """
    Scans PHP files in the specified directory and subdirectories for URLs containing '://api.'.
    Captures any headers and body data related to the API calls.
    Returns a list of tuples with file paths, matched URLs, headers, and body data.
    
    Parameters:
        directory (str): The directory path to start scanning from. Defaults to the current directory.

    Returns:
        tuple: A list of API data (file path, URL, headers, body data), and the count of files scanned.
    """
    api_data = set()  # Using a set to store unique URLs, headers, and bodies
    files_scanned = 0  # Counter for total PHP files scanned
    # Regular expression to match full URLs containing '://api.'
    api_url_pattern = re.compile(r'http[s]?://api\.[\w.-]+(?:/[^\s\'"]*)?')
    
    # Regular expression to match headers in API request functions
    header_pattern = re.compile(
        r'(?:(?:wp_remote_get|wp_remote_post|curl_setopt|file_get_contents)\s*\([^)]*?headers\s*=>\s*\[.*?\])',
        re.DOTALL
    )
    # Regular expression to match specific headers like 'User-Agent' or 'Content-Type'
    specific_header_pattern = re.compile(
        r'\'(?:User-Agent|Content-Type|Authorization)\'\s*=>\s*[\'"].*?[\'"]',
        re.DOTALL
    )
    # Regular expression to match body data in API request functions
    body_pattern = re.compile(
        r'\'body\'\s*=>\s*(\{.*?\}|\[.*?\]|\'.*?\'|".*?")',
        re.DOTALL
    )

    # Collect all PHP files in advance for progress tracking
    php_files = [os.path.join(root, file_name)
                 for root, _, files in os.walk(directory)
                 for file_name in files if file_name.endswith('.php')]

    # Initialize progress bar with the total count of PHP files
    with tqdm(total=len(php_files), desc="Scanning PHP files", unit="file") as progress_bar:
        for file_path in php_files:
            files_scanned += 1
            
            try:
                # Open and read the file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Find all matching URLs in the file content
                matches = api_url_pattern.findall(content)
                for url in matches:
                    # Find headers associated with this API call
                    headers = header_pattern.findall(content) or specific_header_pattern.findall(content)
                    headers = "; ".join(headers) if headers else "No headers found"
                    
                    # Find body data associated with this API call
                    bodies = body_pattern.findall(content)
                    body_data = "; ".join(bodies) if bodies else "No body data found"
                    
                    # Add each URL, headers, and body data as unique entries in the set
                    api_data.add((file_path, url, headers, body_data))
            
            except UnicodeDecodeError:
                # Ignore encoding errors without printing them
                continue
            
            # Update the progress bar for each file scanned
            progress_bar.update(1)
    
    return list(api_data), files_scanned

# Define the function to save results to a CSV file in a "reports" folder with a timestamp
def save_to_csv(data, csv_filename=None):
    """
    Saves the scanned data to a CSV file in a "reports" folder with a timestamped filename.

    Parameters:
        data (list of tuple): Data to write to CSV; each tuple contains file path, URL, headers, and body data.
        csv_filename (str, optional): The name of the CSV file to save to. If None, a timestamped filename will be used.
    """
    # Ensure the "reports" directory exists
    os.makedirs("reports", exist_ok=True)

    # Generate a timestamped filename if not provided
    if not csv_filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'reports/api_urls_with_headers_and_body_{timestamp}.csv'
    
    try:
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['File Path', 'API URL', 'Request Headers', 'Request Body'])
            writer.writerows(data)
        print(f"Data successfully saved to {csv_filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Main script execution
if __name__ == "__main__":
    start_time = time.time()
    print("Starting scan...")

    # Scan for API URLs, headers, and body data in PHP files
    api_data, files_scanned = scan_php_files_for_api_urls()
    
    # Save results to CSV if any URLs are found
    if api_data:
        save_to_csv(api_data)
    else:
        print("No API URLs, headers, or body data found.")
    
    # Display summary information
    end_time = time.time()
    execution_time = end_time - start_time
    print("\n--- Scan Summary ---")
    print(f"Total files scanned: {files_scanned}")
    print(f"Total PHP files with API URLs found: {len(api_data)}")
    print(f"Total unique API URLs identified: {len({url for _, url, _, _ in api_data})}")
    print(f"Time taken: {execution_time:.2f} seconds")
