from logging import debug
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    
    return render_template("start.html")

@app.route('/questions/<int:qid>')
def handle_question(qid):
   
    if qid == len(responses):
        question_num = qid + 1
        question = survey.questions[qid].question
        choices = survey.questions[qid].choices
        return render_template("question.html", question=question, num=question_num, choices=choices)
    else: 
        flash("Trying to access an invalid question", 'error')
        return redirect(f"/questions/{len(responses)}")
    

@app.route('/answer', methods=['POST'])
def handle_answer():
    """Appends answer to responses list and then redirects to next question"""
    answer = request.form["answer"]
    responses.append(answer)

    # print(responses)

    if len(responses) < 4:
        return redirect(f"/questions/{len(responses)}")
    elif len(responses) == len(survey.questions):
        return redirect("/complete")
    elif len(responses) == 0:
        return redirect("/")

@app.route("/complete")
def finish_survey():
    """Directs user to ending page"""

    return render_template("complete.html")