from fastapi import APIRouter

from app.schemas import WebActionPlanRequest, WebActionPlanResponse
from app.services.web_action_planner import make_web_action_plan

router = APIRouter(prefix="/api/web-actions", tags=["web-actions"])


# ==============================================================================
# PHASE 4: THE HANDS (Safe Web Actions Route)
# ==============================================================================
@router.post("/plan", response_model=WebActionPlanResponse)
async def plan_web_action(request: WebActionPlanRequest) -> WebActionPlanResponse:
    """
    TODO (Phase 4 - Step 9):
    Return planned destination URL for frontend user confirmation.
    """
    if not request.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be blank.")
    return WebActionPlanResponse(**make_web_action_plan(request.text))
