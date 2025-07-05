from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import datetime

# --- MongoDB Connection ---
client = MongoClient('mongodb://localhost:27017/')  # Change if needed
db = client['webhook_db']
events = db['events']

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Home Route with Navigation Link ---
@app.route('/')
def home():
    return '<h2>Webhook Listener Running!</h2><a href="/ui">Go to Events UI</a>'

# --- Webhook Endpoint ---
@app.route('/webhook', methods=['POST'])
def github_webhook():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.json

    # Handle Push Event
    if event_type == 'push' and payload.get('head_commit'):
        event = {
            "request_id": payload['head_commit']['id'],
            "author": payload['pusher']['name'],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload['ref'].split('/')[-1],
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        events.insert_one(event)

    # Handle Pull Request Event
    elif event_type == 'pull_request' and payload.get('pull_request'):
        pr = payload['pull_request']
        event = {
            "request_id": str(pr['id']),
            "author": pr['user']['login'],
            "action": "PULL_REQUEST",
            "from_branch": pr['head']['ref'],
            "to_branch": pr['base']['ref'],
            "timestamp": pr['created_at']
        }
        events.insert_one(event)

        # Handle Merge Event (Optional, for extra credit)
        if pr.get('merged', False):
            merge_event = {
                "request_id": str(pr['id']),
                "author": pr['merged_by']['login'] if pr.get('merged_by') else pr['user']['login'],
                "action": "MERGE",
                "from_branch": pr['head']['ref'],
                "to_branch": pr['base']['ref'],
                "timestamp": pr['merged_at']
            }
            events.insert_one(merge_event)

    return jsonify({'status': 'received'}), 200

# --- Events API for UI ---
@app.route('/events')
def get_events():
    all_events = list(events.find().sort('timestamp', -1))
    for event in all_events:
        event['_id'] = str(event['_id'])
    return jsonify(all_events)

# --- UI Route ---
@app.route('/ui')
def ui():
    return render_template('index.html')

# --- Main Entry Point ---
if __name__ == '__main__':
    app.run(port=5000)
