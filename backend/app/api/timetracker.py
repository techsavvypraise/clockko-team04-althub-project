from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.timelog import StartSessionRequest, EndSessionRequest, TimeLogResponse
from app.services import timetrackerservice
import logging

# Use the same logger configured in main.py
logger = logging.getLogger("clockko-backend")

router = APIRouter(tags=["time-log"])


@router.post("/time-logs/start-work", response_model=TimeLogResponse)
def start_work(request: StartSessionRequest, db: Session = Depends(get_db)):
    logger.info("Start work requested", extra={"user_id": request.user_id})
    return timetrackerservice.start_session(db, request, session_type="work")


@router.post("/time-logs/end-work", response_model=TimeLogResponse)
def end_work(request: EndSessionRequest, db: Session = Depends(get_db)):
    logger.info("End work requested", extra={"user_id": request.user_id})
    result = timetrackerservice.end_session(db, request, session_type="work")
    if not result:
        logger.warning("No open work session found", extra={"user_id": request.user_id})
        raise HTTPException(status_code=404, detail="No open work session found")
    return result


@router.post("/time-logs/start-break", response_model=TimeLogResponse)
def start_break(request: StartSessionRequest, db: Session = Depends(get_db)):
    logger.info("Start break requested", extra={"user_id": request.user_id})
    return timetrackerservice.start_session(db, request, session_type="break")


@router.post("/time-logs/end-break", response_model=TimeLogResponse)
def end_break(request: EndSessionRequest, db: Session = Depends(get_db)):
    logger.info("End break requested", extra={"user_id": request.user_id})
    result = timetrackerservice.end_session(db, request, session_type="break")
    if not result:
        logger.warning("No open break session found", extra={"user_id": request.user_id})
        raise HTTPException(status_code=404, detail="No open break session found")
    return result


@router.get("/time-logs", response_model=list[TimeLogResponse])
def get_logs(user_id: str, db: Session = Depends(get_db)):
    logger.info("Fetching time logs", extra={"user_id": user_id})
    return timetrackerservice.list_time_logs(db, user_id)


@router.get("/time-logs/summary")
def get_summary(session_id: str, db: Session = Depends(get_db)):
    logger.info("Fetching session summary", extra={"session_id": session_id})
    return timetrackerservice.get_summary(db, session_id)


@router.get("/time-logs/current", response_model=TimeLogResponse)
def current_session(user_id: str, db: Session = Depends(get_db)):
    logger.info("Fetching current session", extra={"user_id": user_id})
    result = timetrackerservice.get_current_session(db, user_id)
    if not result:
        logger.warning("No ongoing session", extra={"user_id": user_id})
        raise HTTPException(status_code=404, detail="No ongoing session")
    return result
