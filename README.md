## API with MongoDB Integration

1. Create **credentials.env** file inside **/app/.** directory
   
2. Add the following lines inside you credentials file
```env
MONGO_CONNECTION_STRING = "<YOUR_ACTUAL_CONNECTION_STRING>"
```

Application Structure

```mermaid
/app
    /models/*
    server.py
    routes.py
    credentials.env
/venv/*
README.md
requirements.txt
```


Run the application
```shell
uvicorn server:app --reload --port 8000
```

### Reference
- https://github.com/Krishna-D-K/FastAPI_Mongo