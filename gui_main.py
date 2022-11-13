import sys
from os import path
import sqlite3
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from main import AllUsers, check_user
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from db_functions import (create_db, get_account_infos, get_existing_accounts,get_key, get_user_id, add_account, add_user,
    update_account_password, update_account_username, delete_account, delete_user, update_account_email)
from encryption_functions import (generate_key, get_hash, encrypt_password, decrypt_password)
from other_functions import Check, Library, ShowWarningPopup, ShowInformationPopup


class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        loadUi("main_menu.ui", self)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.Sign_Up.clicked.connect(self.GoToSignUp)
        self.Sign_In.clicked.connect(self.GoToSignIn)
        self.DeleteAUser.clicked.connect(self.GoToDelAUser)
        self.Quit.clicked.connect(self.Exit)

    def GoToSignUp(self):
        signup = SignUp()
        widget.addWidget(signup)
        widget.setFixedWidth(760)
        widget.setFixedHeight(525)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToSignIn(self):
        signin = SignIn()
        widget.addWidget(signin)
        widget.setFixedWidth(745)
        widget.setFixedHeight(525)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToDelAUser(self):
        delauser = DelAUser()
        widget.addWidget(delauser)
        widget.setFixedWidth(715)
        widget.setFixedHeight(480)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Exit(self):
        sys.exit()


class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi("sign_up.ui", self)
        self.Sign_Up.clicked.connect(self.SignUp)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)


    def SignUp(self):
        username = self.Username.text()
        master_password = self.MasterPassword.text()
        master_password_confirmation = self.PasswordConfirmation.text()

        # Checking the non-ressemblance of the users' names
        for name in AllUsers():
            if name[0] == username:
                ShowWarningPopup("Username already exists !")
                break
        
        else :
            if master_password != master_password_confirmation :
                ShowWarningPopup("The Password And Its Confirmation Aren't Similar !")

            else :
                hashed_mp = get_hash(master_password)
                key = generate_key()

                try :
                    add_user(username, hashed_mp, key)
                    ShowInformationPopup("Success", "User Added Successfully !")
                    mainmenu = MainMenu()
                    widget.addWidget(mainmenu)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                

                except sqlite3.Error :
                    ShowWarningPopup("Error Occured, Try Again Later!")
        

    def Return(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setFixedWidth(725)
        widget.setFixedHeight(490)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class SignIn(QDialog):
    def __init__(self):
        super(SignIn, self).__init__()
        loadUi("sign_in.ui", self)
        self.Sign_In.clicked.connect(self.SignIn)
        self.Exit.clicked.connect(self.Quit)
        self.ReturnButton.clicked.connect(self.Return)


    def SignIn(self):
        username = self.Username.text()
        master_password = get_hash(self.MasterPassword.text())

        verif = check_user(username, master_password)
        if verif == True:
            ShowInformationPopup("Success", "User Signed In Successfully !")

            global user_id
            user_id = get_user_id(username)
            global key 
            key = get_key(user_id)

            usermenu = UserMenu()
            widget.addWidget(usermenu)
            widget.setCurrentIndex(widget.currentIndex() + 1)

            # Returning the username and the key
            return user_id, key
        
        if verif == False:
            ShowWarningPopup("Access Blocked, Password Is Incorrect !")

        if verif == None:
            ShowWarningPopup("Given Infos Doesn't Match With Any Of Our Users Infos !")

    def Return(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setFixedWidth(725)
        widget.setFixedHeight(490)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class DelAUser(QDialog):
    def __init__(self):
        super(DelAUser, self).__init__()
        loadUi("delete_a_user.ui", self)
        self.Delete.clicked.connect(self.DeleteAUser)
        self.Exit.clicked.connect(self.Quit)
        self.ReturnButton.clicked.connect(self.Return)


    def DeleteAUser(self):
        username = self.Username.text()
        hashed_master_password = get_hash(self.MasterPassword.text())
        # Function to delete the user 

        verification = check_user(username, hashed_master_password)

        if verification == True:
            try :
                delete_user(get_user_id(username))
                ShowInformationPopup("Success", "User Deleted Successfully !")
                mainmenu = MainMenu()
                widget.addWidget(mainmenu)
                widget.setFixedWidth(730)
                widget.setFixedHeight(490)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            except sqlite3.Error:
                ShowWarningPopup("Error Occured, Try Again Later !")

        elif verification == False:
            ShowWarningPopup("Access Denied !")

        elif verification == None:
            ShowWarningPopup("The Provided Infos Doesn't Exist !")

    def Return(self):
        mainmenu = MainMenu()
        widget.addWidget(mainmenu)
        widget.setFixedWidth(730)
        widget.setFixedHeight(490)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class UserMenu(QDialog):
    def __init__(self):
        super(UserMenu, self).__init__()
        loadUi("user_menu.ui", self)
        self.AddANewAccount.clicked.connect(self.GoToAddANewAccount)
        self.ListAllSavedAccounts.clicked.connect(self.GoToListAccounts)
        self.GetAnAccountInfos.clicked.connect(self.GoToGetInfos)
        self.UpdateAnAccountInfos.clicked.connect(self.GoToUpdateInfos)
        self.DeleteAnExistingAccount.clicked.connect(self.GoToDeleteAccount)
        self.Exit.clicked.connect(self.Quit)

    def GoToAddANewAccount(self):
        addAnAccount = AddAnAccount()
        widget.addWidget(addAnAccount)
        widget.setFixedWidth(755)
        widget.setFixedHeight(525)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToListAccounts(self):
        listAllAccounts = ListAllAccounts()
        widget.addWidget(listAllAccounts)
        widget.setFixedWidth(745)
        widget.setFixedHeight(525)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToGetInfos(self):
        getAnAccountInfos = GetAnAccountInfos()
        widget.addWidget(getAnAccountInfos)
        widget.setFixedWidth(765)
        widget.setFixedHeight(525)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToUpdateInfos(self):
        accountSelection = AccountSelection()
        widget.addWidget(accountSelection)
        widget.setFixedWidth(630)
        widget.setFixedHeight(350)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToDeleteAccount(self):
        deleteAnAccount = DeleteAnAccount()
        widget.addWidget(deleteAnAccount)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class AddAnAccount(QDialog):
    def __init__(self):
        super(AddAnAccount, self).__init__()
        loadUi("add_a_new_account.ui", self)
        self.Add.clicked.connect(self.AddAccount)
        self.Exit.clicked.connect(self.Quit)
        self.ReturnButton.clicked.connect(self.Return)

    def AddAccount(self):
        account_name = self.AccountName.text()
        account_username = self.AccountUsername.text()
        account_email = self.AccountEmail.text()
        account_password = self.AccountPassword.text()
        account_password_confirmation = self.PasswordConfirmation.text()

        # Function to add the account
        all_accounts = get_existing_accounts(user_id)

    # Getting the account's name and checking if it already exists 
        condition = False
        for account in all_accounts:
            if account_name == account[0]:
                ShowWarningPopup("Account Already Exists !")
                condition = True
                break

        while condition == False:
            if Check(account_email) == False:
                ShowWarningPopup("Given Email Isn't Valid !")
                break
            if account_password != account_password_confirmation:
                ShowWarningPopup("Password And Its Confirmation Aren't Similar !")
                break
            if ((len(account_name) == 0) or (len(account_username) == 0) or (len(account_email) == 0) or
             (len(account_password) == 0) or (len(account_password_confirmation) == 0)):
                ShowWarningPopup("Please Fill In All The Info Fields.")
                break

            encrypted_account_password = encrypt_password(key, account_password) 

            try:
                add_account(account_name, account_username, account_email, encrypted_account_password, user_id)
                ShowInformationPopup("Success", f"Account Added Successfully !")
                usermenu = UserMenu()
                widget.addWidget(usermenu)
                widget.setFixedWidth(730)
                widget.setFixedHeight(510)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            
            except sqlite3.Error:
                ShowWarningPopup("Error Occured, Try Again Later.")
            
            break

    def Return(self):
        usermenu = UserMenu()
        widget.addWidget(usermenu)
        widget.setFixedWidth(730)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class AccountSelection(QDialog):
    def __init__(self):
        super(AccountSelection, self).__init__()
        loadUi("account_to_update.ui", self)
        self.Confirm.clicked.connect(self.GetAccount)
        self.ReturnButton.clicked.connect(self.Return)
        self.ExitButton.clicked.connect(self.Quit)

    def GetAccount(self):
        global account
        account = self.AccountName.text()
        all_accounts = get_existing_accounts(user_id)

        exists = False
        for acc in all_accounts:
            if acc[0] == account:
                exists = True

        if exists == False:
            ShowWarningPopup("Account Doesn't Exist !")

        else:
            updateAnAccountInfos = UpdateAnAccountInfos()
            widget.addWidget(updateAnAccountInfos)
            widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def Return(self):
        usermenu = UserMenu()
        widget.addWidget(usermenu)
        widget.setFixedWidth(730)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class GetAnAccountInfos(QDialog):
    def __init__(self):
        super(GetAnAccountInfos, self).__init__()
        loadUi("get_an_account_infos.ui", self)
        self.Show.clicked.connect(self.GetInfos)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def GetInfos(self): 
        account_name = self.AccountName.text()

    # Function to get the account's infos
        all_accounts = get_existing_accounts(user_id)
        if len(all_accounts) == 0:
            ShowWarningPopup("There Are No Accounts Saved !")

        else:
            # Checking if the account already exists
            exists = False
            for acc in all_accounts:
                if acc[0] == account_name:
                    exists = True

            if exists == False:
                ("Account Doesn't Exist !")

            else:
                account_username, account_email, encrypted_account_password = get_account_infos(user_id, account_name)
                decrypted_account_password = decrypt_password(key, encrypted_account_password)

                self.AccountUsername.setText(account_username)
                self.AccountEmail.setText(account_email)
                self.AccountPassword.setText(decrypted_account_password)

    def Return(self):
        usermenu = UserMenu()
        widget.addWidget(usermenu)
        widget.setFixedWidth(730)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class ListAllAccounts(QDialog):
    def __init__(self):
        super(ListAllAccounts, self).__init__()
        loadUi("all_saved_accounts.ui", self)
        self.Show.clicked.connect(self.GetInfos)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def GetInfos(self): 
        # Function to display the accounts
        accounts = get_existing_accounts(user_id)
        if len(accounts) == 0:
            ShowWarningPopup("There Are No Accounts Saved !")

        else:
            # Getting the number of rows
            accounts_number = len(accounts)
            print(accounts_number)
            # Listing All The Accounts
            self.Table.setRowCount(accounts_number)
            tableRow = 0
            for row in accounts:
                self.Table.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(row[0]))
                tableRow += 1

    def Return(self):
        usermenu = UserMenu()
        widget.addWidget(usermenu)
        widget.setFixedWidth(730)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class UpdateAnAccountInfos(QDialog):
    def __init__(self):
        super(UpdateAnAccountInfos, self).__init__()
        loadUi("update_an_account_infos.ui", self)
        self.UpdateUsername.clicked.connect(self.GoToUpdateUsername)
        self.UpdateEmail.clicked.connect(self.GoToUpdateEmail)
        self.UpdatePassword.clicked.connect(self.GoToUpdatePassword)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def GoToUpdateUsername(self):
        updateUsername = UpdateUsername()
        widget.addWidget(updateUsername)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToUpdateEmail(self):
        updateUsername = UpdateEmail()
        widget.addWidget(updateUsername)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToUpdatePassword(self):
        updatePassword = UpdatePassword()
        widget.addWidget(updatePassword)
        widget.setFixedWidth(735)
        widget.setFixedHeight(460)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Return(self):
        usermenu = UserMenu()
        widget.addWidget(usermenu)
        widget.setFixedWidth(730)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        self.exit()
        

class UpdateUsername(QDialog):
    def __init__(self):
        super(UpdateUsername, self).__init__()
        loadUi("update_username.ui", self)
        self.Update.clicked.connect(self.UpUsername)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def UpUsername(self): 
        username = self.Username.text()

        # Function to update the account's username
        try:
            update_account_username(user_id, username, account)
            ShowInformationPopup("Success", "Account's Username Updated Successfully !")
            usermenu = UserMenu()
            widget.addWidget(usermenu)
            widget.setFixedWidth(730)
            widget.setFixedHeight(510)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        except sqlite3.Error:
            ShowWarningPopup("An Error Occured, Try Again !")

    def Return(self):
        updateanaccountinfos = UpdateAnAccountInfos()
        widget.addWidget(updateanaccountinfos)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class UpdateEmail(QDialog):
    def __init__(self):
        super(UpdateEmail, self).__init__()
        loadUi("update_email.ui", self)
        self.Update.clicked.connect(self.UpEmail)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def UpEmail(self): 
        email = self.Email.text()
        # Function to update the account's email
        if Check(email) == True:
            try:
                update_account_email(user_id, email, account)
                ShowInformationPopup("Success", "Account's Email Updated Successfully !")
                usermenu = UserMenu()
                widget.addWidget(usermenu)
                widget.setFixedWidth(730)
                widget.setFixedHeight(510)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            except sqlite3.Error:
                ShowWarningPopup("An Error Occured, Try Again !")
        
        else:
            ShowWarningPopup("Email Isn't Valid !")

    def Return(self):
        updateanaccountinfos = UpdateAnAccountInfos()
        widget.addWidget(updateanaccountinfos)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def Quit(self):
        sys.exit()


class UpdatePassword(QDialog):
    def __init__(self):
        super(UpdatePassword, self).__init__()
        loadUi("update_password.ui", self)
        self.Update.clicked.connect(self.UpPassword)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def UpPassword(self): 
        password = self.Password.text()
        password_confirmation = self.PasswordConfirmation.text()

        # Function to update the account's password
        if password != password_confirmation:
            ShowWarningPopup("Password And Its Confirmation Aren't Similar !")

        else :
            encrypted_password = encrypt_password(key, password)
            try:
                update_account_password(user_id, encrypted_password, account)
                ShowInformationPopup("Success", "Account's Password Updated Successfully !")
                usermenu = UserMenu()
                widget.addWidget(usermenu)
                widget.setFixedWidth(730)
                widget.setFixedHeight(510)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            except sqlite3.Error:
                ShowWarningPopup("An Error Occured, Try Again !")

    def Quit(self):
        sys.exit()

    def Return(self):
        updateanaccountinfos = UpdateAnAccountInfos()
        widget.addWidget(updateanaccountinfos)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeleteAnAccount(QDialog):
    def __init__(self):
        super(DeleteAnAccount, self).__init__()
        loadUi("delete_an_account.ui", self)
        self.Delete.clicked.connect(self.DelAccount)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def DelAccount(self): 
        account_name = self.Name.text()

    # Function to delete an account
        all_accounts = get_existing_accounts(user_id)
        condition = True
        for acc in all_accounts:
            if acc[0] == account_name:
                break
        else:
            condition = False
        
        # In case the given account doesn't exist in the database
        if condition == False:
            ShowWarningPopup(f"Account Doesn't Exist !")

        else :
            try:
                delete_account(user_id, account_name)
                ShowInformationPopup("Success", "Account Deleted Successfully !")
            except sqlite3.Error:
                ShowWarningPopup("An Error Occured, Try Again Later !")


    def Return(self):
        usermenu = UserMenu()
        widget.addWidget(usermenu)
        widget.setFixedWidth(730)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


# Main Part :

if __name__ == '__main__':
    if not path.exists('passwords.db'):
        create_db()

    app = QApplication([])
    widget = QtWidgets.QStackedWidget()
    mainmenu = MainMenu()
    widget.addWidget(mainmenu)
    widget.setFixedWidth(725)
    widget.setFixedHeight(480)
    widget.setWindowIcon(QtGui.QIcon("LOGO.png"))
    widget.setWindowTitle("Password Manager - Testing Version")
    widget.show()
    app.exec_()
    