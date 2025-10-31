from config import *
from utils import fetch_user_id

def get_available_badges():
	return {
		"STAFF": 1,
		"PHOENIX": 47,
		"BDE": 73,
		"PEGASUS": 369,
		"VIBRANIUM": 379
	}

def get_user_groups(user_id):
	groups_url = f"{api_url}/users/{user_id}/groups_users"
	response = requests.get(groups_url, headers=get_auth_headers())
	if response.status_code != 200:
		print(f"Failed to retrieve user groups. Status code: {response.status_code}")
		return None
	return response.json()

def validate_badge_ids(badge_ids_list, available_badges):
	for badge_id in badge_ids_list:
		if badge_id not in available_badges.values():
			print(f"Invalid badge ID: {badge_id}. Valid IDs are: {', '.join(map(str, available_badges.values()))}")
			return False
	return True

def add_badge_to_user(user_id, badge_id, available_badges):
	url = f"{api_url}/groups_users"
	data = {
		"groups_user[user_id]": user_id,
		"groups_user[group_id]": badge_id
	}
	response = requests.post(url, headers=get_auth_headers(), data=data)
	
	if response.status_code in [200, 201]:
		badge_name = [name for name, id in available_badges.items() if id == badge_id][0]
		print(f"Successfully added badge: {badge_name} (ID: {badge_id})")
		return True
	else:
		print(f"Failed to add badge {badge_id}. Status code: {response.status_code}")
		print(f"Response: {response.text}")
		return False

def remove_badge_from_user(relationship_id, badge_id, available_badges):
	url = f"{api_url}/groups_users/{relationship_id}"
	response = requests.delete(url, headers=get_auth_headers())
	
	if response.status_code in [200, 204]:
		badge_name = [name for name, id in available_badges.items() if id == badge_id][0] if badge_id in available_badges.values() else f"Unknown (ID: {badge_id})"
		print(f"Successfully removed badge: {badge_name} (ID: {badge_id})")
		return True
	else:
		print(f"Failed to remove badge {badge_id}. Status code: {response.status_code}")
		print(f"Response: {response.text}")
		return False

def handle_add_badges(user_id, existing_badge_ids, available_badges):
	badge_ids = input("Enter badge IDs to add (comma-separated): ")
	badge_ids_list = [int(badge_id.strip()) for badge_id in badge_ids.split(",")]

	if not validate_badge_ids(badge_ids_list, available_badges):
		return

	for badge_id in badge_ids_list:
		if badge_id not in existing_badge_ids:
			add_badge_to_user(user_id, badge_id, available_badges)
		else:
			badge_name = [name for name, id in available_badges.items() if id == badge_id][0]
			print(f"Badge {badge_name} (ID: {badge_id}) already exists for this user")

def handle_remove_badges(existing_groups, available_badges):
	if not existing_groups:
		print("User has no badges to remove.")
		return
	
	print("Current badges:")
	for group_info in existing_groups:
		group = group_info['group']
		print(f"- {group['name']} (ID: {group['id']}) [Relationship ID: {group_info['id']}]")
	
	badge_ids = input("Enter badge IDs to remove (comma-separated): ")
	badge_ids_list = [int(badge_id.strip()) for badge_id in badge_ids.split(",")]
	
	for badge_id in badge_ids_list:
		relationship_id = None
		for group_info in existing_groups:
			if group_info['group']['id'] == badge_id:
				relationship_id = group_info['id']
				break
		
		if relationship_id:
			remove_badge_from_user(relationship_id, badge_id, available_badges)
		else:
			print(f"Badge ID {badge_id} not found in user's current badges")

def update_user_badges() -> None:
	user_id = fetch_user_id()
	if not user_id:
		return
	
	existing_groups = get_user_groups(user_id)
	if existing_groups is None:
		return
	
	existing_badge_ids = [group_info['group']['id'] for group_info in existing_groups]
	available_badges = get_available_badges()

	print(f"Available badges: {available_badges}")
	print(f"Current user badges: {existing_badge_ids}")
	
	action = input("Do you want to (a)dd or (r)emove badges? Enter 'a' or 'r': ").lower()
	
	if action == 'a':
		handle_add_badges(user_id, existing_badge_ids, available_badges)
	elif action == 'r':
		handle_remove_badges(existing_groups, available_badges)
	else:
		print("Invalid choice. Please enter 'a' for add or 'r' for remove.")

if __name__ == "__main__":
	update_user_badges()