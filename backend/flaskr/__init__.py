import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import asc, desc , func
from flask_cors import CORS
import random
import sys
import json


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  
  
  def paginated_questions(page,questions):

    # if page > (len(questions)/QUESTIONS_PER_PAGE):
    #   abort(404)

    start = (page-1) *QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formated_questions = [question.format() for question in questions]
    return  formated_questions[start : end]

  def get_categories_list():
    categories = Category.query.all()
    categories_array = {}
    for cat in categories:
      categories_array[cat.id]=cat.type
    return categories_array

  #test Route
  # @app.route('/')
  # def index():
  #   return jsonify({
  #     'success' : True,
  #     'message' : 'HELLOOOO'
  #   })


  #endpoint retrieve all available categories.
  @app.route('/categories')
  def retrieve_categories():
    categories = Category.query.all()
    formated_categories = get_categories_list()
    #[category.format() for category in categories]

    if len(categories) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'categories': formated_categories
    })

  

  #endpoint to handle GET requests for questions,
  @app.route('/questions')       
  def get_questions_list():
      
      questions = Question.query.order_by(desc(Question.id)).all()
      page = request.args.get('page',1, type=int)
      formated_questions=paginated_questions(page,questions)
      
      categories_array = get_categories_list()
    
      
      if len(questions) == 0:
        abort(404)

      return  jsonify({
          'success':True,
          'questions' : formated_questions,
          'total_questions' : len(questions),
          'categories' : categories_array, 
          'current_category' : None #todo
          })
 


  #endpoint to DELETE question using a question ID
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      questions = Question.query.order_by(Question.id).all()
      page = request.args.get('page',1, type=int)
      formated_questions=paginated_questions(page,questions)
      categories_array = get_categories_list()

      return jsonify({
        'success':True,
        'questions' : formated_questions,
        'total_questions' : len(questions),
        'categories' : categories_array, 
        'current_category' : None 
      })

    except:
      abort(422)


 #endpoint to POST a new question 
 # Search by Search Term
  @app.route('/questions', methods=['POST'])
  def create_question():
   
    body = request.get_json()
    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)
    searchTerm = body.get('searchTerm', None)
    page = request.args.get('page',1, type=int)
    
    try:
      categories_array = get_categories_list()
      if searchTerm != None:
        query =  Question.query.filter((Question.question.ilike("%{}%".format(searchTerm))) | (Question.answer.ilike("%{}%".format(searchTerm))))                     
        search_result = query.order_by(desc(Question.id)).all()
       
        formated_questions = paginated_questions(page,search_result)
       
        return jsonify({
          'success': True,
          'questions': formated_questions,
          'total_questions' : len(search_result),
          'categories' : categories_array, 
          'current_category' : None #category
        })
      else: 
        new_question = Question(question=question, answer=answer, difficulty=difficulty,category=category)
        new_question.insert()

        questions = Question.query.order_by(desc(Question.id)).all()
        page = request.args.get('page',1, type=int)
        formated_questions = paginated_questions(page,questions)

        return jsonify({
          'success':True,
          # 'questions' : formated_questions,
          # 'total_questions' : len(questions),
          # 'categories' : categories_array, 
          # 'current_category' : None #category
        })

    except:
      print(sys.exc_info())
      abort(422)

  
  #endpoint to get questions based on category.
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
      questions = Question.query.filter(Question.category == category_id).all()
      page = request.args.get('page',1, type=int)
      formated_questions = paginated_questions(page,questions)
      categories_array = get_categories_list()
 
      if len(questions) == 0:
        abort(404)

      return jsonify({
          'success':True,
          'questions' : formated_questions,
          'total_questions' : len(questions),
          'categories' : categories_array, 
          'current_category' : category_id
      })


 
  #endpoint to get random questions to play the quiz
  @app.route('/quizzes', methods=['POST'])
  def select_random_question():
    
    body = request.get_json()
    previous_questions = body.get('previous_questions', {})
    quiz_category = body.get('quiz_category', None)
    category_id = quiz_category.get('id')

    try:   
      query =  Question.query.filter(~Question.id.in_(previous_questions))              
      if category_id !=0 :
        query = query.filter(Question.category == category_id)  
        total_cat_questions = Question.query.filter(Question.category == category_id).count()      
    
      selected_question = query.order_by(func.random()).first()
      
      return jsonify({
        'success': True,
        'question': selected_question.format()  if selected_question!= None else None,
        'total_cat_questions' : total_cat_questions
      })
     
 
    except:
      print(sys.exc_info())
      abort(422)

     
        
 #error handlers for all expected errors 
 
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  
  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed for this request"
      }), 405

  @app.errorhandler(500)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": " Internal Server Error"
      }), 500
  
  return app

    