from config import *
from getNewStudentsByKickoffDate import getNewStudentsByKickoffDate
from datetime import datetime, timedelta

def postPoneCursusUser(user_id: int, begin_at: datetime) -> None:
	url = f"{api_url}/cursus_users/{user_id}"
	params = {
		"cursus_user": {
			"begin_at": f'{begin_at}'
		}
	}
	response = requests.put(url, json=params, headers=get_auth_headers())
	if response.status_code in [200, 201, 203, 204]:
		print(f"Cursus user {user_id} updated successfully.")
	else:
		print(f"Failed to update cursus user {user_id}. Status code: {response.status_code}")
		print(f"Response: {response.text}")

def givePiscineReloaded(user_id: int, begin_at: datetime, end_at: datetime) -> None:
	url = f'{api_url}/cursus_users'
	params = {
		"cursus_user": {
			"begin_at": f'{begin_at}',
			"cursus_id": "66",
			"end_at": f'{end_at}',
			"user_id": f'{user_id}'
		}
	}
	response = requests.post(url, json=params, headers=get_auth_headers())
	if response.status_code in [200, 201, 203, 204]:
		print(f"Cursus user for user {user_id} added successfully.")
	else:
		print(f"Failed to add cursus user for user {user_id}. Status code: {response.status_code}")
		print(f"Response: {response.text}")

def kick_off_new_students(date: datetime) -> None:
	new_students = getNewStudentsByKickoffDate(date)
	for student in new_students:
		if student['login'] in ["gimli", "jade-", "freya", "alphonse"]:
			continue
		url = f'{api_url}/users/{student['login']}/cursus_users?filter[cursus_id]=21'
		response = requests.get(url, headers=get_auth_headers())
		if response.status_code != 200:
			print(f"Failed to fetch cursus users. Status code: {response.status_code}")
			print(f"Response: {response.text}")
			return
		res = response.json()
		postPoneCursusUser(res[0]['id'], date + timedelta(days=7))
		givePiscineReloaded(student['id'], date), date + timedelta(days=7)
	pass

if __name__ == "__main__":
	date_str = input("Enter the date of the piscine start (YYYY-MM-DD): ")
	try:
		date = datetime.strptime(date_str, "%Y-%m-%d")
	except ValueError:
		print("Invalid date format. Please use YYYY-MM-DD.")
		exit(1)
	kick_off_new_students(date)
