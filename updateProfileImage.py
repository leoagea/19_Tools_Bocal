from config import *
from utils import fetch_user_id

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

if __name__ == "__main__":
	update_user_image()