import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','sa','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_categories(self):
        resp = self.client().get("/categories")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data["categories"])
    
    def test_get_questions(self):
        resp = self.client().get("/questions")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

    def test_get_questions_beyond_valid_page(self):
        resp = self.client().get("/questions?page=10000")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_delete_question(self):
    #     resp = self.client().delete("/questions/29")
    #     data = json.loads(resp.data)

    #     question = Question.query.filter(Question.id == 29).one_or_none()

    #     self.assertEqual(resp.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 29)
    #     self.assertEqual(question, None)

    def test_search_questions_with_results(self):
        resp = self.client().post("/questions", json={"searchTerm": "who"})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(data["total_hits"], 2)

    def test_search_questions_without_results(self):
        resp = self.client().post("/questions", json={"searchTerm": "somegibberish"})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["questions"], [])
        self.assertEqual(data["total_hits"], 0)

#     def test_post_new_question(self):
#         resp = self.client().post("/questions", json={
#     "question":  "What was that again?",
#     "answer":  "Oh, just another post question endpoint test. No biggie.",
#     "difficulty": 1,
#     "category": 3
# })
#         data = json.loads(resp.data)

#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(data["success"], True)

    def test_get_questions_by_category(self):
        resp = self.client().get("/categories/2/questions")
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertNotEqual(data["total_questions"], 0)
        self.assertEqual(data["current_category"], "Art")
    
    def test_404_on_get_questions_by_category(self):
        resp = self.client().get("/categories/500/questions")
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_playing_quiz(self):
        resp = self.client().post("/quizzes", json={
            "previous_questions":[1,2,14,15],
            "quiz_category":{"id":2, "type":"Art"}
        })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data["question"])

    def test_playing_quiz(self):
        resp = self.client().post("/quizzes", json={
            "previous_questions":[1,2,14,15],
            "quiz_category":{"id":2, "type":"Art"}
        })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data["question"])

    def test_422_playing_quiz(self):
        resp = self.client().post("/quizzes", json={
            "previous_questions":[],
            "quiz_category":{}
        })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()