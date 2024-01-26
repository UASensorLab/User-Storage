import hashlib
import getpass
import json
import os
from shutil import copyfile

def get_user_input():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    return username, password

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def is_username_duplicate(username, user_data):
    for user_info in user_data:
        if user_info.get("username") == username:
            return True
    return False

def save_user_credentials(username, hashed_password):
    data = {
        "username": username,
        "hashed_password": hashed_password
    }
    with open('user_credentials.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

def authenticate_user(username, password, user_data):
    hashed_password = hash_password(password)

    for user_info in user_data:
        if user_info.get("username") == username and user_info.get("hashed_password") == hashed_password:
            return True
    return False

def display_user_folders(username):
    user_folders_path = '/Users/stefanbao/Desktop/UW'
    user_folders = [f for f in os.listdir(user_folders_path) if os.path.isdir(os.path.join(user_folders_path, f)) and f.startswith(username)]

    if user_folders:
        print("Available folders:")
        for i, folder in enumerate(user_folders, start=1):
            print(f"{i}. {folder}")
    else:
        print("No folders available.")

def create_user_folder(username, custom_folder_name):
    user_folder_name = f"{username}_{custom_folder_name}"
    user_folder_path = os.path.join('/Users/stefanbao/Desktop/UW', user_folder_name)

    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)

    return user_folder_path

def upload_user_data(destination_folder, username, file_extension, custom_file_name):
    while True:
        try:
            file_path = input(f"Upload {username}'s {file_extension.upper()} file: ")

            destination_path = os.path.join(destination_folder, f'{username}_{custom_file_name}.{file_extension}')
            copyfile(file_path, destination_path)

            print(f"{username}'s {file_extension.upper()} file has been successfully uploaded to {destination_folder} folder.")
            break
        except Exception as e:
            print(f"Failed to upload {file_extension.upper()} file: {e}")
            retry = input("Do you want to retry uploading the file? (yes/no): ").lower()
            if retry != 'yes':
                break

def upload_menu(username):
    print("Welcome to the upload menu!")

    # Display user's folders
    display_user_folders(username)

    choice = input("Enter the number of the folder you want to upload to (leave blank to create a new folder): ")
    if choice:
        selected_folder = f"{username}_{choice}"
        destination_folder = os.path.join('/Users/stefanbao/Desktop/UW', selected_folder)
    else:
        custom_folder_name = input("Enter a custom folder name: ")
        destination_folder = create_user_folder(username, custom_folder_name)

    file_types = get_file_types()
    display_file_types(file_types)
    selected_type_index = int(input("Select the file type number you want to upload: "))

    if 1 <= selected_type_index <= len(file_types):
        selected_file_type = file_types[selected_type_index - 1]
        custom_file_name = input("Enter a custom file name: ")
        upload_user_data(destination_folder, username, selected_file_type, custom_file_name)
    else:
        print("Invalid selection.")

def get_file_types():
    return ['jpeg', 'pdf', 'py', 'xls', 'xlsx', 'html', 'css', 'json']

def display_file_types(file_types):
    print("Supported file types:")
    for i, file_type in enumerate(file_types, start=1):
        print(f"{i}. {file_type.upper()}")
    print()

def register_user():
    print("Welcome to registration!")
    username, password = get_user_input()

    user_data = read_user_credentials()
    if is_username_duplicate(username, user_data):
        print("Registration failed, username already exists.")
        return

    hashed_password = hash_password(password)
    save_user_credentials(username, hashed_password)

    print("Registration successful!")

def read_user_credentials(file_path='user_credentials.json'):
    user_data = []
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            user_data.append(data)
    return user_data

def login():
    print("Welcome to login!")
    username, password = get_user_input()

    user_data = read_user_credentials()
    if authenticate_user(username, password, user_data):
        print("Login successful!")
        return username
    else:
        print("Login failed. Incorrect username or password.")
        return None

def main():
    if not os.path.isfile('user_credentials.json'):
        with open('user_credentials.json', 'w') as file:
            file.write('')  # Create an empty file

    while True:
        choice = input("Select:\n1. Register\n2. Login\n3. Exit\n")
        if choice == '1':
            register_user()
        elif choice == '2':
            username = login()
            if username:
                upload_menu(username)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid option, please choose again.")

if __name__ == "__main__":
    main()













