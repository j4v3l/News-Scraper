#!/bin/bash
python main.py &
uvicorn api.app.main:app --host 0.0.0.0 --port 1876
