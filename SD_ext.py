import sqlite3
import tkinter.messagebox

# main table

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS RegisteredAccounts(
                    UserID TEXT,
                    UserPassword TEXT)"""# for accounts login

SELECT_SN_PASSWORD = "SELECT *FROM RegisteredAccounts WHERE UserID = ? AND  UserPassword = ?"



CREATE_TABLE = """CREATE TABLE IF NOT EXISTS Students(
                StudentID TEXT,
                LastName TEXT,
                FirstName TEXT,
                MiddleName TEXT,
                Course TEXT,
                YearLevel TEXT,
                Gender TEXT)   """
INSERT_RESEARCHER = "INSERT INTO Students(StudentID,LastName,FirstName,MiddleName,Course,YearLevel,Gender) VALUES(?,?,?,?,?,?,?)"#
DELETE_RESEARCHER = "DELETE FROM Students WHERE StudentID = ?"



RECORD_TABLE = """CREATE TABLE IF NOT EXISTS UserRecord(
                StudentID TEXT,
                Professor TEXT,
                Date TEXT,
                TimeIn TEXT,
                TimeOut TEXT)""" #for digital logbook


ADDSTUDENT = "INSERT INTO UserRecord(StudentID,Professor,Date,TimeIn) VALUES(?,?,?,?)"
SELECTNAME="SELECT *FROM Students WHERE StudentID =?"
OUT = "SELECT * FROM UserRecord WHERE StudentID = ? AND TimeIn = ?"
UPDATE = f"UPDATE UserRecord SET TimeOut = ? WHERE StudentID = ? AND TimeOut IS NULL AND TimeIn=?"
POPULATE = "SELECT *FROM UserRecord"
QUERY= "SELECT TimeOut FROM UserRecord WHERE StudentID = ?"




def connect():
    return sqlite3.connect("Laboratory_Database.db")


def createtable(connection):
    with connection:
        connection.execute(CREATE_TABLE)


def addResearcher(connection, StudentID, LastName, FirstName, Password, Course, YearLevel,Gender):
    with connection:
        connection.execute(INSERT_RESEARCHER, (StudentID,LastName, FirstName, Password, Course, YearLevel,Gender))



def confirm_SN_Pass(connection, UserID, UserPassword):
    with connection:
        result = connection.execute(SELECT_SN_PASSWORD, (UserID, UserPassword)).fetchone()
        return result


def delete(connection, StudentID):
    with connection:
        connection.execute(DELETE_RESEARCHER, (StudentID,))
        print("An account has been deleted!")


# second table
def RecordTable(connection):
    with connection:
        connection.execute(RECORD_TABLE)

def get_details(connection, StudentID):
    with connection:
        name = connection.execute(SELECTNAME, (StudentID,)).fetchone()
        return name



def addStudent(connection, StudentID, Professor, Date, TimeIn):
    # Use a context manager for the database connection
    with connection:
        connection.execute(ADDSTUDENT, (StudentID,Professor, Date, TimeIn))
        print("You added a student in record")

def OutRecord(connection, StudentID, timeIn,time):
    with connection:
        current_timeout_result = connection.execute(OUT, (StudentID,timeIn)).fetchone()
        if current_timeout_result:
            connection.execute(UPDATE, (time, StudentID,timeIn))
            tkinter.messagebox.showinfo(title="Log out", message=f'{StudentID} is now logged out')
            return current_timeout_result  # Assuming you want to return something meaningful here
        else:
            tkinter.messagebox.showerror(title="Invalid", message="Student not found or already logged out!")


def getLogOutTime(connection, StudentID):
    QUERY = "SELECT TimeOut FROM UserRecord WHERE Name = ?"
    cursor = connection.execute(QUERY, (StudentID,))
    result = cursor.fetchone()
    if result:
        return result[0]  # Return the logout time
    else:
        return None  # Student hasn't logged out yet



def populate(connection):
    with connection:
        rec = connection.execute(POPULATE).fetchall()
        return rec



