import json
import secrets
import string

def loadPasswords():
    with open("passwords.json", "r") as file:
        passwords = json.load(file)
    return passwords
def savePasswords(passwords):
    with open("passwords.json", "w") as file:
        json.dump(passwords, file, indent=4)

#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


def loadMasterPassword():
    with open("master.json", "r") as file:
        masterPassword = json.load(file)
    return masterPassword
def saveMasterPassword(masterPassword):
    with open("master.json", "w") as file:
        json.dump(masterPassword, file)

#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#show all website's username/password pairs saved to the program
def viewPasswords(passwords):
    print("Here is a list of all your passwords: ")
    for website in passwords:
        for username, password in passwords[website].items():
            print(f"Website: {website} | Username: {username} | Password: {password}")

#add new username/password pair to a website, prevents duplicate usernames
def addPassword(passwords, website, username, password):
    if website not in passwords:
        passwords[website] = {}
    if username in passwords[website]:
        print(f"An account with this username: {username} already exists. Please enter a different username, or select 3 to update your password.")
    else:
        passwords[website][username] = password
        print("Password added successfully.")

#updates an existing account's password, and optionally generates a secure password.
def updatePassword(passwords, website):
    username = input("Enter your username: ")
    if username in passwords[website]:
        option = input("Would you like a randomly generated password? (y/n): ").lower()
        if option in ["y", "yes", "yep", "yeah"]:
            password = passwordGenerator()
            print("Your randomly generated password is: ", password)
        else:
            password = input("Enter your password: ")
        passwords[website][username] = password

        print("Password updated successfully.")
    else:
        print("Account not found. Please enter a correct username.")

#shows all usernames and passwords for a given website.
def searchPassword(passwords, website):
    if website in passwords:
        print(f"Showing accounts for this website: {website}")
        print("=========================================")
        for key, value in passwords[website].items():
            print(f"Username: {key} | Password: {value}")
    else:
        print("No accounts found for this website.")

#deletes password by website and username
def deletePassword(passwords, website):
    username = input("Enter the username of the account you wish to remove: ")
    if username in passwords[website]:
        del passwords[website][username]
        if len(passwords[website]) == 0:            #remove website from program file if last account is deleted
            del passwords[website]
        print("Account removed successfully.")
    else:
        print("Account not found. Please enter a correct username.")

#shows all websites that use the same username
def allAccounts(passwords, username):
    found = False
    for website in passwords:
        for user, password in passwords[website].items():
            if user == username:
                found = True
                print(f"Website: {website} | Username: {username} | Password: {password}")
    if not found:
        print("No accounts found with this username.")

#generates random password using secrets
def passwordGenerator():
    password = ""
    characters = string.ascii_letters + string.digits + string.punctuation
    for _ in range(12):
        password += secrets.choice(characters)
    return password

#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


def menu():
    print()
    print("=========================================")
    print("           Password Manager")
    print("=========================================")
    print("1) View Passwords")
    print("2) Add Password")
    print("3) Update Password")
    print("4) Search Password")
    print("5) Delete Password")
    print("6) Show Websites With the Same Username")
    print("7) Change Program Password")
    print("8) Quit")
    print("==========================================")
    print()
    selection = input("Select an option: ")
    while selection not in ["1", "2", "3", "4", "5", "6", "7", "8"]:    #ensures a valid menu option is selected
        print("Please enter a valid option.")
        selection = input("Select an option: ")
    return selection

#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

def main(masterPassword):
    passwords = loadPasswords()
    programPassword = input("Enter your password: ")

    #can't access program unless the correct master password is entered
    while programPassword != masterPassword:
        print("The password you have entered is incorrect. Please enter a different password.")
        programPassword = input("Enter your password: ")
    print("Password is correct. Welcome to Password Manager!")
    print()

    selection = menu()
    #run until user decides to exit
    while selection != "8" :
        if selection == "1":
            if passwords:
                viewPasswords(passwords)
            else:
                print("No passwords currently saved.")

        elif selection == "2":          #add a new password
            website = input("Enter the website you wish to access: ")
            username = input("Enter your username: ")
            if website in passwords and username in passwords[website]:
                print("The username entered for this website already has a password. Enter 3 to update your password")
            else:
                option = input("Would you like a randomly generated password? (y/n): ").lower()
                if option in ["y", "yes", "yep", "yeah"]:
                    password = passwordGenerator()
                    print("Your randomly generated password is: ", password)
                else:
                    password = input("Enter your password: ")
                addPassword(passwords, website, username, password)
                savePasswords(passwords)


        elif selection == "3":
            website = input("Enter the website you wish to access: ")
            if website in passwords:
                updatePassword(passwords, website)
                savePasswords(passwords)
            else:
                print("No accounts found for this website.")


        elif selection == "4":
            website = input("Enter the website you wish to access: ")
            if website in passwords:
                searchPassword(passwords, website)
            else:
                print("No accounts found for this website.")


        elif selection == "5":
            website = input("Enter the website you wish to access: ")
            if website in passwords.keys():
                deletePassword(passwords, website)
                savePasswords(passwords)
            else:
                print("No accounts found for this website.")


        elif selection == "6":
            username = input("Enter your username: ")
            allAccounts(passwords, username)


        elif selection == "7":
            newPassword = input("Enter your new password: ")
            master = loadMasterPassword()
            master["masterPassword"] = newPassword
            saveMasterPassword(master)
            masterPassword = newPassword
            print("Password has been updated successfully.")
            print(f"Your new password is: {masterPassword}")


        selection = menu()
    print("Thank you for using Password Manager!")

master = loadMasterPassword()
if "masterPassword" not in master:          #create master password for the first time
    masterPassword = input("Create your master password: ")
    master["masterPassword"] = masterPassword
    saveMasterPassword(master)
main(master["masterPassword"])