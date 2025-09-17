import os
import requests
from dotenv import load_dotenv
from auth import authenticate, get_auth_headers

load_dotenv()

id = 0

if __name__ == "__main__":
	api_url = os.getenv("42_API_URL")

	authenticate()

	url = f"{api_url}/users/gimli"
	response = requests.get(url, headers=get_auth_headers())
	if response.status_code == 200:
		id = response.json().get("id")
	else:
		print(f"Failed to retrieve user info. Status code: {response.status_code}")
		print(f"Response: {response.text}")

	print(f"User ID: {id}")

	url = f"{api_url}/users/{id}"
	response = requests.get(url, headers=get_auth_headers())
	if response.status_code == 200:
		user_data = response.json()
		print(f"User Data: {user_data['image']['link']}")

	else:
		print(f"Failed to retrieve user data. Status code: {response.status_code}")
		print(f"Response: {response.text}")

	response = requests.patch(url, headers=get_auth_headers(), params={ 'user[image]': "/Users/gimli/Downloads/Gimli.The-Lord-of-the-Rings-The-Fellowship-of-the-Ring.png"})
	if response.status_code == 200:
		print("User updated successfully.")
	else:
		print(f"Failed to update user. Status code: {response.status_code}")
		print(f"Response: {response.text}")

