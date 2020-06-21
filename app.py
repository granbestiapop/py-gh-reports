from flask import Flask, render_template, request
import requests
import json
import re
import hashlib
from addict import Dict
import chevron


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


def extract_url_info(url):
  p = re.compile(r"https://github.com/(.*)/(.*)/milestone/(.*)")
  m = p.match(url)
  org = m.group(1)
  application = m.group(2)
  milestone_id = m.group(3)
  q_id = hashlib.md5(application.encode('utf')).hexdigest()
  return {'org': org, 'application':application, 'milestone_id': milestone_id, 'q_id':q_id}

def milestone_info(urls):
  urls = urls.split(',')
  formatted_urls = [extract_url_info(u) for u in urls]
  return formatted_urls

def get_data_from_github(token, milestones):
  url = "https://api.github.com/graphql"
  headers = {
    'Authorization': 'bearer ' + token 
  }
  payload = {
    'query': create_query(milestones)
  }
  resp = requests.post(url=url, data=json.dumps(payload), headers=headers)
  data = resp.json()
  return data

def transform_repository(repository):
  milestone = repository.milestone
  pull_requests = [pr for pr in milestone.pullRequests.nodes]
  template_data = {
    'repository_name': repository.name,
    'title': milestone.title,
    'description': milestone.description,
    'url': milestone.url,
    'pull_requests': pull_requests,
  }
  return template_data

def process_data(data):
  return [transform_repository(Dict(data['data'][key])) for key in data['data']]



def create_app():
  app = Flask(__name__)

  @app.route('/reports')
  def reports():
    token = request.args.get('token')
    milestones = request.args.get('milestones')
    # Parse params
    params = milestone_info(milestones)
    # Get data from github
    data = get_data_from_github(token=token, milestones=params)
    # Format prepare data for template engine
    template_data = process_data(data)
    # Render data
    return render_template('index.html', milestones = template_data)

  @app.route('/health')
  def health():
    return 'alive!'
  
  return app

if __name__ == "__main__":
  app = create_app()
  app.run(host='0.0.0.0', debug=True)