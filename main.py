from auth import authenticate
from userApi import *
if __name__ == "__main__":
	authenticate()

	functions = {
		"1": display_user_data,
		"2": display_user_groups,
	}

	while True:
		print("\nChoose an action:")
		print("1. Show user data")
		print("2. Show user groups")
		print("3. Exit")
		choice = input("Enter your choice: ")
		if choice == "3":
			break
		elif choice in functions:
			functions[choice]()
		else:
			print("Invalid choice. Please try again.")