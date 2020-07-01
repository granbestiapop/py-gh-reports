from flask import Flask, render_template, request, make_response, redirect

from client.github import get_data_from_github, get_user_token
from service.milestone import process_data, milestone_info

def create_app():
  app = Flask(__name__)

  @app.route('/reports')
  def reports():
    uid = request.cookies.get('uid')
    token = request.args.get('token')
    if token == None:
      token = uid
    milestones = request.args.get('milestones')
    # Parse milestone query param
    params = milestone_info(milestones)
    data = get_data_from_github(token=token, milestones=params)
    # Prepare data for template engine
    template_data = process_data(data)
    return render_template('index.html', milestones = template_data)

  @app.route('/health')
  def health():
    return 'alive!'

  @app.route('/home')
  def home():
    authenticated = request.cookies.get('uid') is not None
    return render_template('home.html', data={}, authenticated=authenticated)

  @app.route('/reports/callback')
  def reports_callback():
    code = request.args.get('code')
    ## Get user data access token
    user_data = get_user_token(code)
    token = user_data['access_token']

    ## Send logged to home
    resp = make_response(redirect('/home'))
    resp.set_cookie('uid', token)
    return resp

  return app

if __name__ == "__main__":
  app = create_app()
  app.run(host='0.0.0.0', debug=True)