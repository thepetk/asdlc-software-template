# Create a Simple Python Flask Application

Create a minimal Python Flask web application with a health endpoint and basic project structure.

## Objectives

- Create a Flask app with a `/health` endpoint that returns `{"status": "ok"}`
- Add a `requirements.txt` with pinned dependencies
- Add a `README.md` with instructions on how to run the app locally
- Write at least one pytest test covering the `/health` endpoint

## Acceptance Criteria

- The app starts without errors with `flask run`
- `GET /health` returns HTTP 200 and `{"status": "ok"}`
- `pytest` passes with no failures
- No unused imports or dependencies
