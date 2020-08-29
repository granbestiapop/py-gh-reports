from client.github import get_data_from_github, get_user_token


def get_milestones(token, milestones):
    return get_data_from_github(token=token, milestones=milestones)


def get_user_token(code):
    data = get_user_token(code)
    return data['access_token']
