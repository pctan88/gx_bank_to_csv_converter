# GX Bank Statement to CSV Converter

This Python project extracts and processes GXBank statements from PDF format and converts them into a cleaned and structured CSV file. The CSV file is suitable for further data analysis or integration into other systems.

## Features

- Extracts tables from the GXBank PDF statement using Camelot.
- Cleans and processes the statement data by merging date and time rows into one.
- Filters and retains only relevant transaction rows, excluding redundant information (e.g., transaction types or remarks).
- Merges the "Interest earned" into the "Money in (RM)" column for a simpler credit/debit structure.
- Exports the cleaned data to a properly formatted CSV file.
- Can process multiple pages from the PDF.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.7+** installed on your machine.
- **pip** for managing Python packages.
- Install the required Python libraries by running:
  ```bash
  pip install pandas camelot-py[cv] xlsxwriter
  ```

  > `camelot-py[cv]` requires additional dependencies, including Ghostscript, which you need to install separately for Camelot to work with PDFs.

### Installing Ghostscript (for Camelot)

For **MacOS** (using Homebrew):
```bash
brew install ghostscript
```

For **Linux** (using apt):
```bash
sudo apt install ghostscript
```

For **Windows**, download the appropriate installer from the [Ghostscript website](https://www.ghostscript.com/download/gsdnld.html) and follow the installation instructions.

## How to Use

1. **Place the PDF file** in the `./data/` directory. By default, the script looks for a file named `gxbank-statement.pdf`. You can modify this in the script as needed.
   
2. **Run the script**:
   ```bash
   python3 main.py
   ```

3. The processed CSV will be saved in the `./output/` directory with a timestamp in its filename.

### Example

If your bank statement PDF is named `gxbank-statement.pdf`, running the script will generate a CSV file in the following path:
```
./output/gxbank_statement_YYYYMMDD_HHMMSS.csv
```

## Code Structure

- **`main.py`**: The main script that handles PDF extraction, data cleaning, merging of rows, and CSV export.
- **`/data/`**: The directory where the PDF statement file is stored.
- **`/output/`**: The directory where the output CSV files will be saved.

## Code Workflow

1. **PDF Extraction**: The tables are extracted from the PDF using Camelot (`flavor='stream'`).
2. **Data Processing**: 
    - Date and time rows are merged.
    - Duplicate headers are removed.
    - "Interest earned" is added to "Money in (RM)" for simplification.
3. **Export**: The cleaned data is saved in CSV format.
   
## Known Issues

- The current version is tested with GXBank statements. If you are using it for a different bank, the script may need modifications to handle different table structures or formats.
- Make sure the PDF statements are clear and well-structured for Camelot to extract tables correctly.

## Contributing

If you'd like to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

### Notes:
- **README File Location**: Save this README file in the root of your project directory as `README.md`.
- **Keep It Simple**: If any specific instructions or setup steps apply to your project, make sure to detail those in the appropriate sections.

Let me know if you need any changes or additional sections in the README!
