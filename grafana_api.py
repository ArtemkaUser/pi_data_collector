import requests
import json

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJrIjoiM09kR0RFWjNZSzUxWXRZNDR0SEdKN2Y1RERHOFVZbU0iLCJuIjoic2hhZHIxayIsImlkIjoxfQ=='
}
def get_json(uid):
    resp = requests.get('http://localhost:3000/api/dashboards/uid/' + uid, headers=headers)
    return json.loads(resp.text)

def push_json(uid, json):
    resp = requests.post('http://localhost:3000/api/dashboards/db', json=json, headers=headers)

def get_name_panel(json):
    return json.get('dashboard').get('panels')[0].get('title')

def change_name(json, name):
    json.get('dashboard').get('panels')[0].update({'title': name})
    requests.post('http://localhost:3000/api/dashboards/db', json=json, headers=headers)

# print(d)
# change time panel
# print(d.get('dashboard'))
# post changes
#
# print(resp)
# print(resp.text)
if __name__ == '__main__':
    json = get_json('rzlhlzrik')
    print(json.get('dashboard').get('panels')[0].get('targets')[0].get('tags'))