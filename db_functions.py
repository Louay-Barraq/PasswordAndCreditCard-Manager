import sqlite3
 
def connect():
    # Connecting to the database
    connection = sqlite3.connect("passwords.db")
    # Creating the cursor
    cursor = connection.cursor()

    return connection, cursor

def disconnect(connection):
    connection.commit()
    connection.close()


def create_db():
    connection, cursor = connect()
    # Query to create the users' table
    CREATE_USERS_QUERY = """
    CREATE TABLE users (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        master_password BLOB NOT NULL,
        key BLOB NOT NULL);
    """

    cursor.execute(CREATE_USERS_QUERY)

    # Query to create the accounts' table
    CREATE_ACCOUNTS_QUERY = """
    CREATE TABLE accounts (
        account_name TEXT NOT NULL ,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id));
    """

    cursor.execute(CREATE_ACCOUNTS_QUERY)

    disconnect(connection)


def usernames_list():
    connection, cursor = connect()
    # Query to get a list with all the users' names
    USERNAMES_QUERY = """SELECT name FROM users"""

    cursor.execute(USERNAMES_QUERY)
    usernames_list = cursor.fetchall()

    #disconnect(connection)

    return usernames_list


def add_user(name, hashed_mp, key):
    connection, cursor = connect()

    # Query to add a user to the database
    ADD_USER_QUERY = f"""
    INSERT INTO users 
    ("name", "master_password", "key") 
    VALUES ("{name}", "{hashed_mp}", "{key}");
    """

    cursor.execute(ADD_USER_QUERY)
    connection.commit()
    connection.close()


def delete_user(user_id):
    connection, cursor = connect()

    # Query to delete a given user
    DELETE_USER_QUERY = f"""DELETE FROM users WHERE id = {user_id}"""
    DELETE_USERS_SERVICES_QUERY = f"""DELETE FROM accounts WHERE user_id = {user_id}"""

    cursor.execute(DELETE_USER_QUERY)
    cursor.execute(DELETE_USERS_SERVICES_QUERY)

    disconnect(connection)
    

def get_user_id(name):
    connection, cursor = connect()

    #Query to get the id of a user based on his name
    USER_ID_QUERY = f"""SELECT id FROM users WHERE name = "{name}" """

    cursor.execute(USER_ID_QUERY)
    user_id = cursor.fetchone()[0]

    return user_id


def get_hashed_password(name):
    connection, cursor = connect()

    # Query to get the hashed master password of a user

    GET_HASHED_PASSWORD_QUERY = f"""
    SELECT master_password FROM users WHERE name = "{name}";
    """

    cursor.execute(GET_HASHED_PASSWORD_QUERY)
    hashed_master_password = (cursor.fetchone())

    #disconnect(connection)

    return hashed_master_password[0]


def get_key(user_id):
    connection, cursor = connect()

    # Query to get the encryption key of a user
    GET_KEY_QUERY = f"""
    SELECT key FROM users
    WHERE id = "{user_id}";
    """

    cursor.execute(GET_KEY_QUERY)
    key = cursor.fetchone()[0][2::]

    return key


def add_account(account_name, username, email, password, user_id):
    connection, cursor = connect()

    # Query to add a new service for a user
    ADD_SERVICE_QUERY = f"""
    INSERT INTO accounts 
    (account_name, username, email, password, user_id) VALUES 
    ("{account_name}", "{username}", "{email}", "{password}", "{user_id}");
    """

    cursor.execute(ADD_SERVICE_QUERY)

    disconnect(connection)


def update_account_username(user_id, new_username, account_name):
    connection, cursor = connect()

    # Query to update a username of an account of a user
    ACCOUNT_USERNAME_UPDATE_QUERY = f"""
    UPDATE accounts
    SET username = "{new_username}"
    WHERE user_id = "{user_id}" AND account_name = "{account_name}"; 
    """

    cursor.execute(ACCOUNT_USERNAME_UPDATE_QUERY)

    disconnect(connection)


def update_account_email(user_id, new_email, account_name):
    connection, cursor = connect()

    # Query to update an email of an account of a user
    ACCOUNT_EMAIL_UPDATE_QUERY = f"""
    UPDATE accounts
    SET email = "{new_email}"
    WHERE user_id = "{user_id}" AND account_name = "{account_name}";
    """

    cursor.execute(ACCOUNT_EMAIL_UPDATE_QUERY)

    disconnect(connection)


def update_account_password(user_id, new_password, account_name):
    connection, cursor = connect()

    # Query to update a password of an account of a user
    ACCOUNT_PASSWORD_UPDATE_QUERY = f"""
    UPDATE accounts
    SET password = "{new_password}"
    WHERE user_id = "{user_id}" AND account_name = "{account_name}";
    """

    cursor.execute(ACCOUNT_PASSWORD_UPDATE_QUERY)

    disconnect(connection)


def delete_account(user_id, account_name):
    connection, cursor = connect()

    # Query to delete an account of a user
    DELETE_ACCOUNT_USER = f"""
    DELETE FROM accounts
    WHERE user_id = {user_id} AND account_name = "{account_name}";
    """

    cursor.execute(DELETE_ACCOUNT_USER)

    disconnect(connection)


def get_existing_accounts(user_id):
    connection, cursor = connect()

    # Query to get all the accounts of a user
    GET_EXISTING_ACCOUNTS_QUERY = f"""
    SELECT account_name FROM accounts 
    WHERE user_id = "{user_id}";
    """

    cursor.execute(GET_EXISTING_ACCOUNTS_QUERY)
    accounts = cursor.fetchall()

    return accounts 


def get_account_infos(user_id, account_name):
    connection, cursor = connect()

    # Query to get all the infos of an account of a user
    GET_ACCOUNT_INFOS_QUERY = f"""
    SELECT username, email, password FROM accounts
    WHERE user_id = "{user_id}" AND account_name = "{account_name}";
    """

    cursor.execute(GET_ACCOUNT_INFOS_QUERY)
    infos = cursor.fetchall()

    username = infos[0][0]
    email = infos[0][1]
    pwd = infos[0][2][2::]

    return username, email, pwd
