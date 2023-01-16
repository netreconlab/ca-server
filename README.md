## To start the server on a machine
### Option 1
Use the docker-compose.yml file to run on a docker container or

### Option 2
Run directly on your local machine by:
1. Installing python 10 and poetry
2. Running `poetry install in the root directory`
3. Run `poetry run uvicorn server.main:app --host 0.0.0.0 --port 3000`
4. Then Go to `http://0.0.0.0:3000/docs` to view api docs and use as needed