from config import *
from math import ceil

import random

from datetime import datetime, timedelta

timezone = datetime.now().astimezone().tzinfo



project_session_id = 9370

start = datetime(2026, 2, 9, 12, 45, tzinfo=timezone)

corr_count = 3

corr_len = timedelta(minutes=45)

correctors = ['juhanse']


correctors = [requests.get(f'{api_url}/users/{u}', headers=get_auth_headers()).json()['id'] for u in correctors]

response = requests.get(f"{api_url}/project_sessions/{project_session_id}/teams", params={'filter[status]': 'waiting_for_correction'}, headers=get_auth_headers())
teams = response.json()

print(len(teams))

team_ids = [str(t['id']) for t in teams]

response = requests.get(f"{api_url}/project_sessions/{project_session_id}/scale_teams", params={'team_id': ','.join(team_ids)}, headers=get_auth_headers())
corrs = response.json()

print(corrs)

print(len(corrs))

matched = [c['team']['id'] for c in corrs]

print(matched)

response = requests.get(f"{api_url}/project_sessions/{project_session_id}", headers=get_auth_headers())
ps = response.json()

scale_id = next(s['id'] for s in ps['scales'] if s['is_primary'] == True)

print(scale_id)



correctors = [(c, (start + (corr_len * delta)).isoformat()) for c in correctors for delta in range(corr_count)]

print(correctors)

random.shuffle(correctors)



print(len(teams), '\n')



scale_teams = []



for team in teams:

	if not len(correctors):

		break

	if team['id'] in matched:

		continue

	corr = correctors.pop()

	scale_teams += [{'scale_id': scale_id, 'team_id': team['id'], 'user_id': corr[0], 'begin_at': corr[1]}]



print(scale_teams)

print(len(scale_teams))



print(requests.post(f"{api_url}/scale_teams/multiple_create", json={'scale_teams': scale_teams},headers=get_auth_headers()))



#for t in teams:

#    print(t['id'], [u['login'] for u in t['users']], correctors.pop())