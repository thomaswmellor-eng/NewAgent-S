#!/bin/bash
# Change to backend directory and run uvicorn
cd /tmp/*/backend 2>/dev/null || cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
