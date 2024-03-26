import os
from dotenv import load_dotenv
from brave import Brave

def brave_request(query):
    # Your Brave API key
    load_dotenv(dotenv_path='.env')

    api_key = os.getenv("BRAVE_API_KEY")
    brave = Brave(api_key)

    num_results = 10

    search_results = brave.search(q=query, count=num_results)
    web_results = search_results.web_results

    output_data = {"results": []}
    for result in web_results:
        description = result['description']
        url = result['url']

        output_data["results"].append({"description": description, "url": url})

    return output_data