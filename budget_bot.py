import os
import gspread

from bank_scraper import Bank
from bank_scraper.config import BOA_schema

from dotenv import load_dotenv

load_dotenv()

u = os.environ.get("BOA_USER")
p = os.environ.get("BOA_PASS")


bofa = Bank("Bank of America", u, p, schema=BOA_schema)

scraper = bofa.generate_scraper()  # create bank scraping session
scraper.login()  # log in to bank account
accounts = (
    scraper.scrape_overview()
)  # scrape account metadata from account overview page

first_account = accounts[0]

transactions = scraper.scrape_account(
    first_account
)  # scrape the first account for transactions
# can also reference accounts and transactions on the Bank and Account object
# eg. first_account.transactions or bofa.accounts


# Implementaiton of scraped transactions being added to a spreadsheet
client = gspread.service_account(filename="cred/budget-390915-2b136855e1e5.json")
sh = client.open("budget").sheet1
# Get existing IDs from column F
existing_ids = sh.col_values(6)  # Assuming the IDs are in column F (index 6)

for item in transactions:
    _id = item["_id"]
    if _id not in existing_ids:
        # Append the ID to the sheet
        sh.append_row([_id])
        print(f"Appended ID {_id} to the sheet.")
