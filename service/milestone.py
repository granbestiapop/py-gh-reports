import hashlib
from addict import Dict
import re

milestone_regex = re.compile(r"https://github.com/(.*)/(.*)/milestone/(\d*)")


def process_template_data(data, title):
    return {
        'milestones': [transform_repository(Dict(data['data'][key])) for key in data['data']],
        'title': get_title_or_default(title)
    }


def get_title_or_default(title):
    if not title:
        return "Subida programada"
    return title


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


def extract_url_info(url):
    m = milestone_regex.match(url)
    if m is None:
        return None

    org = m.group(1)
    application = m.group(2)
    milestone_id = m.group(3)
    q_id = hashlib.md5(
        f"{application}{milestone_id}".encode('utf')).hexdigest()
    return {'org': org, 'application': application, 'milestone_id': milestone_id, 'q_id': "m_"+q_id}


def milestone_info(urls):
    urls = re.split(',|\n', urls)
    urls = list(filter(None, urls))
    formatted_urls = list(filter(None, [extract_url_info(u) for u in urls]))
    return formatted_urls
