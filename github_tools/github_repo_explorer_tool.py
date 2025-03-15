from langchain.tools import BaseTool
from typing import Optional, Type, Union, List
from pydantic import BaseModel, Field
import requests
from loguru import logger


class GitHubRepoExplorerToolInput(BaseModel):
    language: Optional[str] = Field(description = "The language to filter repositories")
    topics: Optional[List[str]] = Field(default_factory = list, description = "List of topics to filter repositories")
    labels: Optional[List[str]] = Field(default_factory = list, description = "List of Labels to filter repositories")

    sort_by: Optional[str] = Field("stars", description = "Sort results by: stars, forks, watchers, created, updated, pushed")
    limit: Optional[int] = Field(10, description = "Number of results to return")

    min_stars: Optional[int] = Field(None, description = "Minimum number of stars")
    max_stars: Optional[int] = Field(None, description = "Maximum number of stars")
    min_forks: Optional[int] = Field(None, description = "Minimum number of forks")
    max_forks: Optional[int] = Field(None, description = "Maximum number of forks")
    min_issues: Optional[int] = Field(None, description = "Minimum number of open issues")
    max_issues: Optional[int] = Field(None, description = "Maximum number of open issues")
    min_watchers: Optional[int] = Field(None, description = "Minimum number of watchers")
    max_watchers: Optional[int] = Field(None, description = "Maximum number of watchers")
    created_before: Optional[str] = Field(None, description = "Created before date")
    created_after: Optional[str] = Field(None, description = "Created after date")
    updated_before: Optional[str] = Field(None, description = "Updated before date")
    updated_after: Optional[str] = Field(None, description = "Updated after date")
    pushed_before: Optional[str] = Field(None, description = "Pushed before date")
    pushed_after: Optional[str] = Field(None, description = "Pushed after date")


class GitHubRepoExplorerTool(BaseTool):
    name: str = "github_repository_explorer_tool"
    description: str = "Search GitHub repositories based on certain filters."

    args_schema: Type[BaseModel] = GitHubRepoExplorerToolInput
    return_direct: bool = False
    
    github_token: Optional[str] = Field(default = None, description = "GitHub API token")
    headers: dict = Field(default_factory=dict, description="Request headers")
   
    def __init__(self, github_token):
        super().__init__()
        self.github_token = github_token
        self.headers = {
            "Authorization": f"Bearer {github_token}" if github_token else None,
            "Accept": "application/vnd.github.v3+json"
        }

    def _build_query(self, params: GitHubRepoExplorerToolInput) -> str:
        query_parts = []

        if params.language:
            query_parts.append(f'language:"{params.language}"')
        if params.topics:
            topic_query = " ".join(f'label:"{topic}"' for topic in params.topics)
            query_parts.append(topic_query)
        if params.labels:
            label_query = " ".join(f'label:"{label}"' for label in params.labels)
            query_parts.append(label_query)

        for param, value in {
            'stars': (params.min_stars, params.max_stars),
            'forks': (params.min_forks, params.max_forks),
            'open_issues': (params.min_issues, params.max_issues),
            'watchers': (params.min_watchers, params.max_watchers)
        }.items():
            min_val, max_val = value
            if min_val is not None:
                query_parts.append(f'{param}:>={min_val}')
            if max_val is not None:
                query_parts.append(f'{param}:<={max_val}')

        for param, value in {
            'created': (params.created_after, params.created_before),
            'updated': (params.updated_after, params.updated_before),
            'pushed': (params.pushed_after, params.pushed_before)
        }.items():
            after_val, before_val = value
            if after_val:
                query_parts.append(f'{param}:>={after_val}')
            if before_val:
                query_parts.append(f'{param}:<={before_val}')

        query = " ".join(query_parts)
        return query

    def _format_repository(self, repo: dict) -> dict:
        return {
            "name": repo.get("full_name"),
            "description": repo.get("description"),
            "url": repo.get("html_url"),
            "stars": repo.get("stargazers_count"),
            "forks": repo.get("forks_count"),
            "language": repo.get("language"),
            "topics": repo.get("topics", []),
            "last_updated": repo.get("updated_at"),
            "open_issues": repo.get("open_issues_count")
        }  

    def _run(
        self,
        language: Optional[str] = None,
        topics: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        sort_by: Optional[str] = "stars",
        limit: Optional[int] = 10,
        **kwargs
    ) -> Union[List[dict], str]:
        
        params = GitHubRepoExplorerToolInput(
            language=language,
            topics=topics,
            labels=labels,
            sort_by=sort_by,
            limit=limit,
            **kwargs
        )
        search_query = self._build_query(params)
        logger.info(f"Searching repositories with query: {search_query}")
        
        base_url = "https://api.github.com/search/repositories"

        try:
            response = requests.get(
                base_url,
                headers=self.headers,
                params={
                    "q": search_query,
                    "sort": params.sort_by,
                    "order": "desc",
                    "per_page": params.limit
                }
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("items"):
                return "No repositories found matching the specified criteria. Change filters and try again."
            
            results = []
            for repo in data.get("items", [])[:params.limit]:
                results.append(self._format_repository(repo))
            
            return results
        
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            return f"An error occurred: {err}"

