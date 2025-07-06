# Use these Steps to run and make it work in your own system.


1. First create a folder for the project and open terminal for that folder in VS Code.
2. Clone the repo and open it with "git clone <your-webhook-repo-url>" & "cd webhook-repo".
3. Create the Virtual Environment with "python -m venv venv".
4. Activate the Virtual Environment by using "venv\Scripts\activate".
5. Now, Install Dependencies with the help of "pip install flask pymongo".
6. Run the flask app with "python app.py".
7. Expose localhost with Ngrok, download and set it up, then start it by "ngrok http 5000".
8. Copy the HTTPS forwarding URL for webhook setup.
9. Now, Set Up GitHub Webhook, go to your action-repo on GitHub.
10. Navigate to Settings > Webhooks > Add webhook.Set the Payload URL to:https://<your-ngrok-url>/webhook.
11. Content type: application/json. Select events: Push, Pull Request, (optionally Merge) and save.
12. To test it, push a commit: Edit a file and push to action-repo.
13. To test if for pull, Open a pull request: Create a new branch, make a change, and open a PR.
14. Merge a pull request: Merge the PR into the main branch.
15. Check the UI at http://localhost:5000/ui to see events appear and auto-refresh.
