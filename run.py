import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last trading day.")
        print("Data should be 6 numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        # Ask user for data
        data_str = input("Enter your data here: ")

        # Convert string value into list of values using split()
        sales_data = data_str.split(",")

        # Call validate_data function, passing it the list of sales data
        # This function checks for errors -
        # If no errors it will return True
        # and print a statement to the terminal
        # and the while loop is stopped using the break keyword.
        # If validate_data function encounters an error,
        # it will print the error to the terminal, and return False.
        # So the while loop will repeat it’s request for data.
        if validate_data(sales_data):
            print("Data is valid")
            break

    # Return validated sales_data from the get_sales_data function.
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        # Use list comprehension to convert each individual value in the values list into an integer.
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided.
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")

# def update_surplus_worksheet(data):
#     """
#     Update surplus worksheet, add new row with the list data provided.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully.\n")

# Refactor update_sales_worksheet and update_surplus_worksheet
# into one function:
# update_worksheet
def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returas the data 
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")


    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    # Convert strings from data variable to integers
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to Love Sandwiches Data Automation")
main()

