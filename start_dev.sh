exec uvicorn main:app --host 0.0.0.0 --port 5000 --env-file .env.local --reload --log-level debug --app-dir src
