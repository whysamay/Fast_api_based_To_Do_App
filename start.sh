#!/bin/bash
cd ToDoApp
uvicorn main:app --host 0.0.0.0 --port $PORT 