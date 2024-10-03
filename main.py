import platform
import pandas as pd
import camelot
import time
from enum import Enum
import re
from pathlib import Path

# Constants
HEADERS_TO_REMOVE = ['Date', 'Tarikh']
DATE_PATTERN = re.compile(r'\d{1,2} [A-Za-z]{3}')  # Matches date format like '9 Sep'
TIME_PATTERN = re.compile(r'\d{1,2}:\d{2} [APMapm]{2}')  # Matches time like '02:10 PM'

class SystemPlatform(Enum):
    Windows = 1
    Darwin = 2
    Linux = 3

def get_file_paths():
    """Get the PDF and CSV paths based on the operating system."""
    time_str = time.strftime("%Y%m%d_%H%M%S")

    base_dir = Path('./data') if platform.system() in [SystemPlatform.Darwin.name, SystemPlatform.Linux.name] else Path('.\\data')
    output_dir = Path('./output') if platform.system() in [SystemPlatform.Darwin.name, SystemPlatform.Linux.name] else Path('.\\output')

    pdf_file = base_dir / 'gxbank-statement.pdf'
    csv_file = output_dir / f'gxbank_statement_{time_str}.csv'

    return pdf_file, csv_file

def merge_rows_and_remove_duplicates(df):
    """
    Merges rows that contain only the time with the previous row that contains the date,
    and removes duplicate headers.
    """
    merged_data = []
    current_row = None
    first_header_found = False

    for index, row in df.iterrows():
        # Check and remove duplicate headers
        if row['Date'] in HEADERS_TO_REMOVE:
            if not first_header_found:
                first_header_found = True  # Keep the first header
            else:
                continue  # Skip any subsequent headers

        # Check if the row contains a valid date or time
        if pd.notna(row['Date']) and (DATE_PATTERN.match(row['Date']) or TIME_PATTERN.match(row['Date'])):
            if TIME_PATTERN.match(row['Date']):
                current_row['Date'] = f"{current_row['Date']} {row['Date']}"  # Merge Date and Time
            else:
                if current_row is not None:
                    merged_data.append(current_row)
                current_row = row.copy()  # Start a new row with the new Date
        elif current_row is not None and pd.notna(row['Transaction description']) and current_row['Transaction description'].strip() == "":
            current_row['Transaction description'] = row['Transaction description'].strip()

    if current_row is not None:
        merged_data.append(current_row)

    return pd.DataFrame(merged_data)

def clean_and_export(df, csv_path):
    """Clean the dataframe, merge rows, and export to CSV."""
    # Merge rows and remove duplicates
    df_merged = merge_rows_and_remove_duplicates(df)

    # Remove redundant headers
    df_merged = df_merged[df_merged['Date'] != 'Date']

    # Clean up the 'Money in (RM)' and 'Interest earned (RM)' columns
    df_merged['Money in (RM)'] = df_merged['Money in (RM)'].replace('', '0').str.replace(',', '').astype(float)
    df_merged['Interest earned (RM)'] = df_merged['Interest earned (RM)'].replace('', '0').str.replace(',', '').astype(float)

    # Merge 'Interest earned (RM)' into 'Money in (RM)'
    df_merged['Money in (RM)'] += df_merged['Interest earned (RM)']

    # Drop the 'Interest earned (RM)' column
    df_merged.drop(columns=['Interest earned (RM)'], inplace=True)

    # Filter rows that contain valid Date-Time
    df_filtered = df_merged.dropna(subset=['Date'])

    # Export to CSV
    df_filtered.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"Exported data to: {csv_path}")

    return df_filtered

if __name__ == "__main__":
    try:
        # Get the file paths
        pdf_path, csv_path = get_file_paths()

        # Extract tables from the PDF using Camelot
        tables = camelot.read_pdf(str(pdf_path), pages='all', flavor='stream')

        # Concatenate all tables into a single DataFrame
        df = pd.concat([table.df for table in tables], ignore_index=True)

        # Reassign proper column names
        df.columns = ['Date', 'Transaction description', 'Money in (RM)', 'Money out (RM)', 'Interest earned (RM)', 'Closing balance (RM)']

        # Clean, merge rows, and export to CSV
        cleaned_data = clean_and_export(df, csv_path)

        # Print first few rows for validation
        print(cleaned_data.head())

    except Exception as e:
        print(f"An error occurred: {e}")
