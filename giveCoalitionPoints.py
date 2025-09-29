import requests
from auth import get_auth_headers
from config import api_url

def postCoalitionPoints(coal_id: int, coal_user_id: int) -> None:
	reason = input("Enter reason for points: ")
	value = input("Enter value of points: ")
	data = {
		"score":{
			"reason": f"{reason}",
			"value": f"{value}",
			"coalitions_user_id": f"{coal_user_id}"
		}
	}
	url = f"{api_url}/coalitions/{coal_id}/scores"
	request = requests.post(url, json=data, headers=get_auth_headers())
	if request.status_code == 201:
		print("Points added successfully.")
	else:
		print(f"Failed to add points. Status code: {request.status_code}")
		print(f"Response: {request.text}")

def giveCoalitionPoints():
	user_status = input("Piscine or Student User? (p/s): ")
	login = input("Enter username: ")
	
	url = f"{api_url}/users/{login}/coalitions_users"
	response = requests.get(url, headers=get_auth_headers())
	if response.status_code == 200:
		data = response.json()
		for res in data:
			coalition_user_id = res['id']
			coal_id = res['coalition_id']
			if ((coal_id == 378 or coal_id == 380 or coal_id == 381) and user_status == "p") or ((coal_id == 52 or coal_id == 53 or coal_id == 54) and user_status == "s"):
				postCoalitionPoints(coal_id, coalition_user_id)
				return
		print(f"Coalition Data: {data}")
	else:
		print(f"Failed to retrieve coalition data. Status code: {response.status_code}")
		print(f"Response: {response.text}")
	
if __name__ == "__main__":
	giveCoalitionPoints()
