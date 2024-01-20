import csv
import json
import glob
import os
from pypdf import PdfReader

def parse_pdf(file_path, categories_map):
    # Read credit card statement pdf into a string
    reader = PdfReader(file_path)
    pages = ""
    for page in reader.pages:
        pages += page.extract_text() + "\n"

    # Finds transactions in the string and parses them into a list of tuples
    # (date, description, amount, category)
    lines = pages.split("\n")
    result = []
    for i, line in enumerate(lines):
        if (line.startswith("Ref No.")):
            date = lines[i-1][:6]
            description = lines[i-1][14:]
            amount = line[33:]

            # Categorise the transaction
            category = "unknown"
            for categoryy, keywords in categories_map.items():
                for keyword in keywords:
                    if keyword.lower() in description.lower():
                        category = categoryy
                        break

            result.append((date, description, amount, category))

    return result

def write_csv(tuples, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Date", "Description", "Amount", "Category"])
        csv_writer.writerows(tuples)

if __name__ == "__main__":
    pdf_file_paths = glob.glob("data/pdf/*.pdf")
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    
    for pdf_file_path in pdf_file_paths:
        pdf_file_name = os.path.basename(pdf_file_path)[:-4]
        transactions = parse_pdf(pdf_file_path, config["categories"])
        write_csv(transactions, f"data/csv/{pdf_file_name}.csv")
