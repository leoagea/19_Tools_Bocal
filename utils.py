from config import *

def fetch_user_id() -> int | None:
	username = input("Enter username: ")

	url = f"{api_url}/users/{username}"
	response = requests.get(url, headers=get_auth_headers())

	if response.status_code == 200:
		id = response.json().get("id")
		print(f"User ID: {id}")
		return id
	else:
		print(f"Failed to retrieve user info. Status code: {response.status_code}")
		print(f"Response: {response.text}")
		return None

def getLoginById() -> None:
	user_id = input("Enter user ID: ")
	page_number = 0

	url = f"{api_url}/campus/12/users"
	
	while True:
		params = {
			"page[size]": 100, 
			"page[number]": page_number
		}
		response = requests.get(url, headers=get_auth_headers(), params=params)
		page_number += 1
		if not response or not response.json():
			return
		if response.status_code == 200:
			user_data = response.json()
			for user in user_data:
				if user['id'] == int(user_id):
					print(f"Login: {user['login']}")
					return
		else:
			print(f"Failed to retrieve user data. Status code: {response.status_code}")
			print(f"Response: {response.text}")
			return

if __name__ == "__main__":
	# fetch_user_id()
	# getLoginById()
	pass