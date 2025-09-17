import requests

from auth import get_auth_headers
from config import api_url

def fetch_user_id() -> int | None:
	username = input("Enter username: ")

	url = f"{api_url}/users/{username}"
	response = requests.get(url, headers=get_auth_headers())

	if response.status_code == 200:
		return response.json().get("id")
	else:
		print(f"Failed to retrieve user info. Status code: {response.status_code}")
		print(f"Response: {response.text}")
		return None

def display_user_image() -> None:
	user_id = fetch_user_id()
	if not user_id:
		return

	url = f"{api_url}/users/{user_id}"
	response = requests.get(url, headers=get_auth_headers())

	if response.status_code == 200:
		user_data = response.json()
		print(f"User Data: {user_data['image']}")
	else:
		print(f"Failed to retrieve user data. Status code: {response.status_code}")
		print(f"Response: {response.text}")

def update_user_image() -> None:
	user_id = fetch_user_id()
	if not user_id:
		return
	
	image_path = input("Enter image file path: ")

	url = f"{api_url}/users/{user_id}"
	with open(image_path, "rb") as img_file:
		files = { 'user[image]': img_file }
		response = requests.patch(
			url,
			headers=get_auth_headers(),
			files=files
		)
	if response.status_code == 200:
		print("User updated successfully.")
	else:
		print(f"Failed to update user. Status code: {response.status_code}")
		print(f"Response: {response.text}")