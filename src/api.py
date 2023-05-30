import httpx
import os
from dotenv import load_dotenv
import subprocess

def get_workflow_job_id(pull_request_number):
    load_dotenv()
    base_url = "https://api.github.com"
    repo_owner = "rust-lang"
    repo_name = "rust"
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")  # Replace with your GitHub access token

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {access_token}",
    }

    # Get pull request details
    pr_url = f"{base_url}/repos/{repo_owner}/{repo_name}/pulls/{pull_request_number}"
    response = httpx.get(pr_url, headers=headers)
    pr_data = response.json()

    # Get the workflow runs for the pull request
    workflows_url = f"{base_url}/repos/{repo_owner}/{repo_name}/actions/runs"
    params = {
        "event": "pull_request",
        "branch": pr_data["head"]["ref"],
        "per_page": 1,
    }
    response = httpx.get(workflows_url, headers=headers, params=params)
    workflows_data = response.json()

    if not workflows_data["workflow_runs"]:
        return "No workflow runs found for the pull request."

    # Get the JOB_ID of the latest workflow run
    latest_workflow_run = workflows_data["workflow_runs"][0]
    job_id = latest_workflow_run["id"]

    job_logs_url = workflows_url + f"/{job_id}/logs"

    print("info: Downloading CI build logs and unzipping them.")
    command = f"curl -L -H 'Authorization: Bearer {access_token}' {job_logs_url} > .cistern-job-{job_id}.zip"
    subprocess.run(command, shell=True)
    subprocess.run(["unzip", f".cistern-job-{job_id}.zip", "-d", f".cistern-job-{job_id}"])
    print("---------------------------------------------------------------------------------------------")
    print("Finished downloading and unizzping.")
    print("---------------------------------------------------------------------------------------------")
    subprocess.run(["rm", "-rf", f".cistern-job-{job_id}.zip"])