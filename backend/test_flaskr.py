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
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql:///"+self.database_name
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

    def test_404_access_undefined_route(self):
        res = self.client().get('/test')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
  
    #retrieve all available categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
       


   #endpoint to handle GET requests for questions 
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])

    def test_404_get_questions_not_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


   # endpoint to DELETE question using a question ID
    def test_delete_question(self):
        id_to_test_with= Question.query.first().id
        res = self.client().delete('/questions/'+str(id_to_test_with))
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == id_to_test_with).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertTrue(data['deleted_question'])
        self.assertEqual(question, None)

    def test_error_405_delete_question_without_id(self):
        res = self.client().delete('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], "method not allowed for this request")

    def test_error_422_delete_question_wrong_id(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], "unprocessable")


  #endpoint to POST a new question
    def test_create_new_question(self):
        new_question = {
            "question" : "testing question?",
            "answer" : "yes",
            "difficulty" : 1 , 
            "category" : 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_400_create_new_question_no_body(self):      
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400 )
        self.assertEqual(data['message'], "bad request")

    def test_error_400_create_new_question_missing_body(self):      
        new_question = {
            "question" : "testing question?",
            "answer" : "yes"            
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400 )
        self.assertEqual(data['message'], "bad request")

    def test_error_422_create_new_question_wrong_input(self):      
        new_question = {
            "question" : "testing question?",
            "answer" : "yes",
            "difficulty" : "dif" , 
            "category" : "Science"       
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422 )
        self.assertEqual(data['message'], "unprocessable")


    #endpoint to get questions based on a search term
    def test_search__questions_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': '?'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertNotEqual(len(data['questions']), 0)
    
    def test_search_questions_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': '00000'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'],[])
        self.assertEqual(data['total_questions'],0)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['questions']), 0)
    
    def test_error_search_questions_with_wrong_body(self):
        res = self.client().post('/questions', json={'search': '00000'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400 )
        self.assertEqual(data['message'], "bad request")


   #endpoint to get questions based on category
    def test_search_paginated_questions_by_category(self):
        res = self.client().get('categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])

    def test__error_404_search_questions_undefined_category(self):
        res = self.client().get('categories/10/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False),
        self.assertEqual(data['message'], "resource not found")
        

   #endpoint to get random questions to play the quiz
    def test_find_random_questions_for_quiz(self):
        res = self.client().post('/quizzes', json= {"previous_questions":[],
                                                      "quiz_category" :  { "type": "Science", "id": "1" }
                                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['total_cat_questions'])

    def test_error_400_find_random_questions_for_quiz_empty_body(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400 )
        self.assertEqual(data['message'], "bad request")

    def test_error_400_find_random_questions_for_quiz_wrong_body(self):
        res = self.client().post('/quizzes', json= {"previous":[],
                                                      "category" :  { "type": "Science", "id": "1" }
                                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400 )
        self.assertEqual(data['message'], "bad request")

    def test_error_400_find_random_questions_for_quiz_wrong_input(self):
        res = self.client().post('/quizzes', json= {"previous":[],
                                                      "category" : "Science"
                                                      })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400 )
        self.assertEqual(data['message'], "bad request")
        

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()