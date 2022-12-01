import sys
from os import path
import sqlite3
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from main import AllUsers, check_user
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from db_functions import (create_db, get_account_infos, get_existing_accounts,get_key, get_user_id, add_account, add_user,
    update_account_password, update_account_username, delete_account, delete_user, update_account_email, add_credit_card,
    update_credit_card_name, update_credit_cardholder_name, update_credit_card_number, update_credit_card_expiration_date,
    update_credit_card_CVV, delete_credit_card, get_credit_card_infos, get_existing_credit_cards)
from encryption_functions import (generate_key, get_hash, encrypt_password, decrypt_password)
from other_functions import CheckEmail, ShowWarningPopup, ShowInformationPopup, CheckExpirationDate


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

            serviceSelection = ServiceSelection()
            widget.addWidget(serviceSelection)
            widget.setFixedWidth(600)
            widget.setFixedHeight(350)
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


class ServiceSelection(QDialog):
    def __init__(self):
        super(ServiceSelection, self).__init__()
        loadUi("service_selection.ui", self)
        self.Accounts.clicked.connect(self.MoveToAccountsMenu)
        self.CCards.clicked.connect(self.MoveToCreditCardsMenu)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def MoveToAccountsMenu(self):
        accountUserMenu = AccountUserMenu()
        widget.addWidget(accountUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(515)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def MoveToCreditCardsMenu(self):
        creditCardUserMenu = CreditCardUserMenu()
        widget.addWidget(creditCardUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Return(self):
        mainMenu = MainMenu()
        widget.addWidget(mainMenu)
        widget.setFixedWidth(725)
        widget.setFixedHeight(490)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class AccountUserMenu(QDialog):
    def __init__(self):
        super(AccountUserMenu, self).__init__()
        loadUi("acc_user_menu.ui", self)
        self.AddANewAccount.clicked.connect(self.GoToAddANewAccount)
        self.ListAllSavedAccounts.clicked.connect(self.GoToListAccounts)
        self.GetAnAccountInfos.clicked.connect(self.GoToGetInfos)
        self.UpdateAnAccountInfos.clicked.connect(self.GoToUpdateInfos)
        self.DeleteAnExistingAccount.clicked.connect(self.GoToDeleteAccount)
        self.Exit.clicked.connect(self.Quit)
        self.ReturnButton.clicked.connect(self.Return)

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
        widget.setFixedHeight(355)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToDeleteAccount(self):
        deleteAnAccount = DeleteAnAccount()
        widget.addWidget(deleteAnAccount)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Return(self):
        serviceSelection = ServiceSelection()
        widget.addWidget(serviceSelection)
        widget.setFixedWidth(600)
        widget.setFixedHeight(340)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class CreditCardUserMenu(QDialog):
    def __init__(self):
        super(CreditCardUserMenu, self).__init__()
        loadUi("cc_user_menu.ui", self)
        self.AddANewCreditCard.clicked.connect(self.GoToAddANewCreditCard)
        self.ListAllSavedCreditCards.clicked.connect(self.GoToListCreditCards)
        self.GetACreditCardInfos.clicked.connect(self.GoToGetInfos)
        self.UpdateACreditCardInfos.clicked.connect(self.GoToUpdateInfos)
        self.DeleteAnExistingCreditCard.clicked.connect(self.GoToDeleteCreditCard)
        self.Exit.clicked.connect(self.Quit)
        self.ReturnButton.clicked.connect(self.Return)

    def GoToAddANewCreditCard(self):
        addACreditCard = AddACreditCard()
        widget.addWidget(addACreditCard)
        widget.setFixedWidth(800)
        widget.setFixedHeight(525)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToListCreditCards(self):
        listAllCreditCards = ListAllCreditCards()
        widget.addWidget(listAllCreditCards)
        widget.setFixedWidth(745)
        widget.setFixedHeight(525)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToGetInfos(self):
        getACreditCardInfos = GetACreditCardInfos()
        widget.addWidget(getACreditCardInfos)
        widget.setFixedWidth(765)
        widget.setFixedHeight(525)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToUpdateInfos(self):
        creditCardSelection = CreditCardSelection()
        widget.addWidget(creditCardSelection)
        widget.setFixedWidth(630)
        widget.setFixedHeight(355)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToDeleteCreditCard(self):
        deleteACreditCard = DeleteACreditCard()
        widget.addWidget(deleteACreditCard)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Return(self):
        serviceSelection = ServiceSelection()
        widget.addWidget(serviceSelection)
        widget.setFixedWidth(600)
        widget.setFixedHeight(350)
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
            if CheckEmail(account_email) == False:
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
                accountUserMenu = AccountUserMenu()
                widget.addWidget(accountUserMenu)
                widget.setFixedWidth(750)
                widget.setFixedHeight(515)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            
            except sqlite3.Error:
                ShowWarningPopup("Error Occured, Try Again Later.")
            
            break

    def Return(self):
        accountUserMenu = AccountUserMenu()
        widget.addWidget(accountUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(515)
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
        accountUserMenu = AccountUserMenu()
        widget.addWidget(accountUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(515)
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
        accountUserMenu = AccountUserMenu()
        widget.addWidget(accountUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(515)
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
            # Listing All The Accounts
            self.Table.setRowCount(accounts_number)
            tableRow = 0
            for row in accounts:
                self.Table.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(row[0]))
                tableRow += 1

    def Return(self):
        accountUserMenu = AccountUserMenu()
        widget.addWidget(accountUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(515)
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
        accountUserMenu = AccountUserMenu()
        widget.addWidget(accountUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(515)
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
            accountUserMenu = AccountUserMenu()
            widget.addWidget(accountUserMenu)
            widget.setFixedWidth(750)
            widget.setFixedHeight(515)
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
        if CheckEmail(email) == True:
            try:
                update_account_email(user_id, email, account)
                ShowInformationPopup("Success", "Account's Email Updated Successfully !")
                accountUserMenu = AccountUserMenu()
                widget.addWidget(accountUserMenu)
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
                accountUserMenu = AccountUserMenu()
                widget.addWidget(accountUserMenu)
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
        accountUserMenu = AccountUserMenu()
        widget.addWidget(accountUserMenu)
        widget.setFixedWidth(730)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class AddACreditCard(QDialog):
    def __init__(self):
        super(AddACreditCard, self).__init__()
        loadUi("add_a_new_cc.ui", self)
        self.Add.clicked.connect(self.AddCreditCard)
        self.Exit.clicked.connect(self.Quit)
        self.ReturnButton.clicked.connect(self.Return)

    def AddCreditCard(self):
        cardName = self.CardName.text()
        cardholderName = self.CardholderName.text()
        cardNumber = self.CardNumber.text()
        cardExpDate = self.CardExpirationDate.text()
        cardCVV = self.CardCVV.text()

        all_ccs = get_existing_credit_cards(user_id)

        # Getting the credit card's name and checking if it already exists 
        condition = True
        for cc in all_ccs:
            if cardName == cc[0]:
                ShowWarningPopup("Credit Card Already Exists !")
                condition = False
                break
        else:
            condition = True

        while condition:
            # Fields shouldn't be empty
            if (len(cardName) == 0) or (len(cardholderName) == 0) or (len(cardNumber) == 0) or (len(cardExpDate) == 0) or (len(cardCVV) == 0):
                ShowWarningPopup("All Required Infos Should Be Given !")
                break

            # Condition on the card's number
            if ((len(cardNumber) < 13) or (len(cardNumber) > 19)):
                ShowWarningPopup("This Credit Card's Number Isn't Valid !")
                break
            
            # Condition on the card's expiration date
            if CheckExpirationDate(cardExpDate) == False:
                ShowWarningPopup("This Credit Card Expiration Date Isn't Valid !")
                break

            # Condition on the card's CVV
            if (len(cardCVV) != 3) or (cardCVV.isdigit() == False):
                ShowWarningPopup("This Credit Card's CVV Isn't Valid !")
                break

            encrypted_CVV = encrypt_password(key, cardCVV)
            encrypted_Number = encrypt_password(key, cardNumber)

            try:
                add_credit_card(cardName, cardholderName, encrypted_Number, encrypted_CVV, cardExpDate, user_id)
                ShowInformationPopup("Success", "Credit Card Added Successfully !")
                creditCardUserMenu = CreditCardUserMenu()
                widget.addWidget(creditCardUserMenu)
                widget.setFixedWidth(750)
                widget.setFixedHeight(510)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                break
            except sqlite3.Error:
                ShowWarningPopup("An Error Occured, Try Again Later !")
                break


    def Return(self):
        creditCardUserMenu = CreditCardUserMenu()
        widget.addWidget(creditCardUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class CreditCardSelection(QDialog):
    def __init__(self):
        super(CreditCardSelection, self).__init__()
        loadUi("credit_card_to_update.ui", self)
        self.Confirm.clicked.connect(self.SelectCreditCard)
        self.ExitButton.clicked.connect(self.Quit)
        self.ReturnButton.clicked.connect(self.Return)

    def SelectCreditCard(self):
        global cc_name
        cc_name = self.CreditCardName.text()

        # Checking if the credit card already exists
        all_ccs = get_existing_credit_cards(user_id)

        exists = False
        for cc in all_ccs:
            if cc[0] == cc_name:
                exists = True

        if exists == False:
            ShowWarningPopup("Account Doesn't Exist !")
            
        else:
            updateACreditCardInfos = UpdateACreditCardInfos()
            widget.addWidget(updateACreditCardInfos)
            widget.setFixedWidth(620)
            widget.setFixedHeight(435)
            widget.setCurrentIndex(widget.currentIndex() + 1)


    def Return(self):
        creditCardUserMenu = CreditCardUserMenu()
        widget.addWidget(creditCardUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(520)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class GetACreditCardInfos(QDialog):
    def __init__(self):
        super(GetACreditCardInfos, self).__init__()
        loadUi("get_a_cc_infos.ui", self)
        self.Show.clicked.connect(self.ShowCreditCardInfos)
        self.Exit.clicked.connect(self.Quit)
        self.ReturnButton.clicked.connect(self.Return)

    def ShowCreditCardInfos(self):
        cc_name = self.CreditCardName.text()
        while True:
            if (len(cc_name) == 0):
                ShowWarningPopup("Please Fill In The Field")
                break

            all_ccs = get_existing_credit_cards(user_id)
            if len(all_ccs) == 0:
                ShowWarningPopup("There Are No Accounts Saved !")
                break

            else:
                # Checking if the credit card already exists
                exists = False
                for acc in all_ccs:
                    if acc[0] == cc_name:
                        exists = True

                if exists == False:
                    ShowWarningPopup("Account Doesn't Exist !")
                    break

                else:
                    cc_name, ccholder_name, cc_number, cc_CVV, cc_exp_date = get_credit_card_infos(user_id, cc_name)

                    decrypted_cc_number = decrypt_password(key, cc_number)
                    decrypted_cc_CVV = decrypt_password(key, cc_CVV) 

                    self.CreditCardholderName.setText(ccholder_name)
                    self.CreditCardNumber.setText(decrypted_cc_number)
                    self.CreditCardExpirationDate.setText(cc_exp_date)
                    self.CreditCardCVV.setText(decrypted_cc_CVV)
                    break



    def Return(self):
        creditCardUserMenu = CreditCardUserMenu()
        widget.addWidget(creditCardUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class ListAllCreditCards(QDialog):
    def __init__(self):
        super(ListAllCreditCards, self).__init__()
        loadUi("all_saved_ccs.ui", self)
        self.Show.clicked.connect(self.GetInfos)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)


    def GetInfos(self): 
        # Function to display the credit cards
        all_ccs = get_existing_credit_cards(user_id)
        if len(all_ccs) == 0:
            ShowWarningPopup("There Are No Credit Cards Saved !")

        else:
            # Getting the number of rows
            ccs_number = len(all_ccs)
            # Listing All The Credit Cards
            self.Table.setRowCount(ccs_number)
            tableRow = 0
            for row in all_ccs:
                self.Table.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(row[0]))
                tableRow += 1


    def Return(self):
        creditCardUserMenu = CreditCardUserMenu()
        widget.addWidget(creditCardUserMenu)
        widget.setFixedWidth(750)
        widget.setFixedHeight(510)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class UpdateACreditCardInfos(QDialog):
    def __init__(self):
        super(UpdateACreditCardInfos, self).__init__()
        loadUi("update_a_credit_card_infos.ui", self)
        self.UpdateCardName.clicked.connect(self.GoToUpdateCCName)
        self.UpdateCardholderName.clicked.connect(self.GoToUpdateCCholderName)
        self.UpdateNumber.clicked.connect(self.GoToUpdateCCNumber)
        self.UpdateCVV.clicked.connect(self.GoToUpdateCC_CVV)
        self.UpdateExpirationDate.clicked.connect(self.GoToUpdateCCExpirationDate)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def GoToUpdateCCName(self):
        updateCardName = UpdateCardName()
        widget.addWidget(updateCardName)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToUpdateCCholderName(self):
        updateCardholderName = UpdateCardholderName()
        widget.addWidget(updateCardholderName)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToUpdateCCNumber(self):
        updateCardNumber = UpdateCardNumber()
        widget.addWidget(updateCardNumber)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToUpdateCC_CVV(self):
        updateCardCVV = UpdateCardCVV()
        widget.addWidget(updateCardCVV)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToUpdateCCExpirationDate(self):
        updateCardExpirationDate = UpdateCardExpirationDate()
        widget.addWidget(updateCardExpirationDate)
        widget.setFixedWidth(620)
        widget.setFixedHeight(450)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Return(self):
        creditCardSelection = CreditCardSelection()
        widget.addWidget(creditCardSelection)
        widget.setFixedWidth(625)
        widget.setFixedHeight(345)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class UpdateCardName(QDialog):
    def __init__(self):
        super(UpdateCardName, self).__init__()
        loadUi("update_card_name.ui", self)
        self.Update.clicked.connect(self.UpdateCCName)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def UpdateCCName(self):
        credit_card = self.CardName.text()
        while True:
            if (len(credit_card) == 0):
                ShowWarningPopup("Please Fill In The Field")
                break
            try:
                update_credit_card_name(user_id, credit_card, cc_name)
                ShowInformationPopup("Success", f"Credit Card's Name Updated Successfully !")
                updateACreditCardInfos = UpdateACreditCardInfos()
                widget.addWidget(updateACreditCardInfos)
                widget.setFixedWidth(620)
                widget.setFixedHeight(435)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                break
            except sqlite3.Error:
                ShowWarningPopup("An Error Occured, Try Again Later !")
                break


    def Return(self):
        updateACreditCardInfos = UpdateACreditCardInfos()
        widget.addWidget(updateACreditCardInfos)
        widget.setFixedWidth(620)
        widget.setFixedHeight(435)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class UpdateCardholderName(QDialog):
    def __init__(self):
        super(UpdateCardholderName, self).__init__()
        loadUi("update_cardholder_name.ui", self)
        self.Update.clicked.connect(self.UpdateCCholderName)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def UpdateCCholderName(self):
        credit_cardholder_name = self.CardholderName.text()
        while True:
            if (len(credit_cardholder_name) == 0):
                ShowWarningPopup("Please Fill In The Field")
                break
            try:
                update_credit_cardholder_name(user_id, credit_cardholder_name, cc_name)
                ShowInformationPopup("Success", "Credit Cardholder's Name Updated Successfully !")
                updateACreditCardInfos = UpdateACreditCardInfos()
                widget.addWidget(updateACreditCardInfos)
                widget.setFixedWidth(620)
                widget.setFixedHeight(435)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                break
            except sqlite3.Error:
                ShowWarningPopup("An Error Occured, Try Again Later !")
                break


    def Return(self):
        updateACreditCardInfos = UpdateACreditCardInfos()
        widget.addWidget(updateACreditCardInfos)
        widget.setFixedWidth(620)
        widget.setFixedHeight(435)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class UpdateCardNumber(QDialog):
    def __init__(self):
        super(UpdateCardNumber, self).__init__()
        loadUi("update_card_number.ui", self)
        self.Update.clicked.connect(self.UpdateCCNumber)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def UpdateCCNumber(self):
        credit_card_number = self.CardNumber.text()
        while True:
            if (len(credit_card_number) == 0):
                ShowWarningPopup("Please Fill In The Field")
                break
            if ((len(credit_card_number) < 13) or (len(credit_card_number) > 19) or (credit_card_number.isdigit() == False)):
                ShowWarningPopup("The Given Credit Card's Number Isn't Valid !")
                break
            
            encrypted_number = encrypt_password(key, credit_card_number)
            try:
                update_credit_card_number(user_id, encrypted_number, cc_name)
                ShowInformationPopup("Success", "Credit Card's Number Updated Successfully !")
                updateACreditCardInfos = UpdateACreditCardInfos()
                widget.addWidget(updateACreditCardInfos)
                widget.setFixedWidth(620)
                widget.setFixedHeight(435)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                break
            except sqlite3.Error:
                ShowWarningPopup("An Error Occured, Try Again Later !")
                break


    def Return(self):
        updateACreditCardInfos = UpdateACreditCardInfos()
        widget.addWidget(updateACreditCardInfos)
        widget.setFixedWidth(620)
        widget.setFixedHeight(435)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class UpdateCardExpirationDate(QDialog):
    def __init__(self):
        super(UpdateCardExpirationDate, self).__init__()
        loadUi("update_card_expiration_date.ui", self)
        self.Update.clicked.connect(self.UpdateCCExpirationDate)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def UpdateCCExpirationDate(self):
        cc_exp_date = self.CardExpirationDate.text()
        while True:
            if (len(cc_exp_date) == 0):
                ShowWarningPopup("Please Fill In The Field")
                break
            if CheckExpirationDate(cc_exp_date) == False:
                ShowWarningPopup("This Given Credit Card's Expiration Date Isn't Valid !")
                break
            try:
                update_credit_card_expiration_date(user_id, cc_exp_date, cc_name)
                ShowInformationPopup("Success", "Credit Card's Expiration Date Updated Successfully !")
                updateACreditCardInfos = UpdateACreditCardInfos()
                widget.addWidget(updateACreditCardInfos)
                widget.setFixedWidth(620)
                widget.setFixedHeight(435)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                break
            except sqlite3.Error:
                ShowWarningPopup("An Error Occured, Try Again Later !")
                break


    def Return(self):
        updateACreditCardInfos = UpdateACreditCardInfos()
        widget.addWidget(updateACreditCardInfos)
        widget.setFixedWidth(620)
        widget.setFixedHeight(435)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class UpdateCardCVV(QDialog):
    def __init__(self):
        super(UpdateCardCVV, self).__init__()
        loadUi("update_card_CVV.ui", self)
        self.Update.clicked.connect(self.UpdateCVV)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def UpdateCVV(self):
        cc_CVV = self.CardCVV.text()
        while True:
            if (len(cc_CVV) == 0):
                ShowWarningPopup("Please Fill In The Field")
                break
            if (cc_CVV.isdigit() == False) or (len(cc_CVV) != 3):
                ShowWarningPopup("This Given Credit Card's CVV Isn't Valid !")
                break
                
            encrypted_CVV = encrypt_password(key, cc_CVV)
            try:
                update_credit_card_CVV(user_id, encrypted_CVV, cc_name)
                ShowInformationPopup("Success", "Credit Card's CVV Updated Successfully !")
                updateACreditCardInfos = UpdateACreditCardInfos()
                widget.addWidget(updateACreditCardInfos)
                widget.setFixedWidth(620)
                widget.setFixedHeight(435)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                break
            except sqlite3.Error:
                ShowWarningPopup("An Error Occured, Try Again Later !")
                break


    def Return(self):
        updateACreditCardInfos = UpdateACreditCardInfos()
        widget.addWidget(updateACreditCardInfos)
        widget.setFixedWidth(620)
        widget.setFixedHeight(435)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Quit(self):
        sys.exit()


class DeleteACreditCard(QDialog):
    def __init__(self):
        super(DeleteACreditCard, self).__init__()
        loadUi("delete_a_credit_card.ui", self)
        self.Delete.clicked.connect(self.DelCreditCard)
        self.ReturnButton.clicked.connect(self.Return)
        self.Exit.clicked.connect(self.Quit)

    def DelCreditCard(self):
        credit_card = self.Name.text()
        while True:
            if len(credit_card) == 0:
                ShowWarningPopup("Please Fill In The Field")
                break
            # Getting the credit card's name and checking if it already exists 
            all_ccs = get_existing_credit_cards(user_id)

            condition = True
            for cc in all_ccs:
                if cc[0] == credit_card:
                    break
            else:
                condition = False

            # In case the given credit card doesn't exist in the database
            if condition == False:
                ShowWarningPopup(f"This Given Credit Card Doesn't Exist !")
                break
            else:
                try:
                    delete_credit_card(user_id, credit_card)
                    ShowInformationPopup("Success", f"Credit Card [{credit_card}] Deleted Successfully !")
                    creditCardUserMenu = CreditCardUserMenu()
                    widget.addWidget(creditCardUserMenu)
                    widget.setFixedWidth(740)
                    widget.setFixedHeight(510)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                    break
                except sqlite3.Error:
                    ShowWarningPopup("An Error Occured, Try Again Later !")
                    break
            

    def Return(self):
        creditCardUserMenu = CreditCardUserMenu()
        widget.addWidget(creditCardUserMenu)
        widget.setFixedWidth(750)
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
    widget.setWindowTitle("Louay's Password Manager ")
    widget.show()
    app.exec_()
    