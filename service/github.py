import client.github as github_client


def get_milestones(token, milestones):
    return github_client.get_data_from_github(token=token, milestones=milestones)


def get_user_token(code):
    data = github_client.get_user_token(code)
    return data['access_token']
