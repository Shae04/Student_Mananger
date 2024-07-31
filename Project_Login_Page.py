import re, hashlib
from Project_functions import *  # import extra functions
from Project_Database import dataBaseMain  # import database

session, User, Student, Score = dataBaseMain()  # intialize the database session

# Note: Start Program form Project_Test

class UserAuth:
    welcome_file = 'welcome2.txt'  # stores .txt file into varaible

    @staticmethod  #
    def login():
        while True:  # infite loop
            read_file(UserAuth.welcome_file)  # display file
            user_input = input("Please select (1 - 3): ")
            if user_input == '1':
                username = UserAuth.perform_login()  # prompts login method
                if username:  # if true
                    return username  # returns name
            elif user_input == '2':
                UserAuth.registration()  # create account
            elif user_input == '3':
                exit_system()  # method to exit system
            else:
                print("\t \u274C Invalid Input")

    @staticmethod
    def registration():  # to create new account
        print(22 * "=" + "Registration" + "=" * 23)
        print("\t \u2666 1. Account name is between 6 and 12 letters long")
        print("\t \u2666 2. Account name's first letter must be capitalized")

        while True:
            username = input("Please Enter Account Name: ")
            if re.match(r"^[A-Z][a-zA-Z0-9]{5,11}$", username):  # checks format
                if session.query(User).filter_by(name=username).first():  # if account already exsists
                    print("\t \u274C Registration Failed! Account Already Exists.")
                    return  # Return to the welcome page
                else:
                    break
            else:
                print("\t \u274C Account Name Not Valid!")

        print("\t \u2666 1. Password must start with one of the following special characters !@#$%^&*")
        print("\t \u2666 2. Password must contain at least one digit, one lowercase letter, and one uppercase letter")
        print("\t \u2666 3. Password is between 6 and 12 letters long")

        while True:
            password = input("Please enter your password: ")
            if re.match(r"^(?=.*[!@#$%^&*])(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{6,12}$", password):  # checks if correct format was entered
                break # correct
            else:
                print("\t \u274C Password Not Valid!")  # not correct, prompts again

        hashed_password = hashlib.md5(password.encode()).hexdigest()  # hashes password

        new_user = User(name=username, password=hashed_password)  # adds new user into User table
        session.add(new_user)  # adds new user to database
        session.commit()
        print("\u2714 Registration completed!")

    @staticmethod
    def perform_login():  # method to login
        while True:
            username = input("Please Enter your Account: ")
            user = session.query(User).filter_by(name=username).first()  # filters by username

            if user is None:  # if no name exsists in database
                print("\t \u274C Login Failed! Account does not exist")
            else:
                break  # returns

        while True:
            password = input("Please Enter your Password: ")
            hashed_password = hashlib.md5(password.encode()).hexdigest()  # hashes password
            if user.password == hashed_password: # checks hash password with database hash password
                return username  # returns username to dispaly in menu
            else:
                print("\t \u274C Login Failed! Incorrect password")
