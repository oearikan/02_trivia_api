import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.operators import notin_op
from mylog import mylog

from models import setup_db, Question, Category

# QUESTIONS_PER_PAGE = 4
# I don't need this anymore as paginate() method from SQLAlchemy is used


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    '''
    CORS(app)
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            formatted_dict = {
              category.id: category.type for category in categories
            }
            return jsonify({"categories": formatted_dict})
        except Exception:
            abort(404)
    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination
    at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    # questions endpoint handler
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).paginate(
              per_page=4, page=request.args.get("page", 1, type=int)
            )
            current_questions = [
              question.format() for question in selection.items
            ]

            if current_questions == []:
                abort(404)
            categories = Category.query.all()
            formatted_categories = {
              category.id: category.type for category in categories
            }

            return jsonify({
              "success": True,
              "questions": current_questions,
              "total_questions": selection.total,
              "current_category": None,
              "categories": formatted_categories
            })
        except Exception:
            abort(404)
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
              Question.id == question_id
            ).one_or_none()
            if question is None:
                abort(404)
            question.delete()

            return jsonify({
              "success": True,
              "deleted": question_id,
            })
        except Exception:
            abort(404)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question
    will appear at the end of the last page
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
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            search = body.get("searchTerm", None)
            if not search:
                return jsonify({
                    "success": False,
                    "message": "Empty search is not allowed"
                })
            if search:
                selection = Question.query.order_by(Question.id).filter(
                  Question.question.ilike("%{}%".format(search))
                )
                current_questions = [
                  question.format() for question in selection
                ]

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_hits": len(current_questions),
                "current_category": None
                })
        except Exception:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        try:
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_difficulty = body.get("difficulty", None)
            new_category = body.get("category", None)
            check = [
              bool(new_question), bool(new_answer),
              bool(new_difficulty), bool(new_category)
            ]
            if not all(check):
                abort(422)

            question = Question(
              question=new_question,
              answer=new_answer,
              category=new_category,
              difficulty=new_difficulty
            )
            question.insert()

            return jsonify({
              "success": True,
            })

        except Exception:
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
        try:
            selection = Question.query.filter(
              Question.category == category_id
            ).paginate(
              per_page=4, page=request.args.get("page", 1, type=int)
            )
            current_questions = [
              question.format() for question in selection.items
            ]
            category = Category.query.filter(
              Category.id == category_id
            ).first()

            if current_questions == []:
                abort(404)

            # I return total number of questions in this category
            # as returning all does not make much sense to me
            return jsonify({
              "questions": current_questions,
              "total_questions": selection.total,
              "current_category": category.type
            })
        except Exception:
            abort(404)

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
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", [])
            quiz_category = body.get("quiz_category", None)

            if int(quiz_category["id"]) == 0:
                questions = Question.query.all()
            elif quiz_category["id"]:
                questions = Question.query.filter(
                  Question.category == quiz_category["id"]
                ).all()

            if questions:
                quiz = []
                for question in questions:
                    if question.format()["id"] not in previous_questions:
                        quiz.append(question)

                return jsonify({
                    "question": random.choice(quiz).format()
                  })
            else:
                abort
        except Exception:
            abort(422)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
        }), 400
        )

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
        }), 422
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed"
        }), 405
        )

    @app.errorhandler(500)
    def server_error(error):
        return (jsonify({
          "success": False,
          "error": 500,
          "message": "something went wrong on the server"
        }), 500
        )
    return app
