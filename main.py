# main.py

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
import os
from dice_system import resolve_action

app = FastAPI()

# 从环境变量中读取 API_KEY
API_KEY = os.getenv("API_KEY")

class ActionRequest(BaseModel):
    luck: int
    difficulty_modifiers: List[int]
    situational_modifiers: List[int]

class ActionResponse(BaseModel):
    base_roll: int
    final_roll: int
    outcome: str
    description: str
    modifiers_breakdown: str

@app.post("/resolve_action", response_model=ActionResponse)
def api_resolve_action(request: ActionRequest, api_key: Optional[str] = Header(None)):
    # 验证 API_KEY
    if API_KEY and api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # 验证 luck 值在 0 到 100 之间
    if not (0 <= request.luck <= 100):
        raise HTTPException(status_code=400, detail="Luck must be between 0 and 100.")

    # 调用 resolve_action 函数
    result = resolve_action(
        luck=request.luck,
        difficulty_modifiers=request.difficulty_modifiers,
        situational_modifiers=request.situational_modifiers
    )

    # 解析结果
    lines = result.split('\n')
    if len(lines) < 5:
        raise HTTPException(status_code=500, detail="Invalid response format from dice_system.")

    base_roll_line = lines[0]
    final_roll_line = lines[1]
    outcome_line = lines[2]
    description_line = lines[3]
    modifiers_breakdown = '\n'.join(lines[4:])

    # 提取数值
    try:
        base_roll = int(base_roll_line.split(': ')[1])
        final_roll = int(final_roll_line.split(': ')[1])
    except (IndexError, ValueError) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing rolls: {e}")

    try:
        outcome = outcome_line.split(': ')[1]
        description = description_line.split(': ')[1]
    except IndexError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing outcome/description: {e}")

    return ActionResponse(
        base_roll=base_roll,
        final_roll=final_roll,
        outcome=outcome,
        description=description,
        modifiers_breakdown=modifiers_breakdown
    )
