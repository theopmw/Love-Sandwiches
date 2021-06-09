import gspread
from google.oauth2.service_account import Credentials

# Set scope
# Lists the APIs that the program should access in order to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Create CREDS variable
# Call the from_service_account_file method of the Credentials class (imported in line 2), and pass it the creds.json file name
CREDS = Credentials.from_service_account_file('creds.json')
# Create SCOPE_CREDS variable
#  Use the with_scopes method of the creds object, and pass it the SCOPE variable.
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# Create GSPREAD_CLIENT
# Use the gspread authorize method, and pass it SCOPED_CREDS.
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Access the love_sanwiches spreadsheet by using the open() method on our client object and passing it the name of the spreadsheet
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# Define sheet variable and using the worksheet method of the sheet, call the “sales” worksheet (this corresponds to the name of the worksheet in the love_sandwiches work book)
sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)