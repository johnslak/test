import requests
import json
import time

# Set up your GitHub access token and repository name
access_token = "YOUR_ACCESS_TOKEN"
repo_name = "OWNER/REPO_NAME"

def check_issues():
    # Get all open issues from the repository
    url = f"https://api.github.com/repos/{repo_name}/issues?state=open"
    headers = {"Authorization": f"Token {access_token}"}
    response = requests.get(url, headers=headers)
    issues = json.loads(response.text)
    
    for issue in issues:
        # Check each issue's timestamp and close it if it was opened less than 5 minutes ago
        if "created_at" in issue:
            created_at = issue["created_at"]
            current_time = time.time()
            created_time = time.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            created_time = time.mktime(created_time)
            if (current_time - created_time) < 300: # check if the issue was created less than 5 minutes ago
                issue_id = issue["number"]
                # Close the issue
                url = f"https://api.github.com/repos/{repo_name}/issues/{issue_id}"
                data = {"state": "closed"}
                response = requests.patch(url, json=data, headers=headers)
                print(f"Issue #{issue_id} closed.")
    print("Check completed.")

# Run the function every 5 minutes
while True:
    check_issues()
    time.sleep(300)
