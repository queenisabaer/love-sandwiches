import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    (Docstring should always be right under the functions names)
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated 
    by commas. The loop will repeatedly request data, until it is valid. 
    """
    while True: #repeat request for data right away if incorrect data was entered
        print("Please enter sales data from the last market.")
        print("Data should ne six numbers, separated by comma.")
        print("Example: 10,20,30,40,50,60\n") #to add a new line between example and data input field \n

        data_str = input("Enter your data her: \n") #for heruko app important! always add additional line in input fields
    
        sales_data = data_str.split(",") #split() method returns the broken up values as a list and removes commas from the string. convert string value into a list of values, each separated by a comma
         
        #set a condition to end while loop if data is valid
        if validate_data(sales_data): #takes the return statement in the validate_data()function and only runs if it is true
            print("Data is valid!") #for user to see, everything is correct
            break #ends while loop
    return sales_data #return the validated sales_data and returns this value

#validate data before allowing the rest of the programm to continue
def validate_data(values): #parameter of 'values' which will be our sales data list 
    """
    Inside tge try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values
    """
    #try-except statement to check if data is valid
    try: #code that runs with no errors if data is valid
        [int(value) for value in values] #loop through values list and convert each string into an integer
        if len(values) != 6: #raise a ValueError if lenght of data is not 6
            #len()method returns the length of the list - the number of values in it
            raise ValueError(#create own costum error message
                f"Exactly 6 calues required, you provided {len(values)}" 
            )
    except ValueError as e: #print an error to the terminal, Value Error class containt the details of the error trigerd by the code in try statement
         #by using as we're assigning that ValueError object to the e variable(standard for error)
         print(f"Invalid data: {e}, please try again.\n ")#print error if try fails
         return False
    
    return True #if function runs without any errors

#iCOMMENTED OUT: insert sales_data as a new entry in sales workshett over in Google Sheets
#def update_sales_worksheet(data): #parameter is data to insert, for function to work

   # Update sales worksheet, add new row with the list data provided.
    #print("Updating sales worksheet...\n") #give user feedback(UX) as program completes task.
    #sales_worksheet = SHEET.worksheet('sales') #to access sales worksheet from Google Sheet(on top this SHEET variable was created to get the google sheet)
    #use gspread method append_row() to pass inserted data
    #sales_worksheet.append_row(data) #append row method adds new row to the end of data in selected worksheet
    #print("Sales worksheet updated successfully\n")

# def update_surplus_worksheet(data): #parameter is data to insert, for function to work
#  Update surplus worksheet, add new row with the list data provided.
 
    #print("Updating surplus worksheet...\n") #give user feedback(UX) as program completes task.
    #surplus_worksheet = SHEET.worksheet('surplus') #to access sales worksheet from Google Sheet(on top this SHEET variable was created to get the google sheet)
    #use gspread method append_row() to pass inserted data
    #surplus_worksheet.append_row(data) #append row method adds new row to the end of data in selected worksheet
    #print("Surplus worksheet updated successfully\n")

#refactoring the two functions above(commented out)
def update_worksheet(data, worksheet):
    """
    Update worksheet, add new row with the list data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculate_surplus_data(sales_row): #pass sales data list to use in calculation
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n") #UX: signals that calucation is starting
    stock = SHEET.worksheet('stock').get_all_values() #use worksheet method to let programm know, which sheet we want. use gett_all_values() to fetch all of the cells from the stock worksheet
    stock_row = stock[-1]
    
    surplus_data = [] #create a list from the surplus calculation
    for stock, sales in zip(stock_row, sales_row): #iterates through both lists at same time, by using zip()
        surplus = int(stock) - sales #the stock values are still strings, so they need to be converted into integers to perform a calculation
        surplus_data.append(surplus) #append the calculated values to the surplus_data list
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects collums of data from sales worksheet, collecting the last 5
    entries for each sandwich and returns the data as a list of lists
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1,7): #for loop iterates 6 times starting by 1 and ending at 6(bevore 7) ind is for loop index
        column = sales.col_values(ind) #col index begins with 1 not 0! col is used for columns
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

#Best practice: wrap main function calls into a function called main
def main():
    """
    Run all programm functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data] #convert data from the get sales funciton into integers 
    update_worksheet(sales_data, 'sales') #call the function and pass it the sales_data list
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')

print("Welcome to Love Sandwich Data Automation\n")
main()
