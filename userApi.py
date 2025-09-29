import requests

from config import *
from auth import get_auth_headers
from utils import fetch_user_id

def display_user_data() -> None:
	user_id = fetch_user_id()
	if not user_id:
		return

	url = f"{api_url}/users/{user_id}"
	response = requests.get(url, headers=get_auth_headers())

	if response.status_code == 200:
		data = input("Enter data to display (e.g., 'image') none if full: ")
		user_data = response.json()
		if data == "image":
			print(f"User Data: {user_data[data]}")
			return
		print(f"User Data: {user_data}")
	else:
		print(f"Failed to retrieve user data. Status code: {response.status_code}")
		print(f"Response: {response.text}")

def display_user_groups() -> None:
	user_id = fetch_user_id()
	if not user_id:
		return

	url = f"{api_url}/users/{user_id}/groups_users"
	response = requests.get(url, headers=get_auth_headers())
	
	print(response.json())
	if response.status_code == 200:
		groups_data = response.json()
		if groups_data:
			print("User Groups:")
			for group_info in groups_data:
				group = group_info['group']
				print(f"- {group['name']} (ID: {group['id']})")
		else:
			print("User has no groups.")
	else:
		print(f"Failed to retrieve user data. Status code: {response.status_code}")
