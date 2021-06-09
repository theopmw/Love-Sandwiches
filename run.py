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
# Call the from_service_account_file method of the Credentials class
# (imported in line 2), and pass it the creds.json file name
CREDS = Credentials.from_service_account_file('creds.json')
# Create SCOPE_CREDS variable
#  Use the with_scopes method of the creds object,
# and pass it the SCOPE variable.
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# Create GSPREAD_CLIENT
# Use the gspread authorize method, and pass it SCOPED_CREDS.
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Access the love_sanwiches spreadsheet by using the open() method on our
# client object and passing it the name of the spreadsheet
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# TEST TO CHECK API IS WORKING
# Define sheet variable and using the worksheet method of the sheet,
# call the “sales” worksheet (this corresponds to the name of the worksheet
# in the love_sandwiches spreadsheet)
# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)


def get_sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter sales data from the last market.")
    print("Data should be 6 numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")

    # Convert string value into list of values using split()
    sales_data = data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")


get_sales_data()
