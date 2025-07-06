#!/usr/bin/env python3
"""
Test script to verify imports work correctly
"""
import sys
import os

# Add the ToDoApp directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ToDoApp'))

try:
    from ToDoApp.main import app
    print("✅ All imports successful!")
    print("✅ App created successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Other error: {e}")
    sys.exit(1) 