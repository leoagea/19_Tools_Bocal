from config import *
from datetime import datetime, timedelta

def clean_up_dup(users: list[dict]) -> list[dict]:
	clean_users = {}
	seen_ids = set()
	for user in users:
		user_id = user['user']['id']
		if user_id not in seen_ids:
			seen_ids.add(user_id)
			clean_users[user_id] = {
				'id': user['user']['id'],
				'login': user['user']['login']
			}
	return list(clean_users.values())

def getNewStudentsByKickoffDate(date: datetime, file: bool = False) -> list[dict]:

	url = f"{api_url}/cursus/21/cursus_users?filter[campus_id]=12&range[begin_at]={date - timedelta(days=1)},{date + timedelta(days=1)}"
	all_users = []
	page = 0
	while True:
		params = {
			"page[size]": 100, 
			"page[number]": page
		}
		response = requests.get(url, headers=get_auth_headers(), params=params)
		if response.status_code != 200:
			print(f"Failed to fetch users. Status code: {response.status_code}")
			print(f"Response: {response.text}")
			return
		if not response or not response.json():
			break

		users = response.json()
		all_users.extend(users)
		page += 1

	clean_users = clean_up_dup(all_users)
	print(f"Found {len(clean_users)} new students starting around {date.date()}.")
	if file:
		with open("StudentList.txt", "w") as f:
			for user_info in clean_users:
				if user_info['login'] in ["gimli", "jade-", "freya", "alphonse"]:
					continue
				f.write(f"ID: {user_info['id']}, Login: {user_info['login']}\n")
	return clean_users

if __name__ == "__main__":
	date_str = input("Enter the date of the piscine start (YYYY-MM-DD): ")
	output = input("Output to file? (y/n): ").lower() == 'y'
	try:
		date = datetime.strptime(date_str, "%Y-%m-%d")
	except ValueError:
		print("Invalid date format. Please use YYYY-MM-DD.")
		exit(1)
	getNewStudentsByKickoffDate(date, output)

