# bank statement parser

quick little script that parses your credit card statement pdf files into a csv file in the format
`[date, description, amount, category]` so that you can upload them to your google sheet for further
analysis

to categorise transactions, add your own definition in `config.json` (sample is provided)

obviously there's a lot of variance between the pdf files from different banks, so for now it only
works for UOB statements since that is my primary bank :)

feel free to contribute!

### usage

#### optional: google sheets setup

follow these steps if you want to fully automate uploading the output csv files to your own
google sheets

1. [create a google cloud project](https://developers.google.com/workspace/guides/create-project)
   and give your project a name, e.g. `bank-statement-parser`
1. [enable google sheets API](https://console.cloud.google.com/workspace-api/products) for your
   project
1. follow instructions under [Configure the OAuth consent screen](https://developers.google.com/sheets/api/quickstart/python#configure_the_oauth_consent_screen) section
1. follow instructions under [Authorize credentials for a desktop application](https://developers.google.com/sheets/api/quickstart/python#authorize_credentials_for_a_desktop_application) section.
   after you have downloaded the JSON file and renamed it as `credentials.json`, move it to the root
   of this directory
1. In `config.json`, replace the `"google sheets id"` key with your own google sheet id
   (obtained from the URL)

#### running the script

1.  install dependencies: `pip install -r requirements.txt`
1.  add your bank's credit card statement pdf files into `data/pdf` folder
1.  if you did not set up google sheets in the previous section, delete the line `"google sheets id"`
    in `config.json`
1.  run the script: `python main.py`.
    -   note that if you have have done the optional google sheets setup and it is the first time
        running this script, you would be prompted for access to your google sheets. this is the
        project that you set up yourself earlier (i.e. no 3rd party is accessing your data)
1.  csv files are output to `data/csv` folder (and your google sheet if you chose to set it up)
1.  processed pdf and csv files are moved into `data/csv/processed` and `data/csv/processed`
    directories respectively at the end of the script

### troubleshooting

#### HttpError 400 when requesting ... returned "Invalid requests[0].addSheet: A sheet with the name ‘dec 2023’ already exists. Please enter another name."

-   delete any google sheets which have the same name as your csv files, then rerun the script
