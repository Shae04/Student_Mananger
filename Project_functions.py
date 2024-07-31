
def read_file(file_name, username = None):  # reads .txt files and displays it to user
    with open(file_name, "r", encoding="utf-8") as inputFile:
        content = inputFile.read()
        if username:
            content = content % username
        print(content)

def cus_input(current_value, message):  # takes users input from other methods
    user_input = input(message)
    if user_input.strip() == "":  # if user input is blank it returns the current data that is not modified
        return current_value
    return user_input  # returns the user input, user entered infromation, data changes

def exit_system():  # to exit program
    userInput = input("Do you want to Exit the System? Enter Y to confirm, N to cancel: ").upper()
    if userInput != 'Y':  # if n was entered, it will return to menu
        print("N was entered, returning......")
        return
    exit()   # exits the program
