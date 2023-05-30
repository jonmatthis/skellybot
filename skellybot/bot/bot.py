import os

from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from dotenv import load_dotenv

from skellybot.bot.freemocap_vectorstore_agent import freemocap_retrieval_qa_chain


class Bot:
    def __init__(self):
        load_dotenv()
        self.search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
        self.tools = [
            Tool(
                name="Current Search",
                func=self.search.run,
                description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
            ),
            Tool(
                name="FreeMoCap Docs Question Answering Agent",
                func=freemocap_retrieval_qa_chain.run,
                description="useful for when you need to answer questions about FreeMoCap. The input to this should be a single question about FreeMoCap."
            )
        ]
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=.8)
        self.agent_chain = initialize_agent(self.tools, self.llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                            verbose=True, memory=self.memory)

    def run_agent(self, input_text):
        return self.agent_chain.run(input=input_text)


if __name__ == "__main__":


    bot = Bot()

    while True:
        input_text = input(">>>['q' to quit]>>> ")
        if input_text == "q":
            break
        print(bot.run_agent(input_text))
