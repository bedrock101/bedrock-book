from langchain import hub
from langchain.agents import AgentExecutor, create_xml_agent
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_aws import ChatBedrockConverse

llm = ChatBedrockConverse(model="anthropic.claude-3-5-sonnet-20240620-v1:0")
tools = [DuckDuckGoSearchResults(max_results=4)]
prompt = hub.pull("heuristicwave/xml-agent-convo-korean")

agent = create_xml_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "AWS reinvent 2024는 언제 열려?"})
