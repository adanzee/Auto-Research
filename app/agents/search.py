from langchain_exa import ExaSearchResults 
import config 

search_tool = ExaSearchResults(exa_api_key=config.exasearch_api_key, max_results=5)
results = search_tool.invoke({
    "query": "Latest AI agent frameworks"
})

print(type(results))
