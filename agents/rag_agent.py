from langchain_openai import ChatOpenAI
from langchain.agents import create_agent 
from dotenv import load_dotenv

load_dotenv()


SYSTEM_PROMPT ="""You are an expert Retail banking and wealth advisory assistant 

Provide:
Perosnailised financial recommendations 
Product sustainbilty rationale
Risk warning
Actionable next steps

Based all recommendations on customers
-age
-income
-risk appetite
-financial goals
-excisting investments
-Liabilities

keep response clear,concise and professional

"""

def create_financial_agent():

	model=ChatOpenAI(
		model="gpt-5.5",
		temperature=0.2
	)

	return create_agent(
		model=model,
		system_prompt=SYSTEM_PROMPT,
    	
	)

	




