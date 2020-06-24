import requests
import json
import chevron
import os

client_id = os.environ['GITHUB_CLIENT']
client_secret = os.environ['GITHUB_CLIENT_SECRET']

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
  resp = requests.post(url=url, data=json.dumps(payload), headers = headers)
  data = resp.json()
  return data


def create_query(milestones):
  query = chevron.render(''' 
      query {
        {{#milestones}}
        {{q_id}}: repository(owner:"{{org}}" name:"{{application}}"){
          name
          milestone(number:{{milestone_id}}){
            id
            title
            description
            createdAt
            dueOn
            state
            url
            pullRequests(last:20) {
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
        {{/milestones}}
      }
    ''', {'milestones':milestones})
  return query