from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun
from langchain_community.tools.stackexchange.tool import StackExchangeAPIWrapper, StackExchangeTool
from langchain.agents import Tool

# Custom tools
from github_tools.github_issue_search_tool import GitHubIssueSearchTool
from github_tools.github_repo_explorer_tool import GitHubRepoExplorerTool

from settings import settings

search = DuckDuckGoSearchRun()
stackexchange = StackExchangeTool(api_wrapper=StackExchangeAPIWrapper())
wikidata = WikidataQueryRun(api_wrapper=WikidataAPIWrapper())

tools = [
    Tool.from_function(
        func=search.invoke,
        name="duckduckgo_search",
        description="Search the web using DuckDuckGo",
    ),
    Tool.from_function(
        func=stackexchange.run,
        name="stackexchange_search",
        description="Search StackExchange for relevant questions",
    ),
    Tool.from_function(
        func=wikidata.run,
        name="wikidata_query",
        description="Query Wikidata for information",
    ),

    # Custom tools
    GitHubIssueSearchTool(github_token=settings.GITHUB_API_TOKEN),
    GitHubRepoExplorerTool(github_token=settings.GITHUB_API_TOKEN),
]