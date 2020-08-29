import requests
import json
import os
import sys
from jinja2 import Template
from utils.config import get_github_client, get_github_client_secret

sys.path.append("..")
client_id = get_github_client()
client_secret = get_github_client_secret()

query_template = Template(
    ''' 
      query {
        {% for m in milestones %}
        {{m.q_id}}: repository(owner:"{{m.org}}" name:"{{m.application}}"){
          name
          milestone(number:{{m.milestone_id}}){
            id
            title
            description
            createdAt
            dueOn
            state
            url
            pullRequests(last:50) {
              nodes {
                id
                state
                author{
                  login
                  avatarUrl
                  url
                }
                title
                permalink     		
              }
              totalCount
            }
          }
        }
        {% endfor %}
      }
    '''
)


def get_data_from_github(token, milestones):
    url = "https://api.github.com/graphql"
    headers = {
        'Authorization': f"bearer {token}"
    }
    payload = {
        'query': create_query(milestones)
    }
    resp = requests.post(url=url, data=json.dumps(payload), headers=headers)
    data = resp.json()
    return data


def get_user_token(code):
    url = "https://github.com/login/oauth/access_token"
    payload = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    resp = requests.post(url=url, data=json.dumps(payload), headers=headers)
    data = resp.json()
    return data


def create_query(milestones):
    return query_template.render(milestones=milestones)
