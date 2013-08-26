import os
# We import 'Flask' for creating a flask application,
# 'session' to store and retrieve session variables in every view
# 'render_template' to render a HTML template with the given context variables
# 'url_for' to get the URL corresponding to a view
# 'redirect' to redirect to a given URL
# 'request' to access the request object which contains the request data
# 'flash' to display messages in the template
from flask import Flask, session, render_template, url_for, redirect, request, flash


# Create a flask app and set its secret key

app = Flask(__name__)
app.secret_key = os.urandom(24)


# 'questions' dictionary contains 5 questions and their answers.
# The questions are numbered from 1 to 5

questions = { "1" : { "question" : "Which city is the capital of India?", "answer" : "New Delhi"},
              "2" : { "question" : "Who is the president of the USA?", "answer" : "Barack Obama" },
              "3" : { "question" : "Which is the world's highest mountain?", "answer" : "Mount Everest"},
              "4" : { "question" : "Which is the largest star of the solar system?", "answer" : "Sun"},
              "5" : { "question" : "How many days are there in a leap year?", "answer" : "366" } }



# Route for the URL / accepting GET and POST methods
# We are using session variables to keep track of the current question
# the user is in and show him just that question even if he reloads the page
# or opens the page in a new tab.
@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == "POST":
    
    # The data has been submitted from the form via POST request.
    # Now we need to validate it.
    
    entered_answer = request.form.get('answer', '')
    
    if not entered_answer:
      flash("Please enter an answer", "error") # Show error if no answer entered
      
    elif entered_answer != questions[session["current_question"]]["answer"]:
      # Show error if the answer is incorrect for the current question
      flash("The answer is incorrect. Try again", "error")
    
    else:
      # The answer is correct. So set the current question to the next number
      session["current_question"] = str(int(session["current_question"])+1)
    
      if session["current_question"] in questions:
        # If the question exists in the dictionary, redirect to the question
        redirect(url_for('index'))
      
      else:
        # else redirect to the success template as the quiz is complete.
        return render_template("success.html")
  
  if "current_question" not in session:
    # The first time the page is loaded, the current question is not set.
    # This means that the user has not started to quiz yet. So set the 
    # current question to question 1 and save it in the session.
    session["current_question"] = "1"
  
  elif session["current_question"] not in questions:
    # If the current question number is not available in the questions
    # dictionary, it means that the user has completed the quiz. So show
    # the success page.
    return render_template("success.html")
  
  # If the request is a GET request or the answer wasn't entered or the entered
  # answer is wrong, show the current questions with messages, if any.
  return render_template("quiz.html",
                         question=questions[session["current_question"]]["question"],
                         question_number=session["current_question"])

# Runs the app using the web server on port 80, the standard HTTP port
if __name__ == '__main__':
	app.run( 
        host="0.0.0.0",
        port=int("80")
  )