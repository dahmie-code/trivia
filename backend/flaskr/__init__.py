import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    # querying all questions in Category
    def category_lists():
        query = db.session.query(Category).order_by(Category.id).all()
        category_all = {}
        for category in query:
            category_all[str(category.id)] = category.type
        return category_all
    # Set up CORS
    CORS(app, resources={r"*": {'orgins': '*'}})

    # Use after_request decorator to set Access-Control-Allow

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE')
        return response

    # endpoint to handle GET requests for all available categories
    
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.all()
        body = [category.format() for category in categories]
        
        return jsonify({
            'success': True,
            'body': body,
            'total_question': len(categories) 
            })

    #Endpoint to handle GET requests for questions, including pagination (every 10 questions).
    
    @app.route('/questions', methods=['GET'])
    def get_quiz():
        page = request.args.get('page', 1, type=int)
        current_quiz = db.session.query(Question).order_by(Question.id).paginate(page=page, each_page=QUESTIONS_PER_PAGE).items
        
        query = db.session.query(Question).order_by(Question.id).all()
        
        quizzes = []
        if len(current_quiz) == 0:
            return abort(404)
        
        for quiz in current_quiz:
            quizzes.append({
               'id': quiz.id,
               'question': quiz.question,
               'answer': quiz.answer,
               'difficulty': quiz.difficulty,
               'category': quiz.category
            })
        return jsonify({
            'success': True,
            'questions': quizzes,
            'total_questions': len(query),
            'categories': category_lists(),
            'currentCategory': random.choice(list(category_lists().values()))
        })
    # Endpoint to DELETE question using a question ID.
    @app.route('/question/<int:question_id>', methods=['DELETE'])
    def delete_quiz(quiz_id):
        quiz = Question.query.get(quiz_id)
        print(quiz)

        try:
            quiz.delete()
        except:
            return abort(404)
        return jsonify({
            'success': True,
            'quiz_id': quiz_id
        })
    # Endpoint to POST a new question
    @app.route('/questions', methods=['POST'])
    def new_question():
        body = request.get_json()
        if body is None:
            abort(400)
        
        try:
           question = Question(question=body['question'], answer=body['answer'], category=['category'], difficulty=['difficulty'])
           question.insert()
        except:
            abort(404)
        return jsonify({
            'success': True,
            'question': question
        })
    # POST endpoint to get questions based on a search term.
    @app.route('/questions/search', methods=['POST'])
    def search():
        search_term = request.get_json()['searchTerm']
        query = Question.query.filter(
            Question.query.ilike(f'%{search_term}%')).all()
        
        quizzes = []
        
        if query is None:
            abort(422)
        else:
            for quiz in query:
                quizzes.append({
                    'id': quiz.id,
                    'question': quiz.question,
                    'answer': quiz.answer,
                    'difficulty': quiz.difficulty,
                    'category': quiz.category
                })
        return jsonify({
                'success': True,
                'questions': quizzes,
                'total_questions': len(quizzes),
                'current_category': random.choice(quizzes).get('category') if len(quizzes) > 0 else 'category does not exist'
            })
    # GET endpoint to get questions based on category.
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_quiz_by_category(id):
        try:
            category = Question.query.filter(
            Question.category == str(id)).all()
        
            
            return jsonify({
                'success': True,
                'questions': [question.format() for question in category],
                'total_questions': len(category),
                'current_category': id
            })
        except:
            abort(404)
      
    # POST endpoint to get questions to play the quiz
    
    @app.route('/quizzes', methods=['POST'])
    def get_questions():
        previous_quiz = request.get_json()['previous_questions']
        category = request.get_json()['quiz_category']
        category_id = category['id']
        print(category)
        
        query_all = Question.query.all()
        current_quiz =[]
        
        if previous_quiz is None:
            abort(422)
        else:
            for quiz in query_all:
                if len(previous_quiz) == 0 and int(category_id) != quiz.category:
                    current_quiz.append(quiz.format())
                else:
                    for previous in previous_quiz:
                        if previous != quiz.id and int (category_id) != quiz.category:
                            current_quiz.append(quiz.format())
        return jsonify({'question': random.choice(current_quiz), 'success': True})
    # Error Handlers
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unable to be Processed'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500
        
    return app

