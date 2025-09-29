from auth import authenticate
from userApi import *
if __name__ == "__main__":
	authenticate()

	functions = {
		"2": display_user_data,
		"3": display_user_groups,
		"5": update_user_badges
	}

	while True:
		print("\nChoose an action:")
		print("1. Get user login")
		print("2. Show user data")
		print("3. Show user groups")
		print("4. Update user image")
		print("5. Update user badges")
		print("6. Exit")
		choice = input("Enter your choice: ")
		if choice == "6":
			break
		elif choice in functions:
			functions[choice]()
		else:
			print("Invalid choice. Please try again.")