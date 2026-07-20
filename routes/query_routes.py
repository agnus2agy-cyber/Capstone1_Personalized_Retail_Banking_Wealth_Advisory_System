from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from services.query_service import process_query

router = APIRouter()


class Goal(BaseModel):
	goal: str
	target_amount: float
	years: int


class CustomerProfile(BaseModel):
	customer_id: str
	age: int
	income: float
	employment: str
	risk_appetite: str
	goals: List[Goal]
	existing_investments: Dict
	liabilities: Dict
	monthly_expenses: float
	credit_score: int


class QueryRequest(BaseModel):
	question: str
	customer_profile: CustomerProfile


@router.post("/query")
async def query(request: QueryRequest):
	return await process_query(request)


