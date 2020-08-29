from flask import Flask, render_template, request, make_response, redirect

import service.milestone as milestone_service
import service.github as github_service


def create_app():
    app = Flask(__name__)

    @app.route('/reports')
    def reports():
        uid = request.cookies.get('uid')
        token = request.args.get('token')
        if not token:
            token = uid
        milestones = request.args.get('milestones')
        title = request.args.get('title')
        # Parse milestone query param
        milestones = milestone_service.milestone_info(milestones)
        data = github_service.get_milestones(
            token=token, milestones=milestones)
        # Prepare data for template engine
        template_data = milestone_service.process_template_data(data, title)
        return render_template('index.html', milestones=template_data['milestones'], title=template_data['title'])

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
        token = github_service.get_user_token(code)
        # Redirect and set cookie
        resp = make_response(redirect('/home'))
        resp.set_cookie('uid', token)
        return resp

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
