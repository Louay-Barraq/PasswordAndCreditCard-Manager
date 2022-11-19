from time import sleep
import os 
import re
from PyQt5.QtWidgets import QMessageBox
from os import system, name

# Function to clear the command prompt after a given amount of time for both Windows and Linux users
def SleepClear(time):
   # for windows
   if name == 'nt':
       sleep(time)
       system('cls')

   # for mac and linux
   else:
       sleep(time)
       system('clear')


# Function to declare that an error happened
def Error():
    print("An Error Occured, Please Try Again Later. ")

# Function To Decorate the output 
def Message(string):
    print('-' * (len(string) + 4))
    print('| ' + string + ' |')
    print('-' * (len(string) + 4))

# Function to check if an email address is valid or not
def CheckEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else :
        return False


# Function to check if a credit card expiration date is valid or not
def CheckExpirationDate(number):
    # Length of given expiration date should be 5 characters
    # the first two and last two characters should be integers
    # the month's number should be between 01 and 12
    # the given expiration date should have a / in the middle  
    if (len(number) != 5) or (number[0:2].isdigit() == False) or (number[3::].isdigit() == False) or (number[2] != '/') or (int(number[0:2]) > 12) or (int(number[0:2]) <= 0):
        return False

    else :
        return True


# Function to show a Warning Popup Message
def ShowWarningPopup(text):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)

    msg.exec_()


# Function to show a Warning Popup Message
def ShowInformationPopup(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Information)

    msg.exec_()
