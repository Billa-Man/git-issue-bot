from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun
from langchain_community.tools.riza.command import ExecPython
from langchain_community.tools.riza.command import ExecJavaScript
from langchain_community.tools.stackexchange.tool import StackExchangeAPIWrapper
from langchain.agents import Tool

# Custom tools
from github_tools.github_issue_search_tool import GitHubIssueSearchTool
from github_tools.github_repo_explorer_tool import GitHubRepoExplorerTool

search = DuckDuckGoSearchRun()
stackexchange = StackExchangeAPIWrapper()
wikidata = WikidataQueryRun(api_wrapper=WikidataAPIWrapper())

tools = [
    Tool.from_function(
        func=search.invoke,
        name="DuckDuckGo Search",
        description="Search the web using DuckDuckGo",
    ),
    Tool.from_function(
        func=stackexchange.run,
        name="StackExchange Search",
        description="Search StackExchange for relevant questions",
    ),
    Tool.from_function(
        func=wikidata.run,
        name="Wikidata Query",
        description="Query Wikidata for information",
    ),

    # Code Interpreters
    ExecPython(),
    ExecJavaScript(),

    # Custom tools
    GitHubIssueSearchTool(),
    GitHubRepoExplorerTool(),
]