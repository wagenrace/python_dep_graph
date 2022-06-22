## Local testing

Make a env.list with NEO4J_URL, NEO4J_USER, and NEO4J_PSWD.
Run 

```cmd
uvicorn app.main:app --env-file env.list --port 80
```