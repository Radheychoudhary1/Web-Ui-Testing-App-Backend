# activate your venv
.\.venv311\Scripts\Activate.ps1

# run uvicorn
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000