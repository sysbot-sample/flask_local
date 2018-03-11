from flask import Flask
import requests
from flask import request,json

app = Flask(__name__)

url = 'https://hooks.slack.com/services/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'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/web_hook', methods=['POST'])
def hook_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        sender = data['comment']['user']['login']
        comment = data['comment']['body']
        data = {"text": "@" + sender + " commented " + comment + " on an issue"}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print r
        return json.dumps(request.json)


if __name__ == '__main__':
    app.run()


def slack_request(sender, comment):
    data = {"text": "@" + sender + "commented " + comment + " on an issue"}
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print r