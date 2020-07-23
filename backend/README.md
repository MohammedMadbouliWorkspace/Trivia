# Full Stack Trivia API Backend

## Getting Started

---

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

You have to cd into `backend` directory where this `README.md` file is exist in,
and setup your virtual environment called `env` by running:
```bash
virtualenv env
source env/bin/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

---
With Postgres running:

1- Create a new database called `trivia` with the appropriate role by running:
```bash
createdb trivia
```

2- Go to both `flaskr/development.py` and `flaskr/testing.py` files and edit `SQLALCHEMY_DATABASE_URI` with the right database uri and username (and password if needed)

For e.g.:
```python
SQLALCHEMY_DATABASE_URI = "postgres://username:password@localhost:5432/trivia"
```

3- Migrate `trivia` schema and fill tables with initialized data by running this `dbfs.sh` shell script:
```bash
bash dbfs.sh
```

## Running the server

---

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP="flaskr:create_app('development.py')"
export FLASK_ENV=development
flask run
```

Or, just run this `run.sh` shell script:
```bash
bash run.sh
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing

---
After setting up the database, to run the tests, run:
```
python3 test_flaskr.py
```

## API Reference

---

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:
```json
    {
        "success_status": false,
        "message": "The resource/s cannot be found",
        "error": 404
    }
```

The API will return three error types when requests fail:

- `404 Not Found`: The resource/s cannot be found
- `405 Method Not Allowed`: This method is not allowed in this endpoint
- `422 Unprocessable Entity`: This operation cannot be done

### Endpoints

**GET /categories**
- General:
    - Fetches all categories.
    - Arguments: No arguments needed.
    - Returns: JSON view for `"categories"` including every `"id"` and `"type"` of each category.

- Sample:

    `curl -X GET "http://127.0.0.1:5000/categories"`

    ```bash
    {
        "categories": [
            {
                "id": 1,
                "type": "Science"
            },
            {
                "id": 2,
                "type": "Art"
            },
            {
                "id": 3,
                "type": "Geography"
            },
            {
                "id": 4,
                "type": "History"
            },
            {
                "id": 5,
                "type": "Entertainment"
            },
            {
                "id": 6,
                "type": "Sports"
            }
        ]
    }
    ```

**GET /categories/{category_id}**
- General:
    - Fetches specific category by its id in `{category_id}`.
    - Arguments: No arguments needed.
    - Returns: JSON view for `"category"` including `"id"` and `"type"`.

- Sample:

    `curl -X GET "http://127.0.0.1:5000/categories/1"`

    ```bash
    {
        "category": {
            "id": 1,
            "type": "Science"
        }
    }
    ```

**GET /categories/{category_id}/questions**
- General:
    - Fetches all questions paginated in specific category by its id in `{category_id}`.

    - Arguments:
        - `length={questions_per_page}`:
            - `{questions_per_page}` is for probable number of questions in a single page (optional, default=10)

        - `page={page_number}`:
            - `{page_number}` is for number of the current page and it depends on `length` (optional, default=1)

    - Returns: JSON view for:
        - `"questions"` including every `"id"`, `"question"`. `"answer"`, `"category"` and `"difficulty"` of each question.
        - `"total_questions"` which is the total number of questions in this category.
        - `"categories"` including every `"id"` and `"type"` of each category.
        - `"current_category"` including `"id"` and `"type"`.

- Sample:

    `curl -X GET "http://127.0.0.1:5000/categories/2/questions?length=2&page=1"`

    ```bash
    {
        "categories": [
            {
                "id": 1,
                "type": "Science"
            },
            {
                "id": 2,
                "type": "Art"
            },
            {
                "id": 3,
                "type": "Geography"
            },
            {
                "id": 4,
                "type": "History"
            },
            {
                "id": 5,
                "type": "Entertainment"
            },
            {
                "id": 6,
                "type": "Sports"
            }
        ],
        "current_category": {
            "id": 2,
            "type": "Art"
        },
        "questions": [
            {
                "answer": "Escher",
                "category": {
                    "id": 2,
                    "type": "Art"
                },
                "difficulty": 1,
                "id": 12,
                "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
            },
            {
                "answer": "Mona Lisa",
                "category": {
                    "id": 2,
                    "type": "Art"
                },
                "difficulty": 3,
                "id": 13,
                "question": "La Giaconda is better known as what?"
            }
        ],
        "total_questions": 4
    }
    ```

**GET /questions**
- General:
    - Fetches all questions paginated.

    - Arguments:
        - `length={questions_per_page}`:
            - `{questions_per_page}` is for probable number of questions in a single page (optional, default=10)

        - `page={page_number}`:
            - `{page_number}` is for number of the current page and it depends on `length` (optional, default=1)
            
    - Returns: JSON view for:
        - `"questions"` including every `"id"`, `"question"`. `"answer"`, `"category"` and `"difficulty"` of each question.
        - `"total_questions"` which is the total number of questions in the database.
        - `"categories"` including every `"id"` and `"type"` of each category.
        - `"current_category"` which is always `""` for this endpoint.

- Sample:

    `curl -X GET "http://127.0.0.1:5000/questions?length=5&page=2"`

    ```bash
    {
        "categories": [
            {
                "id": 1,
                "type": "Science"
            },
            {
                "id": 2,
                "type": "Art"
            },
            {
                "id": 3,
                "type": "Geography"
            },
            {
                "id": 4,
                "type": "History"
            },
            {
                "id": 5,
                "type": "Entertainment"
            },
            {
                "id": 6,
                "type": "Sports"
            }
        ],
        "current_category": "",
        "questions": [
            {
                "answer": "Brazil",
                "category": {
                    "id": 6,
                    "type": "Sports"
                },
                "difficulty": 3,
                "id": 6,
                "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
                "answer": "Uruguay",
                "category": {
                    "id": 6,
                    "type": "Sports"
                },
                "difficulty": 4,
                "id": 7,
                "question": "Which country won the first ever soccer World Cup in 1930?"
            },
            {
                "answer": "George Washington Carver",
                "category": {
                    "id": 4,
                    "type": "History"
                },
                "difficulty": 2,
                "id": 8,
                "question": "Who invented Peanut Butter?"
            },
            {
                "answer": "Lake Victoria",
                "category": {
                    "id": 3,
                    "type": "Geography"
                },
                "difficulty": 2,
                "id": 9,
                "question": "What is the largest lake in Africa?"
            },
            {
                "answer": "The Palace of Versailles",
                "category": {
                    "id": 3,
                    "type": "Geography"
                },
                "difficulty": 3,
                "id": 10,
                "question": "In which royal palace would you find the Hall of Mirrors?"
            }
        ],
        "total_questions": 19
    }
    ```

**POST /questions**

* To search for questions by a keyword

    - General:
        - Searches for questions that include a keyword.
        - Arguments: No arguments needed.
        - Returns: JSON view for:
            - `"questions"` including every `"id"`, `"question"`. `"answer"`, `"category"` and `"difficulty"` of each question.
            - `"total_questions"` which is the total number of results.
            - `"categories"` including every `"id"` and `"type"` of each category.
            - `"current_category"` which is always `""` for this endpoint.

    - Headers:
        - `Content-Type: application/json`

    - Body:
        - To trigger this endpoint you have to provide this body of JSON type:
            ```json
            {
                "search_term": "{keyword}"
            }
            ```

    - Sample:

        `curl -X POST "http://127.0.0.1:5000/questions" -H "Content-Type: application/json" -d '{"search_term":"Cassius"}'`

        ```bash
        {
            "categories": [
                {
                    "id": 1,
                    "type": "Science"
                },
                {
                    "id": 2,
                    "type": "Art"
                },
                {
                    "id": 3,
                    "type": "Geography"
                },
                {
                    "id": 4,
                    "type": "History"
                },
                {
                    "id": 5,
                    "type": "Entertainment"
                },
                {
                    "id": 6,
                    "type": "Sports"
                }
            ],
            "current_category": "",
            "questions": [
                {
                    "answer": "Muhammad Ali",
                    "category": {
                        "id": 4,
                        "type": "History"
                    },
                    "difficulty": 1,
                    "id": 2,
                    "question": "What boxer's original name is Cassius Clay?"
                }
            ],
            "total_questions": 1
        }
        ```

* To add a new question

    - General:
        - Adds a new question record to database.
        - Arguments: No arguments needed.
        - Returns: JSON view for:
            - `"success_status"` which will be `true` if adding operation succeeded.
            - `"new_question"` including `"id"`, `"question"`. `"answer"`, `"category"` and `"difficulty"`.
            - `"message"` which descibes the operation status.

    - Headers:
        - `Content-Type: application/json`

    - Body:
        - To trigger this endpoint you have to provide this body of JSON type:
            ```json
            {
                "question": "{question}",
                "answer": "{answer}",
                "difficulty": "{difficulty_number}",
                "category_id": "{category_id}"
            }
            ```

    - Sample:

        `curl -X POST "http://127.0.0.1:5000/questions" -H "Content-Type: application/json" -d '{"question":"What is your name?","answer":"JSONer","difficulty":4,"category_id":5}'`

        ```bash
        {
            "message": "addition operation has been done successfully",
            "new_question": {
                "answer": "JSONer",
                "category": {
                    "id": 5,
                    "type": "Entertainment"
                },
                "difficulty": 4,
                "id": 20,
                "question": "What is your name?"
            },
            "success_status": true
        }
        ```

**GET /questions/{question_id}**
- General:
    - Fetches specific question by its id in `{question_id}`.
    - Arguments: No arguments needed.
    - Returns: JSON view for `"question"` including `"id"`, `"question"`. `"answer"`, `"category"` and `"difficulty"`.

- Sample:

    `curl -X GET "http://127.0.0.1:5000/questions/1"`

    ```bash
    {
        "question": {
            "answer": "Maya Angelou",
            "category": {
                "id": 4,
                "type": "History"
            },
            "difficulty": 2,
            "id": 1,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
    }
    ```

**DELETE /questions/{question_id}**
- General:
    - Deletes specific question record from database by id in `{question_id}`.
    - Arguments: No arguments needed.
    - Returns: JSON view for:
            - `"success_status"` which will be `true` if deleting operation succeeded.
            - `"message"` which descibes the operation status.

- Sample:

    `curl -X DELETE "http://127.0.0.1:5000/questions/20"` (notice that is the id of the last added question above)

    ```bash
    {
        "message": "deletion operation has been done successfully",
        "success_status": true
    }
    ```

**POST /quizzes**
- General:
    - Fetches random question in specific category (if provided) or in any category 
    and plays quizzes by providing a list of previous questions IDs to avoid repeating the same random questions

    - By continuing playing with specific category, 
    if you reached the last question in this category, 
    it'll make an end-game force by returning a `false` value within question

    - Arguments: No arguments needed.
    
    - Returns: JSON view for `"question"` including `"id"`, `"question"`. `"answer"`, `"category"` and `"difficulty"`, or it will be `false` on force-end.

- Headers:
    - `Content-Type: application/json`

- Body:
    - To trigger this endpoint you have to provide this body of JSON type:
        ```json
        {
            "previous_questions_ids": ["{previous_questions_ids}"], // for e.g., [1, 2, 3, 4]
            "quiz_category_id": "{category_id}" 
        }
        ```
        >   `"quiz_category_id"` is optional, but if it's not provided, the game won't end until you provide all questions IDs in the database in `"previous_questions_ids"`

- Sample:

    `curl -X POST "http://127.0.0.1:5000/quizzes" -H "Content-Type: application/json" -d '{"previous_questions_ids":[],"quiz_category_id":6}'`

    ```bash
    {
        "question": {
            "answer": "Uruguay",
            "category": {
                "id": 6,
                "type": "Sports"
            },
            "difficulty": 4,
            "id": 7,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    }
    ```

    `curl -X POST "http://127.0.0.1:5000/quizzes" -H "Content-Type: application/json" -d '{"previous_questions_ids":[7],"quiz_category_id":6}'`

    ```bash
    {
        "question": {
            "answer": "Brazil",
            "category": {
                "id": 6,
                "type": "Sports"
            },
            "difficulty": 3,
            "id": 6,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        }
    }
    ```

    `curl -X POST "http://127.0.0.1:5000/quizzes" -H "Content-Type: application/json" -d '{"previous_questions_ids":[7,6],"quiz_category_id":6}'`

    ```bash
    {
        "question": false
    }
    ```

## Authors

---
Mohammed Madbouli

## Acknowledgements

---
The awesome team at Udacity.