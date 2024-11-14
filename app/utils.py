import os
import requests
from django.conf import settings
from .models import Project
from dotenv import load_dotenv

load_dotenv()

def export_all_projects_to_gist_and_local(pk):
    github_token = os.getenv('GITHUB_ACCESS_TOKEN')
    if not github_token:
        raise ValueError("GitHub access token not found in environment variables")

    # Loop through all Project instances
    for project in Project.objects.filter(pk=pk):
        # Filter tasks based on their status
        completed_tasks = project.tasks.filter(status='Completed')
        pending_tasks = project.tasks.filter(status='Pending')

        # Generate gist content
        gist_content = f"# {project.title}\n\n"
        gist_content += f"**Summary:** {completed_tasks.count()}/{project.tasks.count()} completed\n\n"
        gist_content += "## Pending\n"
        for task in pending_tasks:
            gist_content += f"- [ ] {task.description}\n"
        gist_content += "\n## Completed\n"
        for task in completed_tasks:
            gist_content += f"- [x] {task.description}\n"

        # Upload the gist to GitHub
        response = requests.post(
            'https://api.github.com/gists',
            headers={'Authorization': f'token {github_token}'},
            json={
                "files": {f"{project.title}.md": {"content": gist_content}},
                "description": f"Summary of project {project.title}",
                "public": False  # Set to False for a secret gist
            }
        )
        
        # Check if the request was successful
        if response.status_code == 201:
            gist_url = response.json().get("html_url", "")
            print(f"Gist created for {project.title}: {gist_url}")
        else:
            print(f"Failed to create gist for {project.title}: {response.json()}")

        # Save the gist content locally
        local_filename = f"summary/{project.title}.md"
        with open(local_filename, 'w') as file:
            file.write(gist_content)
            
    return response



