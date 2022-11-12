import sqlite3
from os import path
from db_functions import (create_db, usernames_list, get_account_infos, get_existing_accounts, get_hashed_password,
    get_key, get_user_id, add_account, add_user, update_account_password, update_account_username, delete_account,
    delete_user, update_account_email)
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


def user_menu():
    print("---------------------------------------------------")
    print("| Enter the number of the action you want to do : |")
    print("|           [1] : Add A New Account               |")
    print("|           [2] : List All Saved Accounts         |")
    print("|           [3] : Get An Account's Infos          |")
    print("|           [4] : Update An Account's Infos       |")
    print("|           [5] : Delete An Account               |")
    print("|           [6] : Quit                            |")
    print("---------------------------------------------------")

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


def main():
    Library()
    if not path.exists('passwords.db'):
        create_db()

    SleepClear(0)
    while True:
        first_choice = main_menu()

        if first_choice not in ['1', '2', '3', '4']:
            print("Please enter a valid choice !")
            SleepClear(1)


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
                    second_choice = user_menu()
                    if second_choice not in ['1','2','3','4','5','6']:
                        print("Please Enter a valid choice !")
                        SleepClear(1)

                    elif second_choice == '1':
                        AddAccount(key, username)
                        #SleepClear()
                    elif second_choice == '2':
                        ListAllExistingAccounts(username)
                        # SleepClear()
                    elif second_choice == '3':
                        ListAccountInfo(username, key)
                        # SleepClear()
                    elif second_choice == '4':
                        UpdateAccountInfo(username)
                        SleepClear(1.5)
                    elif second_choice == '5':
                        DeleteAccount(username)
                        SleepClear(1.25)
                    elif second_choice == '6':
                        SleepClear(0)
                        exit()
                
        elif first_choice == '2':
            SignUp()

        
        elif first_choice == '3':
            DeleteUser()
            

        elif first_choice == '4':
            SleepClear(0)
            exit()


if __name__ == '__main__':
    main()
