import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.operators import notin_op
from mylog import mylog

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 4

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  # A helper method to paginate the questions
  def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    sp = (page-1) * QUESTIONS_PER_PAGE
    ep = sp + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[sp:ep]

    return current_questions

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_dict = {category.id: category.type for category in categories}
    
    return jsonify({
      "categories": formatted_dict
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  
  # questions endpoint handler
  @app.route('/questions', methods=['GET'])
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    if current_questions==[]:
      abort(404)
    
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}

    return jsonify({
      "success": True,
      "questions": current_questions,
      "total_questions": len(selection),
      "current_category": None,
      "categories": formatted_categories
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      
      question.delete()

      return jsonify({
        "success": True,
        "deleted": question_id,
      })
    
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()

    new_question = body.get("question", None)
    new_answer = body.get("answer", None)
    new_difficulty = body.get("difficulty", None)
    new_category = body.get("category", None)

    search = body.get("searchTerm", None)

    try:
      if search:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search)))
        current_questions = [question.format() for question in selection]

        return jsonify ({
          "success": True,
          "questions": current_questions,
          "total_hits": len(current_questions),
          "current_category": None
        })
      
      else:
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        question.insert()

        return jsonify({
          "success": True,
        })

    except:
      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    selection = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, selection)
    category = Category.query.filter(Category.id == category_id).first()

    if current_questions == []:
      abort(404)
    
    # I return total number of questions in this category as returning all does not make much sense to me
    return jsonify({
      "questions": current_questions,
      "total_questions": len(current_questions),
      "current_category": category.type
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get("previous_questions", [])
    quiz_category = body.get("quiz_category", None)
    mylog(quiz_category)
    
    if quiz_category:
      questions = Question.query.filter(Question.category == quiz_category["id"]).all()
      if questions:
        quiz = []
        for question in questions:
          if question.format()["id"] not in previous_questions:
            quiz.append(question)
          # mylog(quiz)

          return jsonify({
            "question": random.choice(quiz).format()
          })
        else:
          abort(404)
    else:
        abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return (jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404
    )

  @app.errorhandler(422)
  def unprocessable(error):
    return (jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }),422
    )

  @app.errorhandler(405)
  def method_not_allowed(error):
    return (jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405
    )

  
  return app

    