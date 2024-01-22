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
    Get sales figures input from the user (Docstring should always be right under the functions names)
    """
    while True: #repeat request for data right away if incorrect data was entered
        print("Please enter sales data from the last market.")
        print("Data should ne six numbers, separated by comma.")
        print("Example: 10,20,30,40,50,60\n") #to add a new line between example and data input field \n

        data_str = input("Enter your data her: ")
    
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


data = get_sales_data()