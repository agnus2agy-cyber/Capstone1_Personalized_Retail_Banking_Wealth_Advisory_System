from langchain_openai import ChatOpenAI

from core.settings import settings


def create_agent():

	llm = ChatOpenAI(
    	api_key=settings.OPENAI_API_KEY,
    	model="gpt-5.5",
    	temperature=0.2
	)

	return llm


