from time import sleep
import os 
import re
from PyQt5.QtWidgets import QMessageBox

# Function to clear the command prompt after a given amount of time
def SleepClear(time):
    sleep(time)
    os.system('cls')

# Function to declare that an error happened
def Error():
    print("An Error Occured, Please Try Again Later. ")

# Function To Decorate the output 
def Message(string):
    print('-' * (len(string) + 4))
    print('| ' + string + ' |')
    print('-' * (len(string) + 4))

# Function to check if an email address is valid or not
def Check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else :
        return False

# Function to install the library Cryptography if it's not installed
def Library():
    try:
        import cryptography
    except error:
        os.system("pip install cryptography")


# Function to show a Warning Popup Message
def ShowWarningPopup(text):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)

    x = msg.exec_()


# Function to show a Warning Popup Message
def ShowInformationPopup(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Information)

    x = msg.exec_()
