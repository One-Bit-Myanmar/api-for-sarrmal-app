import uvicorn

# define the entry point for running the application

# make sure you need to define host to [localhost] not [0.0.0.0]

# can also view the interactive API doc at [http://localhost:8000/doc]

# Routes ********
# before dive into the writing routes, you have to define the relevant schema and configure MongoDB
# you have to define schema inside the app/server/models dir


if __name__ == "__main__":
    uvicorn.run("server.app:app", host="localhost", port=8000, reload=True)

