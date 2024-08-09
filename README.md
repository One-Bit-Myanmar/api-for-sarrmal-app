## API with MongoDB Integration

1. Create **credentials.env** file inside **/app/.** directory
   
2. Add the following lines inside you credentials file
```env
MONGO_CONNECTION_STRING = "<YOUR_ACTUAL_CONNECTION_STRING>"
```

Application Structure

```
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

**If you encountered an error wnile running just type the following command**

```shell

set PYTHONPATH=%PYTHONPATH%;C:\Users\acer\Desktop\Development\fastapi

```

### Reference
- https://github.com/Krishna-D-K/FastAPI_Mongo