uv add fastapi
uv add uvicorn
uv add langchain
uv add langchain-openai
uv add python-dotenv
uv add pydantic
uv add langsmith
uv add streamlit

uv run uvicorn main:app --reload
uv run streamlit run ui/page.py


http://localhost:8501/

http://127.0.0.1:8000/query

https://smith.langchain.com/
