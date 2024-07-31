import re
from Project_functions import *  # import extra methods from py file


# Note: Start program from Project_Test

def start(username, session, Student, Score):  # create start method/ Main

    while True:  # infinite loop
        read_file('student.txt', username)  # reads .txt file, displays it to user
        user_input = input("Please enter the Operation Code: ")  # Prompts user to enter
        if user_input == '1':  # methods for each user input
            add_user(session, Student, Score)
        elif user_input == '2':
            displayUser(session, Student)
        elif user_input == '5':
            query_user(session, Student, Score)
        elif user_input == '3':
            modify_user(session, Student)
        elif user_input == '6':
            return
        elif user_input == '4':
            del_user(session, Student, Score)
        else:
            print("\t \u274CInvalid Input")  # if invalid input was entered

def add_user(session, Student, Score):  # methdo to add the user to database

    # retrieve the student record with the highest ID value from the table
    max_id = session.query(Student).order_by(Student.id.desc()).first()
    if max_id is None:
        next_id = 700300000  # first user added
    else:
        next_id = int(max_id.id) + 1  # user exsists with current id, increment to keep ID unique (Primary key requirment)

    read_file('add_user.txt')  # reads .txt file, dispalys to user
    while True:
        while True:
            studentName = input("Please Enter the Student Name (Firstname Lastname): ")
            if re.match(r"^[A-Z][a-z]{2,}\s[A-Z][a-z]{2,}$", studentName): # checks if correct format was entered by user
                break
            else:
                print("\t \u274C Invalid student name")

        while True:  # infinite loop
            studentAge = input("Please Enter the student's age: ")  # promts user
            if re.match(r"(?:[1-9]?\d|100)$", studentAge):  # checks if correct format was entered by user
                break  # if not duplicate, break out of loop
            else:
                print("\t \u274C Invalid student Age")  # not valid ID

        while True:
            studentGender = input("Please Enter the Student Gender: ").upper()
            if re.match(r'^(M|F|O)$', studentGender):  # checks if correct format was entered by user
                break
            else:
                print("\t \u274C Invalid Input")

        studentMajor = input("Please Enter the Student Major: ").upper()


        while True:
            studentPhone = input("Please Enter the Student Phone \u260E: ")
            if re.match(r"^\d{3}-\d{3}-\d{4}$", studentPhone):  # checks if correct format was entered by user
                break
            else:
                print("\t \u274C Invalid phone number")

        studentRecord = Student(  # sets new attributes to be entered into database from user inputs
            id = str(next_id),
            name = studentName,
            age = int(studentAge),
            gender = studentGender,
            major = studentMajor,
            phone = studentPhone
        )

        scoreRecord = Score(  # auto creates students score for each course that is unique to there ID
            id=str(next_id),
            name=studentName,
            CS1030=0,
            CS1100=0,
            CS2030=0
        )

        session.add(studentRecord)  # adds student to database
        session.add(scoreRecord)  # adds score to database
        session.commit()  # commits/ finalizes it to the database

        print("\t New student record has been added \u2714")

        print("\t\u2666 1. Continue\n\t\u2666 2. Exit")
        choice = input("Please Select 1 or 2: ")
        if choice == '1':  # repeats method
            continue
        elif choice == '2':
            return


def displayUser(session, Student):  # dispaly all userrs
    data = session.query(Student).all()  # fetch all student records from the database

    if not data:  # if no data
        print("\t No student records found.")
        return
    print("\t\u2666 1. Show all Students\n\t\u2666 2. Show Students by Name\n\t\u2666 3. Show Students by ID\n\t\u2666 4: Return")
    choice = input("Please Select: ")

    if choice == '1':
        print(40 * "=" + "Student Records" + "=" * 40)
        print(f"\t{'ID':<12} {'Name':<18} {'Age':<17} {'Gender':<13} {'Major':<12} \u260E")

        for student in data:  # prints all data from database table Student
            print(f"\t{student.id:<12} {student.name:<18} {student.age:<17} {student.gender:<13} {student.major:<12} {student.phone}")

    elif choice == '2':
        name = input("Enter the Student Name to Display: ")
        print(40 * "=" + "Student Records" + "=" * 40)
        print(f"\t{'ID':<12} {'Name':<18} {'Age':<6} {'Gender':<8} {'Major':<10} \u260E")

        found = False
        for student in data:
            if name.lower() in student.name.lower(): # prints all data related to name from database table Student
                print(f"\t{student.id:<12} {student.name:<18} {student.age:<6} {student.gender:<8} {student.major:<10} {student.phone}")
                found = True

        if not found:  # no students with name
            print(f"\t No students with name '{name}'")

    elif choice == '3':  # search by ID
        student_id = input("Enter the Student ID to Display: ")
        print(40 * "=" + "Student Records" + "=" * 40)
        print(f"\t{'ID':<12} {'Name':<18} {'Age':<6} {'Gender':<8} {'Major':<10} \u260E")

        found = False
        for student in data:
            if student.id == student_id: # prints all data related to ID from database table Student
                print(f"\t{student.id:<12} {student.name:<18} {student.age:<6} {student.gender:<8} {student.major:<10} {student.phone}")
                found = True

        if not found:
            print(f"\t No students found with ID '{student_id}'")

    elif choice == '4':  # return to menu
        return


def query_user(session, Student, Score):  # display individual data for ID
    print("\t\u2666 1. Display Student Score by Name\n\t\u2666 2. Update Student Score by ID\n\t\u2666 Other Return")
    choice = input("Please Select: ")

    if choice == '1':
        name = input("Enter the Student Name to Display the Score: ")  # prompt user
        print(40 * "=" + "Student Records" + "=" * 35)
        print(f"\t{'ID':<12} {'Name':<18} {'CS 1030':<10} {'CS 1100':<10} {'CS 2030'}")

        # filters table by name that was entered
        students = session.query(Student).filter(Student.name.ilike(f"%{name}%")).all()

        if not students:
            print(f"\t No students with name '{name}'")  # no student with name
        else:
            for student in students:
                scores = session.query(Score).filter_by(id=student.id).first()  # filters table by ID
                print(f"\t{student.id:<12} {student.name:<18} {scores.CS1030:<10} {scores.CS1100:<10} {scores.CS2030}")

    elif choice == '2':
        studentID = input("Please Enter the student ID to Update the Score: ")
        student = session.query(Student).filter_by(id=studentID).first()  # filters by ID
        if student:
            scores = session.query(Score).filter_by(id=studentID).first()  # filters score by ID that was entered

            # invokes method for user input
            cs_1030 = cus_input(scores.CS1030, "New Grade for CS 1030 (press enter without modification): ")
            cs_1100 = cus_input(scores.CS1100, "New Grade for CS 1100 (press enter without modification): ")
            cs_2030 = cus_input(scores.CS2030, "New Grade for CS 2030 (press enter without modification): ")

            scores.CS1030 = cs_1030  # sets table attributes to new data
            scores.CS1100 = cs_1100
            scores.CS2030 = cs_2030

            session.commit()  # commits data to table
            print("\t\u2714 Record Updated Successfully")
        else:
            print(f"\t \u274C No student found with ID '{studentID}'")
    else:
        return  # returns to menu

def modify_user(session, Student):  # modify user's information
    studentID = input("Please Enter Student ID to Modify: ")

    # Retrieve the student record from the database
    student_to_modify = session.query(Student).filter_by(id=studentID).first()

    if not student_to_modify:  # student ID does not exist in the database
        print(f"\u274C No record found")
        return

    # Copy original data
    original_data = {
        'Name': student_to_modify.name,
        'Age': student_to_modify.age,
        'Major': student_to_modify.major,
        'Phone': student_to_modify.phone
    }

    # Update the age
    new_age = cus_input(str(student_to_modify.age), "New age (press enter without modification): ")
    if new_age != str(student_to_modify.age):  # Check if new information was entered
        while not re.match(r"(?:[1-9]?\d|100)$", new_age):  # Check input format
            print("\t \u274C Invalid student Age")
            new_age = cus_input(str(student_to_modify.age), "New Age (press enter without modification): ")
        student_to_modify.age = int(new_age)  # Update age

    # Update the major
    new_major = cus_input(student_to_modify.major, "New major (press enter without modification): ").upper()
    if new_major != student_to_modify.major:
        student_to_modify.major = new_major  # Update major

    # Update the phone
    new_phone = cus_input(student_to_modify.phone, "New phone \u260E (press enter without modification): ")
    if new_phone != student_to_modify.phone:  # Check if new information was entered
        while not re.match(r"^\d{3}-\d{3}-\d{4}$", new_phone):
            print("\t \u274C Invalid phone number")
            new_phone = cus_input(student_to_modify.phone, "New phone \u260E (press enter without modification): ")
        student_to_modify.phone = new_phone  # Update phone

    if (student_to_modify.name != original_data['Name'] or
        student_to_modify.age != original_data['Age'] or
        student_to_modify.major != original_data['Major'] or
        student_to_modify.phone != original_data['Phone']):  # Check if data has changed
        session.commit()  # Commit changes to the database
        print("\t \u2714 Student record updated successfully")
    else:
        print("\t \u274C Record not modified!")  # No changes to the record


def del_user(session, Student, Score):  # delete user and score related to user
    print("\t\u2666 1. Delete Students by Name\n\t\u2666 2. Delete Students by ID\n\t\u2666 Other Return")
    choice = input("Please Select: ")

    if choice == '1':
        student_name = input("Please Enter Student Name to Delete: ")
        students_to_delete = session.query(Student).filter(Student.name == student_name).all()  # filters table by user name

        if not students_to_delete:  # no name exists
            print(f"\u274C The Student Name '{student_name}' does not exist")
            return

        for student in students_to_delete:
            # delete associated scores with user
            session.query(Score).filter(Score.id == student.id).delete()

            # delete the student record
            session.delete(student)

        session.commit()  # commit changes to databases
        print("\t \u2714 Student records deleted")

    elif choice == '2':
        student_id = input("Please Enter Student ID to Delete: ")
        student_to_delete = session.query(Student).filter(Student.id == student_id).first()  # filters by id

        if not student_to_delete:
            print(f"\u274C The Student ID '{student_id}' does not exist")
            return

        # delete associated scores with user ID
        session.query(Score).filter(Score.id == student_id).delete()

        # Delete the student record
        session.delete(student_to_delete)

        session.commit()
        print("\t \u2714 Student record deleted")

    else:
        return  # return to menu


