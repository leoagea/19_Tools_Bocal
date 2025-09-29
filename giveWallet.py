import requests
from auth import get_auth_headers
from userApi import fetch_user_id
from config import api_url

def giveWallet():
	user_id = fetch_user_id()
	if not user_id:
		return

	reason = input("Enter reason for transaction: ")
	value = input("Enter value of transaction: ")

	data = {
		"transaction": {
			"value": f"{value}",
			"user_id": f"{user_id}",
			"transactable_type": "Bocal",
			"reason": f"{reason}"
		}
	}
	url = f"{api_url}/transactions"
	request = requests.post(url, json=data, headers=get_auth_headers())
	if request.status_code == 201:
		print("Transaction added successfully.")
	else:
		print(f"Failed to add transaction. Status code: {request.status_code}")
		print(f"Response: {request.text}")

if __name__ == "__main__":
	giveWallet()