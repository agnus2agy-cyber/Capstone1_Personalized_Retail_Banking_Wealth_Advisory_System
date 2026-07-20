from agents.rag_agent import create_agent
from prompts.financial_prompt import SYSTEM_PROMPT


async def process_query(request):
try:
	llm = create_agent()

	prompt = f"""
	{SYSTEM_PROMPT}

	CUSTOMER PROFILE:
	{request.customer_profile}

	QUESTION:
	{request.question}
	"""

	response = llm.invoke(prompt)

	return {
    	"answer": response.content
	}

except Exception as e:
    return{
		"answer" :f"Error{str(e)}"
    }
