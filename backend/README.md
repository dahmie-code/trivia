# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Setting up the Database

With Postgres running, I created a `trivia` database:

```bash
createbd trivia
```

I populated the database using the `trivia.psql` file. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

These are the backend files to check:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

For each endpoint, I defined the endpoint and response data. The frontend is set up to expect certain endpoints and response data formats. 
1. I used Flask-CORS to enable cross-domain requests and set response headers.
2. I created an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. I created endpoint to handle `GET` requests for all available categories.
4. I created endpoint to `DELETE` a question using a question `ID`.
5. I created endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. I created `POST` endpoint to get questions based on category.
7. I created `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. I created `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. I created error handlers for all expected errors including 400, 404, 422, and 500.

