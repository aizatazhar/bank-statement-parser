import argparse
import csv
import json
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

def write_csv(tuples, file_name):
    with open(file_name, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Date", "Description", "Amount", "Category"])
        csv_writer.writerows(tuples)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parses credit card statement pdf")
    arg_parser.add_argument("-f", dest="file_path", required=True, help="The path to the pdf")
    args = arg_parser.parse_args()
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
 
    transactions = parse_pdf(args.file_path, config["categories"])

    write_csv(transactions, f"{args.file_path[:-4]}.csv")
