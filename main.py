import sqlite3
from os import path
from db_functions import (create_db, usernames_list, get_account_infos, get_existing_accounts, get_hashed_password,
    get_key, get_user_id, add_account, add_user, update_account_password, update_account_username, delete_account,
    delete_user, update_account_email, add_credit_card, delete_credit_card, update_credit_card_CVV, update_credit_card_expiration_date,
    update_credit_card_name, update_credit_card_number, update_credit_cardholder_name, get_existing_credit_cards,
    get_credit_card_infos)
from encryption_functions import (generate_key, get_hash, encrypt_password, decrypt_password)
from other_functions import (SleepClear, Error, Message, Check, Library)


def AllUsers():
    all_users = usernames_list()
    return all_users


def main_menu():
    print("---------------------------------------------------")
    print("| Enter the number of the action you want to do : |")
    print("|                [1] : Sign In                    |")
    print("|                [2] : Sign Up                    |")
    print("|                [3] : Delete A User              |")
    print("|                [4] : Quit                       |")
    print("---------------------------------------------------")

    answer = input('=> Answer : ')

    return answer


def service_menu():
    print("--------------------------------------------------------")
    print("| Enter the number of the service you want to select : |")
    print("|                   [1] : Accounts                     |")
    print("|                   [2] : Credit Cards                 |")
    print("|                   [3] : Quit                         |")
    print("--------------------------------------------------------")

    answer = input("=> Answer : ")

    return answer


def accounts_user_menu():
    print("---------------------------------------------------")
    print("| Enter the number of the action you want to do : |")
    print("|           [1] : Add A New Account               |")
    print("|           [2] : List All Saved Accounts         |")
    print("|           [3] : Get An Account's Infos          |")
    print("|           [4] : Update An Account's Infos       |")
    print("|           [5] : Delete An Account               |")
    print("|           [6] : Return                          |")
    print("|           [7] : Quit                            |")
    print("---------------------------------------------------")

    answer = input('=> Answer : ')

    return answer


def credit_cards_user_menu():
    print("-------------------------------------------------------")
    print("|   Enter the number of the action you want to do :   |")
    print("|            [1] : Add A New Credit Card              |")
    print("|            [2] : List All Saved Credit Cards        |")
    print("|            [3] : Get A Credit Card's Infos          |")
    print("|            [4] : Update A Credit Card's Infos       |")
    print("|            [5] : Delete A Credit Card               |")
    print("|            [6] : Return                             |")
    print("|            [7] : Quit                               |")
    print("-------------------------------------------------------")

    answer = input('=> Answer : ')

    return answer


def check_user(username, provided_hash):
    # Checking the ressemblance
    for user in AllUsers():
        if username == user[0]:
            if str(provided_hash) == str(get_hashed_password(username)):
                return True
            else:
                return False
    else:
        return None


def SignIn():
    # Sign In
    username = input("What is your username? : ")
    provided_password = input("What is your master password? : ")
    provided_hash = get_hash(provided_password)

    accessed = check_user(username, provided_hash)

    return accessed, username


def SignUp():
    # Getting the username and checking if it is valid or not
    condition = False
    while not condition:
        username = input("Enter your username : ")
        for name in AllUsers():
            if name[0] == username:
                print("Username already exists !")
                break
        else :
            condition = True

    # Getting a master password and hashing it
    hashed_master_pwd = get_hash(input("Enter your master password : "))

    # Generating a key
    key = generate_key()

    try :
        add_user(username, hashed_master_pwd, key)
        Message('User added successully!')

    except sqlite3.Error :
        Message("Error Occured , Try Again Later.")


def DeleteUser():
    # Get the username and the master password of the user that will be deleted
    username = input("What's Your Username ? : ")
    hashed_password = get_hash(input("What's Your Master Password ? : "))

    # Verifying if the user exists in the database or not 
    verification = check_user(username, hashed_password)

    if verification == True:
        delete_user(get_user_id(username))
        print("User Deleted Successfully !")

    elif verification == False:
        print("Access Denied !")

    elif verification == None:
        print("The Provided Infos Doesn't Exist !")


def AddAccount(key, username):    
    user_id = get_user_id(username)
    all_accounts = get_existing_accounts(user_id)

    # Getting the account's name and checking if it already exists 
    condition = True
    while condition:
        acc_name = input("Enter The Account's Name : ")
        for account in all_accounts:
            if acc_name == account[0]:
                Message("Account Already Exists !")
                break
        else:
            condition = False

    # Getting the remaining infos
    username = input("Enter The Username : ")

    # Getting an email address and verifying if it's valid or not
    email = input("Enter The Account's Email : ")
    while Check(email) == False:
        print("This Email Address Isn't Valid !")
        email = input("Enter The Account's Email : ")

    # Getting a password and a password verification to make sure no typo happened
    password = input("Enter The Account's Password : ")
    confirmation = input("Enter The Account's Password Again For Confirmation : ")

    while password != confirmation :
        Message("The Password And Its Confirmation Doesn't Match; Try Again !")
        
        password = input("Enter The Password : ")
        confirmation = input("Enter The Password Again For Confirmation : ")        

    # Encrypting Password  
    encrypted_password = encrypt_password(key, password)

    try:
        add_account(acc_name, username, email, encrypted_password, user_id)
        Message(f"Account [ {acc_name} ] Added Successfully !")
        SleepClear(1.1)
    except sqlite3.Error:
        Error()


def ListAllExistingAccounts(username):
    user_id = get_user_id(username)
    accounts = get_existing_accounts(user_id)
    
    if len(accounts) == 0:
        Message("There Is No Account Saved !")

    SleepClear(1.1)

    # Listing All The Accounts
    for i in range(len(accounts)):
        Message(f"Account {i + 1} : {accounts[i][0]}")


def ListAccountInfo(username, key):
    user_id = get_user_id(username)
    all_accounts = get_existing_accounts(user_id)
    if len(all_accounts) == 0:
        Message("There Are No Accounts Saved !")

    else:
        account_name = input("Which Account You Want To See Its Infos ? : ")

        # Checking if the account already exists
        exists = False
        for acc in all_accounts:
            if acc[0] == account_name:
                exists = True

        if exists == False:
            Message("Account Doesn't Exist !")

        account_username, email, encrypted_account_password = get_account_infos(user_id, account_name)

        decrypted_account_password = decrypt_password(key, encrypted_account_password)

        Message(f"Account Name : {account_name}")
        Message(f"Account Username : {account_username}")
        Message(f"Account Email : {email}")
        Message(f"Account Password : {decrypted_account_password}")


def UpdateAccountInfo(username):
    user_id = get_user_id(username)
    key = get_key(user_id)
    account = input("Which Account You Want To Update Its Infos ? :")

    # Checking if the account already exists
    all_accounts = get_existing_accounts(user_id)

    exists = False
    for acc in all_accounts:
        if acc[0] == account:
            exists = True

    if exists == False:
        Message("Account Doesn't Exist !")

    while True:
        # Updating the account's infos
        print("----------------------------")
        print("|  [1] : Update Username   |")
        print("|  [2] : Update Email      |")
        print("|  [3] : Update Password   |")
        print("----------------------------")

        choice = input()

        if choice not in ['1', '2', '3']:
            Message("Please Enter A Valid Choice ")
        
        elif choice == '1':
            new_username = input("Enter The New Username : ")
            try:
                update_account_username(user_id, new_username, account)
                break
            except sqlite3.Error:
                Error()

        elif choice == '2':
            new_email = input("Enter The New Email : ")
            while Check(new_email) == False:
                print("This Email Address Isn't Valid !")
                new_email = input("Enter The New Email : ")
            try:
                update_account_email(user_id, new_email, account)
                break
            except sqlite3.Error:
                Error()

        elif choice == '3':
            new_password = input("Enter The New Password : ")
            encrypted_new_password = encrypt_password(key, new_password)
            try:
                update_account_password(user_id, encrypted_new_password, account)
                break
            except sqlite3.Error:
                Error()


def DeleteAccount(username):
    user_id = get_user_id(username)
    
    # Getting the account's name and checking if it already exists 
    account = input("Which Account You Want To Delete ? :")
    all_accounts = get_existing_accounts(user_id)

    condition = True
    for acc in all_accounts:
        if acc[0] == account:
            SleepClear(1.5)
            break
    else:
        condition = False
    
    # In case the given account doesn't exist in the database
    if condition == False:
        Message(f"Account [ {account} ] Doesn't Exist !")

    else :
        try:
            delete_account(user_id, account)
            Message(f"Account [{account}] Deleted Successfully !")
        except sqlite3.Error:
            Error()


def AddCreditCard(key, username):
    user_id = get_user_id(username)
    all_ccs = get_existing_credit_cards(user_id)

    # Getting the credit card's name and checking if it already exists 
    condition = True
    while condition:
        cc_name = input("Enter The Credit Card's Name : ")
        for cc in all_ccs:
            if cc_name == cc[0]:
                Message("Credit Card Already Exists !")
                break
        else:
            condition = False

    # Getting the remaining infos
    cardholder_name = input("Enter The Cardholder Name : ")

    # Getting the number 
    number = input("Enter The Credit Card's Number : ")
    while ((len(number) < 13) or (len(number) > 19)):
        print("This Credit Card Number Isn't Valid !")
        number = input("Enter The Credit Card's Number : ")

    # Getting the expiration date
    exp_date = input("Enter The Credit Card's Expiration Date ( Type MM/YY ) : ")
    while (len(exp_date) != 5) or (exp_date[0:2].isdigit() == False) or (exp_date[3:-1].isdigit() == False) or (exp_date[2] != '/') or (int(exp_date[0:2]) > 12) :
        print("This Credit Card Expiration Date Isn't Valid !")
        # print("exp_date[0:2] : ", exp_date[0:2])
        # print("exp_date[3:-1] : ", exp_date[3:-1])
        # print("exp_date[2] : ", exp_date[2])
        # print("int(exp_date[0:2]) : ", int(exp_date[0:2]))
        exp_date = input("As An Example On How To Enter The Expiration Date, You Could Type 07/24 \n-Enter The Credit Card's Expiration Date ( Type MM/YY ) : ")
    
    # Getting the CVV
    cvv = input("Enter The Credit Card's CVV : ")
    while (cvv.isdigit() == False) or (len(cvv) != 3):
        print("This Credit Card CVV Isn't Valid !")
        cvv = input("Enter The Credit Card's CVV : ")
       

    # Encrypting Credit Card's Number ( using the same function that encrypts passwords for accounts )
    encrypted_number = encrypt_password(key, number)

    try:
        add_credit_card(cc_name, cardholder_name, encrypted_number, int(cvv), exp_date, user_id)
        Message(f"Credit Card [ {cc_name} ] Added Successfully !")
        SleepClear(1.1)
    except sqlite3.Error:
        Error()


def UpdateCreditCardInfo(username):
    # TODO : implement getpass
    user_id = get_user_id(username)
    key = get_key(user_id)
    credit_card = input("Which Credit Card You Want To Update Its Infos ? :")

    # Checking if the account already exists
    all_ccs = get_existing_credit_cards(user_id)

    exists = False
    for cc in all_ccs:
        if cc[0] == credit_card:
            exists = True

    if exists == False:
        Message("Account Doesn't Exist !")

    while True:
        # Updating the credit card's infos
        print("--------------------------------------------")
        print("|      [1] : Update Card Name              |")
        print("|      [2] : Update Card Holder Name       |")
        print("|      [3] : Update Card Number            |")
        print("|      [4] : Update Card Expiration Date   |")
        print("|      [5] : Update Card CVV               |")
        print("|      [6] : Quit                          |")
        print("--------------------------------------------")

        choice = input("=> Answer : ")

        if choice not in ['1', '2', '3', '4', '5', '6']:
            Message("Please Enter A Valid Choice ")

        elif choice == '1':
            card_name = input("Enter The New Card's Name : ")
            updated = False
            try:
                update_credit_card_name(user_id, card_name, credit_card)
                Message(f"Credit Card [{card_name}] Name Updated Successfully !")
                updated = True
            except sqlite3.Error:
                Error()
            
            if updated == True:
                credit_card = card_name
        
        elif choice == '2':
            cardholder_name = input("Enter The New Cardholder's Name : ")
            try:
                update_credit_cardholder_name(user_id, cardholder_name, credit_card)
                Message(f"Credit Card [{credit_card}] Holder Name Updated Successfully !")
            except sqlite3.Error:
                Error()

        elif choice == '3':
            card_number = input("Enter The New Card's Number : ")
            while (len(card_number) < 13) or (len(card_number) > 19):
                print("This Card's Number Isn't Valid !")
                card_number = input("Enter The New Card's Number : ")
            try:
                encrypted_number = encrypt_password(key, card_number)
                update_credit_card_number(user_id, encrypted_number, credit_card)
                Message(f"Credit Card [{credit_card}] Name Updated Successfully !")
            except sqlite3.Error:
                Error()

        elif choice == '4':
            exp_date = input("Enter The New Card's Expiration Date : ")
            while (len(exp_date) != 5) or (exp_date[0:2].isdigit() == False) or (exp_date[3:-1].isdigit() == False) or (exp_date[2] != '/') or (int(exp_date[0:2]) > 12) :
                print("This Car's Expiration Date Isn't Valid !")
                exp_date = input("Enter The New Card's Expiration Date : ")

            try:
                update_credit_card_expiration_date(user_id, exp_date, credit_card)
                Message(f"Credit Card [ {credit_card} ] Expiration Date Updated Successfully !")
            except sqlite3.Error:
                Error()

        elif choice == '5':
            new_cvv = input("Enter The New Card's CVV : ")
            while (new_cvv.isdigit() == False) or (len(new_cvv) != 3):
                print("This Card's CVV Isn't Valid !")
                new_cvv = input("Enter The New Card's CVV : ")

            try:
                update_credit_card_CVV(user_id, new_cvv, credit_card)
                Message(f"Credit Card [ {credit_card} ] CVV Updated Successfully")
            
            except sqlite3.Error:
                Error()

        elif choice == "6":
            exit()
    

def DeleteCreditCard(username):
    user_id = get_user_id(username)

    # Getting the credit card's name and checking if it already exists 
    credit_card = input("Which Credit Card You Want To Delete ? :")
    all_ccs = get_existing_credit_cards(user_id)

    condition = True
    for cc in all_ccs:
        if cc[0] == credit_card:
            SleepClear(1.5)
            break
    else:
        condition = False

    # In case the given credit card doesn't exist in the database
    if condition == False:
        Message(f"Credit Card [ {credit_card} ] Doesn't Exist !")
    else:
        try:
            delete_credit_card(user_id, credit_card)
            Message(f"Credit Card [ {credit_card} ] Deleted Successfully !")
        except sqlite3.Error:
            Error()


def ListAllExistingCreditCards(username):
    user_id = get_user_id(username)
    all_ccs = get_existing_credit_cards(user_id)
    
    if len(all_ccs) == 0:
        Message("There Are No Credit Cards Saved !")

    SleepClear(0)

    # Listing All The Accounts
    for i in range(len(all_ccs)):
        Message(f"Credit Card {i + 1} : {all_ccs[i][0]}")


def ListCreditCardInfo(username, key):
    user_id = get_user_id(username)
    all_ccs = get_existing_credit_cards(user_id)
    if len(all_ccs) == 0:
        Message("There Are No Credit Cards Saved !")

    else:
        credit_card_name = input("Which Credit Card You Want To See Its Infos ? : ")

        # Checking if the credit card already exists
        exists = False
        for cc in all_ccs:
            if cc[0] == credit_card_name:
                exists = True

        if exists == False:
            Message("Credit Card Doesn't Exist !")

        cc_name, ccholder_name, encrypted_cc_number, cc_CVV, cc_exp_date = get_credit_card_infos(user_id, credit_card_name)

        decrypted_cc_number = decrypt_password(key, encrypted_cc_number)

        Message(f"Credit Card Name : {cc_name}")
        Message(f"Credit Cardholder Name : {ccholder_name}")
        Message(f"Credit Card's Number : {decrypted_cc_number}")
        Message(f"Credit Card's Expiration Date : {cc_exp_date}")
        Message(f"Credit Card's CVV : {cc_CVV}")


def main():
    Library()
    if not path.exists('passwords.db'):
        create_db()

    SleepClear(0)
    while True:
        first_choice = main_menu()

        if first_choice not in ['1', '2', '3', '4']:
            print("Please Enter A Valid Choice !")
            SleepClear(1)

        # The User selects Signing in
        elif first_choice == '1':
            condition, username = SignIn()

            if condition == False:
                print("Access Blocked !")
                SleepClear(0.75)

            elif condition == None:
                print("Entered Infos Doesn't Match With Any User Infos In Our Database !")
                SleepClear(1.5)

            elif condition == True:
                Message(f"User [ {username} ] Signed In Successfully.")
                SleepClear(1)
                key = get_key(get_user_id(username))
                
                while True:
                    # The user has to choose between selecting accounts or credit cards
                    second_choice = service_menu()
                    if second_choice not in ['1', '2', '3']:
                        print("Please Enter A Valid Choice !")
                        SleepClear(1)

                    # The user selects accounts 
                    elif second_choice == '1':
                        third_choice = accounts_user_menu()
                        if third_choice not in ['1','2','3','4','5','6']:
                            print("Please Enter a valid choice !")
                            SleepClear(1)

                        elif third_choice == '1':
                            AddAccount(key, username)
                            #SleepClear()
                        elif third_choice == '2':
                            ListAllExistingAccounts(username)
                            # SleepClear()
                        elif third_choice == '3':
                            ListAccountInfo(username, key)
                            # SleepClear()
                        elif third_choice == '4':
                            UpdateAccountInfo(username)
                            SleepClear(1.5)
                        elif third_choice == '5':
                            DeleteAccount(username)
                            SleepClear(1.25)

                        elif third_choice == '6':
                            pass

                        elif third_choice == '7':
                            SleepClear(0)
                            exit()

                    # The user selects credit cards
                    elif second_choice == '2':
                        fourth_choice = credit_cards_user_menu()
                        if fourth_choice not in ['1','2','3','4','5','6']:
                            print("Please Enter a valid choice !")
                            SleepClear(1)
                        
                        elif fourth_choice == '1':
                            AddCreditCard(key, username)
                            #SleepClear()
                        elif fourth_choice == '2':
                            ListAllExistingCreditCards(username)
                            # SleepClear()
                        elif fourth_choice == '3':
                            ListCreditCardInfo(username, key)
                            # SleepClear()
                        elif fourth_choice == '4':
                            UpdateCreditCardInfo(username)
                            # SleepClear(1.5)
                        elif fourth_choice == '5':
                            DeleteCreditCard(username)
                            SleepClear(1.25)
                        elif fourth_choice == '6':
                            pass
                        elif fourth_choice == '7':
                            SleepClear(0)
                            exit()
                    
                    # The user quits
                    elif second_choice == '3':
                        exit()

        # The user selects signing up           
        elif first_choice == '2':
            SignUp()

        # The user selects deleting a user
        elif first_choice == '3':
            DeleteUser()
            
        # The user selects            
        elif first_choice == '4':
            SleepClear(0)
            exit()


if __name__ == '__main__':
    main()
