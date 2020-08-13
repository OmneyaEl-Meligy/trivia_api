# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)



## API Reference

### Getting Started
- Base URL: The backend app is hosted at the default local host, `http://127.0.0.1:5000/`.
- Authentication: No authentication required. 

### Error Handling
Error is returned as JSON objects as follows:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
Error types :
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal Server Error

### Endpoints 
  # GET '/categories'
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
  - Sample: 
      -Request:  `curl http://127.0.0.1:5000/categories`
      -Response:

          {'1' : "Science",
          '2' : "Art",
          '3' : "Geography",
          '4' : "History",
          '5' : "Entertainment",
          '6' : "Sports"}

  # GET '/questions'
  - Returns a list of  a list of questions, number of total questions, current category, categories
  - Questions are paginated in groups of 10 and ordered in descending order. Include a request argument to choose page number, starting from 1. 

  - Sample: 
      -Request: `curl http://127.0.0.1:5000/questions`
      -Response: 
        {"categories": {
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
            "answer": "Scarab", 
            "category": 4, 
            "difficulty": 4, 
            "id": 23, 
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
          }, 
          {
            "answer": "Blood", 
            "category": 1, 
            "difficulty": 4, 
            "id": 22, 
            "question": "Hematology is a branch of medicine involving the study of what?"
          }, 
          {
            "answer": "Alexander Fleming", 
            "category": 1, 
            "difficulty": 3, 
            "id": 21, 
            "question": "Who discovered penicillin?"
          }, 
          {
            "answer": "The Liver", 
            "category": 1, 
            "difficulty": 4, 
            "id": 20, 
            "question": "What is the heaviest organ in the human body?"
          }, 
          {
            "answer": "Jackson Pollock", 
            "category": 2, 
            "difficulty": 2, 
            "id": 19, 
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
          }, 
          {
            "answer": "One", 
            "category": 2, 
            "difficulty": 4, 
            "id": 18, 
            "question": "How many paintings did Van Gogh sell in his lifetime?"
          }, 
          {
            "answer": "Mona Lisa", 
            "category": 2, 
            "difficulty": 3, 
            "id": 17, 
            "question": "La Giaconda is better known as what?"
          }, 
          {
            "answer": "Escher", 
            "category": 2, 
            "difficulty": 1, 
            "id": 16, 
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
          }, 
          {
            "answer": "Agra", 
            "category": 3, 
            "difficulty": 2, 
            "id": 15, 
            "question": "The Taj Mahal is located in which Indian city?"
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


  # DELETE /question/{question_id}
  - Deletes a question using a question ID. if it exists. - Returns a list of questions after delete, number of total questions, current category, categories
  - Questions are paginated in groups of 10 and ordered in descending order. Include a request argument to choose page number, starting from 1. 
  - Sample: 
      -Request:
        `curl -X DELETE http://127.0.0.1:5000/questions/16?page=2`
      -Response:
          {
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
                "answer": "Agra",
                "category": 3,
                "difficulty": 2,
                "id": 15,
                "question": "The Taj Mahal is located in which Indian city?"
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
              },
              {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
              },
              {
                "answer": "Alexander Fleming",
                "category": 1,
                "difficulty": 3,
                "id": 21,
                "question": "Who discovered penicillin?"
              },
              {
                "answer": "Blood",
                "category": 1,
                "difficulty": 4,
                "id": 22,
                "question": "Hematology is a branch of medicine involving the study of what?"
              },
              {
                "answer": "Scarab",
                "category": 4,
                "difficulty": 4,
                "id": 23,
                "question": "Which dung beetle was worshipped by the ancient Egyptians?"
              }
            ],
            "success": true,
            "total_questions": 18
          }

  # POST /questions
  - Creates a new question which will require : 
        (question [string] ,  answer [string], category [int], difficulty score [int])
  - Returns success only.
  - Sample: 
      -Request:
        `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"testing question?","answer":"yes","difficulty":1,"category":1}'`
      -Response:
        {
          "success": true
        }

  # POST /question
  - Searches questions based on a search term. 
  - which will require : 
        (searchTerm [string])
  - Returns alist of questions related to ther search term and paginated in groups of 10 and ordered in descending order. Include a request argument to choose page number, starting from 1. 
  - Sample: 
      -Request:
          `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"dung"}'`
      -Response:
          {
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
                "answer": "Scarab", 
                "category": 4, 
                "difficulty": 4, 
                "id": 23, 
                "question": "Which dung beetle was worshipped by the ancient Egyptians?"
              }
            ], 
            "success": true, 
            "total_questions": 1
          }


  # GET /categories/{category_id}/questions
  - Searches questions based on a category. 
  - Request Arguments: category_id [int]
  - Returns alist of questions related to the selected category and paginated in groups of 10 and ordered in descending order. Include a request argument to choose page number, starting from 1. 
  - Sample: 
      -Request:
        `curl http://127.0.0.1:5000/categories/1/questions`
      -Response:
          {
          "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
          }, 
          "current_category": 1, 
          "questions": [
            {
              "answer": "The Liver", 
              "category": 1, 
              "difficulty": 4, 
              "id": 20, 
              "question": "What is the heaviest organ in the human body?"
            }, 
            {
              "answer": "Alexander Fleming", 
              "category": 1, 
              "difficulty": 3, 
              "id": 21, 
              "question": "Who discovered penicillin?"
            }, 
            {
              "answer": "Blood", 
              "category": 1, 
              "difficulty": 4, 
              "id": 22, 
              "question": "Hematology is a branch of medicine involving the study of what?"
            }
          ], 
          "success": true, 
          "total_questions": 3
        }
                

  # POST /quizzes
  - Get a question to play the quiz.
  - which will require : 
        -quiz_category [obj] : which can be {"type":"ALL","id":"0"} or any of the category list \
        -previous_questions  [array] : list of previously asked questions in the quiz
  - Returns an object of randomly selected question 
  - Sample: 
      -Request:
          `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}'`
      -Response:
        {
          "question": {
            "answer": "my answer", 
            "category": 1, 
            "difficulty": 1, 
            "id": 36, 
            "question": "test3"
          }, 
          "success": true, 
          "total_cat_questions": 6
        }
