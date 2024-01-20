import argparse
from pypdf import PdfReader

def parse_pdf(file_path):
    # Read credit card statement pdf into a string
    reader = PdfReader(args.file_path)
    pages = ""
    for page in reader.pages:
        pages += page.extract_text() + "\n"

    # Finds transactions in the string and parses them into a list of 
    # (transaction_description, transaction_amount)
    lines = pages.split("\n")
    result = []
    for i, line in enumerate(lines):
        if (line.startswith("Ref No.")):
            transaction_description = lines[i-1][14:]
            transaction_amount = line[33:]
            result.append((transaction_description, transaction_amount))

    return result

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Parses credit card statement pdf')
    arg_parser.add_argument('-f', dest='file_path', required=True, help='The path to the pdf')
    args = arg_parser.parse_args()

    print(*parse_pdf(args.file_path), sep="\n")
