# bank statement parser

quick little script that parses your credit card statement pdf files into a csv file in the format
`(date, description, amount, category)` so that you can upload them to your google sheet for further
analysis

to categorise transactions, add your own definition in `config.json` (sample is provided)

obviously there's a lot of variance between the pdf files from different banks, so for now it only
works for UOB statements since that is my primary bank :)

feel free to contribute!

### usage

1.  install dependencies: `pip install -r requirements.txt`
1.  add your bank's credit card statement pdf files into `data/pdf` folder
1.  run the script: `python parse.py`
1.  csv files are output to `data/csv` folder
