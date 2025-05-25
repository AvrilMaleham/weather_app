# weather_db_sqlalchemy

To view this project locally:

### `git clone git@github.com:AvrilMaleham/weather_db_sqlalchemy.git`

Clone the app into the directory of your choice.

### `python -m venv venv`

Create a virtual environment (optional but recommended).

### `pip install -r requirements.txt`

Install dependencies.

Make sure **Docker** is installed locally.

### `cd apps/api`

Move into the correct directory.

### `docker-compose up -d`

Sets up a Docker container for the DB **and** a Docker container for the API.

Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger the browser.

### `docker exec -it api-db-1 psql -U postgres -d weatherdb`

Programatically access the DB.

# Key project skills:

- SQLAlchemy
- Docker
- FastAPI
- DB Design
- Seeding & Populating a Database
- API Integration
