from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from tools.web_search_tool import web_search


load_dotenv()


model = ChatGroq(
    model="openai/gpt-oss-120b"
)


web_search_agent = create_agent(
    model=model,
    tools=[web_search],
    system_prompt="""
You are a professional Web Research Agent.

Your responsibility is to research information from the web.

Rules:

1. Use the web_search tool when current or external
   information is required.

2. Do not invent information.

3. Base your answer on the search results.

4. Provide a clear and concise answer.

5. When useful, mention the source URLs.
"""
)

query = input(
    "Ask the Web Search Agent: "
)


result = web_search_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }
)


print("\n" + "=" * 60)
print("WEB SEARCH AGENT")
print("=" * 60)

print(result["messages"][-1].content)