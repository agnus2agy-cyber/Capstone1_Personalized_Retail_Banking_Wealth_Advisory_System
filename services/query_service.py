from agents.rag_agent import create_financial_agent

agent = create_financial_agent()


async def process_query(request):
    try:
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                        CUSTOMER_PROFILE:{request.customer_profile.model_dump()}
                        QUESTION:{request.question}""",
                    }
                ]
            }
        )
        return {"answer": response["messages"][-1].text}
    except Exception as e:
        return {"answer": f"Error:{str(e)}"}
