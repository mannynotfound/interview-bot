from email.mime.text import MIMEText
from termcolor import colored
import markovify
import datetime
import smtplib
import random
import time
import json
import sys
import os

# Get model for prompts
with open('./model.json') as data_file:
    model = json.load(data_file)

# Get raw text as string.
with open("./words.txt") as f:
    text = f.read()

index = 0
transcript = {}
interviewer = ''
email = ''

bot_email = os.environ.get('INTERVIEW_BOT_EMAIL')
bot_email_password = os.environ.get('INTERVIEW_BOT_EMAIL_PASSWORD')
interviewee = os.environ.get('INTERVIEWEE')

def is_common_question(interview_question):
    q = interview_question.lower()
    answer = False

    for j in model['common']:
        hasQ = j in q
        # question is within 10 characters of common question
        closeEnough = len(q) <= (len(j) + 5) and len(q) >= (len(j) - 5)
        if hasQ and closeEnough:
            answer = str(model['common'][j])

    return answer

def respond(interview_question):
    global index
    global transcript
    answer = ''

    # get question words
    wordlist = interview_question.split()

    # check if actually a question
    if not wordlist[-1].endswith('?') and wordlist[-1] != '?':
        return 'Please, let\'s stick to questions only.'

    # check if already asked
    if (len(transcript) >= 1):
        for i in transcript:
            if (transcript[i]['question'].lower() == interview_question.lower()):
                return interviewer + ', please. You already asked me that.'

    # check if common question
    common = is_common_question(interview_question)
    if (type(common) is str):
        return common

    # Build the model.
    text_model = markovify.Text(text)

    # generate response
    for i in range(random.randint(1, 5)):
        answer += text_model.make_sentence()

    # save question + response
    # transcript[str(index)]['answer'] = nswer
    transcript.update({index: {
            'question': interview_question,
            'response': answer
        }})

    # increment index + return response
    index += 1
    return answer

def end_interview():
    print colored('Ok, ', 'red') + colored(interviewer, 'magenta') + colored(', thats enough questions for today. Thank you.', 'red')
    print colored('I\'ll send you an email of our conversation.', 'red')
    print ''

    message = ''

    for q in transcript:
        message += ('Question #' + str(q) + ': ')
        message += '\n'
        message += ('You asked: ' + transcript[q]['question'])
        message += '\n'
        message += ('I answered: ' + transcript[q]['response'])
        message += '\n'
        message += '\n'

    content = MIMEText(str(message))
    content['Subject'] = interviewer + ', here\'s the ' + interviewee + ' Interview from ' + str(datetime.date.today()) + ' | ' + time.strftime("%H:%M:%S")

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(bot_email, bot_email_password)
    s.sendmail(bot_email, email, content.as_string())
    s.close()

    sys.exit()

def question_loop():
    global index

    if index > len(model['prompts']) - 1:
        end_interview()
        return

    question_str = model['prompts'][index]
    interview_question = raw_input(colored(question_str, 'yellow'))
    response = respond(interview_question)
    print colored('-----------------------------', 'yellow')
    print (colored(response, 'white'))
    print ''

    time.sleep(1)
    question_loop()

def start_interview():
    global interviewer
    global email
    interviewer = raw_input(colored('Hey there!, whats your name? => ', 'yellow'))
    print ''
    email = raw_input(colored(interviewer, 'magenta') + colored(', Whats your email? I\'ll send a transcript of our interview => ', 'yellow'))
    print ''

    question_loop()

start_interview()
