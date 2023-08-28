import sqlite3
from datetime import datetime

NO_APPOINTMENT = "NO_APPOINTMENT"
SELECT_FIRST_APPOINTMENT_DATE = "SELECT_FIRST_APPOINTMENT_DATE"
FIRST_DOSE_COMPLETED = "FIRST_DOSE_COMPLETED"
SELECT_SECOND_APPOINTMENT_DATE = "SELECT_SECOND_APPOINTMENT_DATE"
SECOND_DOSE_COMPLETED = "SECOND_DOSE_COMPLETED"

conn = sqlite3.connect('CovidVaccination2.db')
cursor = conn.cursor()

table1 = "CREATE TABLE IF NOT EXISTS CITIZEN (AADHAR_NUMBER VARCHAR(255) PRIMARY KEY, DATE BIGINT, STATUS VARCHAR(255)) "
cursor.execute(table1)

def allDB():
    cursor.execute("SELECT * FROM CITIZEN")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def aadhar_existance(aadhar_number):
    query = (f'''SELECT * FROM CITIZEN WHERE AADHAR_NUMBER = '{aadhar_number}' ''')  
    cursor.execute(query)
    row = cursor.fetchone()

    return row != None

def get_current_user(aadhar_number):
    query = (f'''SELECT * FROM CITIZEN WHERE AADHAR_NUMBER = '{aadhar_number}' ''')
    cursor.execute(query)
    return cursor.fetchone()

def update_user(aadhar_number, date, new_status):
    query = f'''UPDATE CITIZEN SET STATUS = '{new_status}', DATE = '{date}' WHERE AADHAR_NUMBER = '{aadhar_number}' '''
    cursor.execute(query)
    pass

options = int(input("Select the Type of User:\n 1.PATIENT \n 2.STAFF "))
if options == 1 :
    take_aadhar = int(input("Enter Your Aadhar Number: "))
    aadhar_exists = aadhar_existance(take_aadhar)
    if aadhar_exists == True:
        user_data = get_current_user(take_aadhar)
        if user_data is not None:
            current_status = user_data[2]
            if current_status == NO_APPOINTMENT:
                print("Please apply for an appointment. Press 1 to confirm.")
                confirm_appointment = int(input())
                if confirm_appointment == 1:
                    appointment_date_str = input("Enter Date (YYYY-MM-DD): ")
                    appointment_timestamp = int(datetime.strptime(appointment_date_str, "%Y-%m-%d").timestamp())
                    print("Appointment has been Booked.")
                    update_user(take_aadhar, appointment_timestamp, SELECT_FIRST_APPOINTMENT_DATE)

            elif current_status == SELECT_FIRST_APPOINTMENT_DATE:
                appointment_timestamp = user_data[1]  
                appointment_date = datetime.fromtimestamp(appointment_timestamp)
                formatted_date = appointment_date.strftime("%Y-%m-%d %H:%M:%S")  
                print("Appointment Date:", formatted_date)

            elif current_status == FIRST_DOSE_COMPLETED:
                print("Status: First dose completed")
                confirm_second_appointment = int(input("Please apply for the second appointment. Press 1 to confirm: "))

                if confirm_second_appointment == 1:
                    appointment_date_str = input("Enter Date (YYYY-MM-DD): ")
                    appointment_timestamp = int(datetime.strptime(appointment_date_str, "%Y-%m-%d").timestamp())
                    print("Second appointment has been Booked.")
                    update_user(take_aadhar, appointment_timestamp, SELECT_SECOND_APPOINTMENT_DATE)

            elif current_status == SELECT_SECOND_APPOINTMENT_DATE:
                appointment_timestamp = user_data[1]  
                appointment_date = datetime.fromtimestamp(appointment_timestamp)
                formatted_date = appointment_date.strftime("%Y-%m-%d %H:%M:%S")  
                print("Appointment Date:", formatted_date)

            elif current_status == SECOND_DOSE_COMPLETED:
                print("Fully vaccinated")
    else:
        cursor.execute(f'''INSERT INTO CITIZEN (AADHAR_NUMBER, DATE, STATUS) VALUES ('{take_aadhar}', 0, '{NO_APPOINTMENT}')''')
        print("Start again to apply for Appointment!")

elif options == 2 :
    take_aadhar = int(input("Enter Patient's Aadhar Number: "))
    aadhar_exists = aadhar_existance(take_aadhar)

    if aadhar_exists == False :
        print("Please Apply for appointment!")
    else:
        user_data = get_current_user(take_aadhar)
        current_status = user_data[2] if user_data else None

        if current_status in [NO_APPOINTMENT, FIRST_DOSE_COMPLETED, SECOND_DOSE_COMPLETED]:
            print("Ask the patient to take an appointment.")

        elif current_status == SELECT_FIRST_APPOINTMENT_DATE :
            update_user(take_aadhar, 0 , FIRST_DOSE_COMPLETED)
            print("First dose completed!")

        elif current_status == SELECT_SECOND_APPOINTMENT_DATE :
            update_user(take_aadhar, 0 ,SECOND_DOSE_COMPLETED)
            print("Second dose completed!")

conn.commit()   
conn.close()
