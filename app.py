from flask import Flask, render_template
import requests

app = Flask(__name__)

# Fill this tuple with strings of all the Stack Exchange user IDs you'd like to rank on your leaderboard.
# You can get the User ID from the URL of any profile.
# For example: https://stackoverflow.com/users/8826629/joel-guerra-msft the ID is 8826629

STACK_IDS=('8826629')

# You will need your own Stack Exchange API key
# Register for one here: https://stackapps.com/apps/oauth/register
# Replace 'INSERT_YOUR_KEY_HERE' with your key in the string below

def get_user(user_id):
    res = requests.get("http://api.stackexchange.com/2.2/users/" + user_id + "?order=desc&sort=reputation&site=stackoverflow&key=INSERT_YOUR_KEY_HERE"
    return res.json()['items'][0]


def rank_users(order_by):
    jsons = map(get_user, STACK_IDS)
    jsons = sorted(jsons, key=lambda k: k[order_by], reverse=True)
    return jsons

@app.route('/')
def index(users=None):
    jsons = rank_users("reputation")
    return render_template('index.html', users=jsons, title="Total Reputation")

@app.route('/week')
def total(users=None):
    jsons = rank_users("reputation_change_week")
    return render_template('index.html', users=jsons, title="Rep Change this Week") 

@app.route('/month')
def month(users=None):
    jsons = rank_users("reputation_change_month")
    return render_template('index.html', users=jsons, title="Rep Change this Month")

if __name__ == '__main__':
    app.run()