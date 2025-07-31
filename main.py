from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def fetch_search(query):
    response = client.responses.create(
        model="gpt-4.1-mini",
        tools=[{"type": "web_search_preview"}],
        input=query
    )
    return response.output_text


async def main():
    query = "search for at least 3 meme generator MCP's."
    tasks = [fetch_search(query) for _ in range(100)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    results_ok = [r for r in results if not isinstance(r, Exception)]
    results_err = [r for r in results if isinstance(r, Exception)]

    print("Got", len(results_ok), "responses out of", len(results))
    print("Number of errors:", len(results_err))
    if results_err:
        print("Sample error:", results_err[0])  

    with open("corpus.json", "w") as f:
        json.dump(results_ok, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())