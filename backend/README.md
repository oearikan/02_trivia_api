# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
### ===student documentation start===

## Endpoints
### GET 'api/v1.0/categories'
- **General:** Fetches a dictionary of categories in which the keys are the ids and the values are the corresponding strings of the categories
- **Request arguments:** None
- **Returns:** An object with all available categories as a single dictionary item with id-type string as key-value pairs.
- **Sample request & response:** 
    - curl -X GET http://127.0.0.1:5000/categories
    - {
  "categories": {     
    "1": "Science",   
    "2": "Art",       
    "3": "Geography", 
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}

### GET 'api/v1.0/questions?page=${int}'
- **General:** Fetches a paginated list of all questions (4 questions per page). 
- **Request arguments:** Page number can be given as an optional argument. If none is given 1st page is returned by default.
- **Returns:** An object that includes categories, current category, the questions list including the question, the answer to the question, the category, the id and the difficulty as well as a success message and total number of questions.
- **Sample request & response:**
    - curl -X GET http://127.0.0.1:5000/questions?page=2
    - {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}

### GET 'api/v1.0/categories/${id}/questions'
- **General:** Fetches questions for a category specified by the id in request argument
- **Request arguments:** An integer representing the category id. An optional "page" argument can be provided if total number of questions for that category exceed 1 page.
- **Returns:** An object that contains the following: A list of all questions for requested category, Total number of questions in that category, category type that the category id corresponds to.
- **Sample request & response:**
    - curl -X GET http://127.0.0.1:5000/categories/2/questions?page=1
    - {
  "current_category": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "total_questions": 4
}

### DELETE 'api/v1.0/questions/${id}'
- **General:** Deletes a specified question using the id of the question.
- **Request arguments:** id of the question to be deleted as integer.
- **Returns:** An object with a sucess message and the id of the successfully deleted question
- **Sample request & response:**
    - curl -X DELETE http://127.0.0.1:5000/questions/25
    - {
  "deleted": 25,
  "success": true
}

### POST 'api/v1.0/questions' => Add new question
- **General:** Sends a post request in order to add a new question.
- **Request arguments:** A request body formatted as follows:
    - {
    "question":  "Question string",
    "answer":  "Answer string",
    "difficulty": "an integer in the [1-5] interval",
    "category": "category code, an integer"
}
- **Returns:** A success message upon successful insertion of new question
- **Sample request & response:**
    - curl -X POST -H "Content-Type: application/json" -d'{
    "question":  "What is the purpose of this?",
    "answer":  "Testing my end points, of course!",
    "difficulty": 1,
    "category": 3
}' http://127.0.0.1:5000/questions
    
    - {
  "success": true
}

### POST 'api/v1.0/questions' => Search for a question
- **General:** Sends a post request in order to search for a specific question by search term in a case insensitive fashion. Note that this is the same end point to post new questions. The structure of the request arguments determines the response type.
- **Request arguments:** For search operation in this endpoint, a request body structured as follows can be used:
{
    "searchTerm": "this is the term the user is looking for"
}
- **Returns:** An object with following parameters: A success message, a list of questions which have the case insensitive search terms in the question key of the Question object, total number of hits and current category.
- **Sample request & response:**
    - curl -X POST -H "Content-Type:application/json" -d'{"searchTerm":"who"}' http://127.0.0.1:5000/questions
    - {
  "current_category": null,
  "questions": [
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_hits": 2
}

### POST 'api/v1.0/quizzes'
- **General:** Sends a post request in order to get the next question during the quiz play.
- **Request arguments:** Two arguments; previous questions and quiz category; should be provided in the following format:
{"previous_questions": an array of question id's such as [1,5,15,12], "quiz_category": "a string of current category"}
- **Returns:** A single new question object
- **Sample request & response:**
    - curl -X POST -H "Content-Type: application/json" -d'{
    "previous_questions": [1,4,20,15,16,17],
    "quiz_category":{"id":2, "type":"Art"}
}' http://127.0.0.1:5000/quizzes
    - {
  "question": {
    "answer": "One",
    "category": 2,
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }
}