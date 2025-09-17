import os
import requests

auth_token = ""

def authenticate() -> str:
	global auth_token
	id = os.getenv("42_CLIENT_ID")
	secret = os.getenv("42_CLIENT_SECRET")

	url = f"https://api.intra.42.fr/oauth/token"
	response = requests.post(
		url,
		data={
			"grant_type": "client_credentials",
			"client_id": id,
			"client_secret": secret
		}
	)

	if response.status_code == 200:
		auth_token = response.json().get("access_token", "")

def get_auth_headers() -> dict:
	return {
		"Authorization": f"Bearer {auth_token}"
	}