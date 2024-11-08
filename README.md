# API Audit

This script scans PHP files in a specified directory (and its sub-directories) to identify API URLs containing `://api.`. 

It retrieves any associated request headers and body data, saving the results to a timestamped CSV file in a `reports`folder. 

This tool helps developers and security analysts understand API interactions within their codebase.

## Features

- Scans all PHP files in the specified directory and subdirectories
- Identifies and records API URLs containing `://api.`
- Captures associated request headers and body data (if any)
- Saves results to a timestamped CSV file in a `reports` folder
- Provides a real-time progress bar and summary of results after completion

## Requirements

- Python 3.x
- `tqdm` library for the progress bar (install with `pip install tqdm`)

## Installation

1. Clone or download this repository to your local machine.
2. Ensure Python 3.x is installed on your system.
3. Install the `tqdm` library for the progress bar by running:
    ```
    pip install tqdm
    ```

## Usage

1. **Run the Script**

Open a terminal, navigate to the directory containing the script, and execute:
    ```
    python3 apiAudit.py
    ```

2. **Progress Bar and Output**

    - While the script runs, a progress bar will display the number of PHP files scanned, giving you real-time feedback on the process.
    - Once complete, a summary will appear, indicating:
        - Total files scanned
        - PHP files with API URLs found
        - Unique API URLs identified
        - Execution time
3. **CSV Report**

    - Results are saved in a CSV file in the `reports` folder.
    - The filename is timestamped for easy identification, e.g., `api_urls_with_headers_and_body_20241107_201000.csv`.
    - The CSV includes the following columns:
        - **File Path**: Path of the PHP file containing the API URL
        - **API URL**: The complete API URL
        - **Request Headers**: Captured headers associated with the API call
        - **Request Body**: Captured body data associated with the API call

## Example Output

After scanning, the summary might look like this:
```
    --- Scan Summary ---
    Total files scanned: 120
    Total PHP files with API URLs found: 15
    Total unique API URLs identified: 25
    Time taken: 10.25 seconds
    Data successfully saved to reports/api_urls_with_headers_and_body_20241107_201000.csv
```

## Troubleshooting

- **Encoding Errors**: Certain files may cause encoding errors, which are automatically suppressed to prevent script interruption.
- **Slow Performance**: For large directories, the scan may take longer. The progress bar will help you track progress in real time.

## License

This project is licensed under the MIT License.