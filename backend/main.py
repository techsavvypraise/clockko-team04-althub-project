#!/usr/bin/env python3
"""
ClockKo API Server
Main entry point for running the FastAPI application
"""
import uvicorn

# ---------- Structured JSON logging (for CloudWatch) ----------
import logging
import sys
from pythonjsonlogger import jsonlogger

# configure root logger to output JSON to stdout (avoids duplicate handlers)
_root_logger = logging.getLogger()
if not any(isinstance(h, logging.StreamHandler) for h in _root_logger.handlers):
    _handler = logging.StreamHandler(sys.stdout)
    _formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    _handler.setFormatter(_formatter)
    _root_logger.addHandler(_handler)

_root_logger.setLevel(logging.INFO)

# convenience logger for your app code
logger = logging.getLogger("clockko-backend")

# Example: logger.info("Health check called", extra={"event":"health_check"})
# -------------------------------------------------------------

from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
