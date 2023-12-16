# Setup

- run `./setup.sh` or (setup.bat in windows )to build python environment and install libraries

- to run orientdb
  container: `docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -v opt:/opt/orientdb -e ORIENTDB_ROOT_PASSWORD=root orientdb:latest`

- #### .venv/lib/pyorient/exceptions.py:5 needs to change 'error' to 'error=None

# Configuration

- Environment variables goes in .env file, so pedantic BaseSetting can reach it
- mandatory variables: ORIENT_USER, ORIENT_PASSWORD, ORIENT_DB

# Test

- run `pytest`  or  `pytest --cov` then `coverage html`

# Run

- After Setting up the environment and configuring variables, run `:./run.sh`

# Routes

(better api documentation is at openai /docs)

- **Class Routes**
- POST /classes: Create a new class.
- PUT /classes: Update an existing class.
- DELETE /classes: Delete a class (temporary disabled).
- GET /classes?class-name: Retrieve class information.
- GET /classes/all: Retrieve a list of all classes.

- **Vertex Routes**
- POST /vertex/{class_name}: Create a new vertex.
- PUT /vertex/{class_name}: Update an existing vertex.
- DELETE /vertex/{vertex_id}: Delete a vertex.
- GET /vertex/{class_name}: Retrieve vertices of a class.

- **Edge Routes**
- POST /edge/{class_name}: Create a new edge.
- PUT /edge/{class_name}: Update an existing edge.
- DELETE /edge/{edge_id}: Delete an edge.
- GET /edge/{class_name}: Retrieve edges of a class.
