from langchain.tools import BaseTool
import requests
from typing import Optional, Type, List
from pydantic import BaseModel, Field


class GitHubIssueSearchToolInput(BaseModel):
    language: str = Field(description = "The language to filter issue")
    labels: List[str] = Field(default_factory = list, description = "List of Labels to filter issues")
    

class GitHubIssueSearchTool(BaseTool):
    name: str = "GitHub Issue Search Tool"
    description: str = "Search GitHub issues based on labels and repository domain."
    args_schema: Type[BaseModel] = GitHubIssueSearchToolInput
    github_token: Optional[str] = Field(default = None, description = "GitHub API token")
    headers: dict = Field(default_factory=dict, description="Request headers")

    def __init__(self, github_token):
        super().__init__()
        self.github_token = github_token
        self.headers = {
            "Authorization": f"Bearer {github_token}" if github_token else None,
            "Accept": "application/vnd.github.v3+json"
        }

    def _run(self, language: str, labels: List[str]) -> str:

        url = "https://api.github.com/search/issues"

        query_parts = ["is:issue", "is:open"]

        if language:
            query_parts.append(f'language:"{language}"')
        if labels:
            label_query = " ".join(f'label:"{label}"' for label in labels)
            query_parts.append(label_query)

        query = " ".join(query_parts)
        print(query)
        params = {"q": query, "sort": "created", "order": "desc"}

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        data = response.json()
        if not data.get("items"):
            return "No issues found matching the specified criteria. Check the language and labels."
            
        results = []
        for issue in data["items"]:
            results.append({
                "number": issue["number"],
                "title": issue["title"],
                "labels": [label["name"] for label in issue["labels"]],
                "url": issue["html_url"],
                "summary": issue['body'],
            })
            
        return results
