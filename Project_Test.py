
from Project_Login_Page import UserAuth  # import Login page
from Project_Home_Page import start  # import home page
from Project_Database import dataBaseMain  # import database

# Current user in system: JohnDoe, Password: ^Password1

def main():

    session, User, Student, Score = dataBaseMain()
    auth = UserAuth()  # create instance of UserAuth
    while True:
        logged_in_user = auth.login()  # prompts login()method
        if logged_in_user:  # if true
            start(logged_in_user, session, Student, Score)  # login with username

main()