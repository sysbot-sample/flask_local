from flask import Flask
import requests
from flask import request, json
from auth_urls import *
from tokens import *
from slackclient import SlackClient

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/challenge', methods=['POST'])
def challenge():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        print data
        try:
            challenge_key = data['challenge']
            return challenge_key
        except KeyError:
            try:
                event = data['event']['type']
                if event == 'member_joined_channel':
                    uid = data['event']['user']
                    channel = data['event']['channel']
                    if channel == channel_join_id:
                        body = {'user': uid}
                        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(BOT_ACCESS_TOKEN)}
                        r = requests.post(dm_channel_open_url, data=json.dumps(body), headers=headers)
                        response = r.json()
                        if 'ok' in response and response['ok'] is True:
                            dm_channel_id = response['channel']['id']
                            body = {'username': 'Sysbot', 'as_user': True, 'text': "Hello from Sysbot", 'channel': dm_channel_id}
                            r = requests.post(dm_chat_post_message_url, data=json.dumps(body), headers=headers)
                            print "Response: %s" % json.dumps(r.json())
                    return json.dumps(request.json)
                else:
                    return json.dumps(request.json)
            except KeyError:
                data = {"text": "Sorry some error occurred"}
                headers = {'Content-type': 'application/json'}
                r = requests.post(url, data=json.dumps(data), headers=headers)
                return json.dumps(request.json)


@app.route('/web_hook', methods=['POST'])
def hook_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        try:
            action = data['action']
            if action == 'opened':
                issue_opened(data)
        except KeyError:
            pass
        return json.dumps(request.json)


if __name__ == '__main__':
    app.run()


def issue_opened(data):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    issue_number = data['issue']['number']
    repo_name = data['repository']['name']
    repo_owner = data['repository']['owner']['login']
    print "\n\nRepo Info: \n %s , %s, %s" % (repo_owner, repo_name, issue_number)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/x-www-form-urlencoded'}
    label = '["Not Approved"]'
    # label = {"name": "First Issue Opened", "description": "Freshly opened issue", "color": "f29513"}
    request_url = 'https://api.github.com/repos/%s/%s/issues/%s/labels' % (repo_owner, repo_name,issue_number)
    # request_url = 'https://api.github.com/repos/%s/%s/labels' % (repo_owner, repo_name)
    r = session.post(request_url, data=label, headers=headers)
    if r.status_code == 201:
        print 'Successfully created label'
    else:
        print 'Unsuccessful.Response:', r.content
    return
