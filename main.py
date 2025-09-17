from auth import authenticate
from userApi import display_user_image, update_user_image

if __name__ == "__main__":
	authenticate()

	while True:
		print("\nChoose an action:")
		print("1. Show user image")
		print("2. Update user image")
		print("3. Exit")
		choice = input("Enter your choice: ")
		if choice == "1":
			display_user_image()
		elif choice == "2":
			update_user_image()
		elif choice == "3":
			break
		else:
			print("Invalid choice. Please try again.")