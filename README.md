# :snake: Python REST API Demo

REST API providing basic functionality for managing user, books and tokens.

Backend: `python + flask`

### Docker Image

1. Create a `requirements.txt` file
1. Set up the `Dockerfile`
1. Add `docker-compose` file to the root so that the application runs automatically
1. Run `docker-compose build`
1. Run `docker image ls` to verify there is a **<project_name>_<service_name>** image
1. From project root, run `docker-compose up`
1. Connect the database, create `Dockerfile` at `/db` folder
1. Add `pymongo` to `requirements.txt` so that the app can communicate with the db
1. Use `py-bcrypt` for hasing the password ([library link](https://www.mindrot.org/projects/py-bcrypt/))
