# interview-bot

A simple python script to automatically give interviews.

# inspo

Interviews suck, but are a necessary evil. Let's automate them. The idea is to use
markov chain + NLP to formulate meaningful responses to an interviewer's questions.

# usage

have the interviewer run `python interview.py` (or better yet, alias it for them) and 
an interactive shell prompt will take over. After receiving the users name and email (to send a log to),
the interviewer can ask questions and receive computer generated responses from a sample text provided
by the interviewee. In this way, the interviewee can spit out their thoughts as a stream of words and ideas
and have the computer do the tedious task of delivering them to the interviewer.

# features

* markov chain sentence construction with configurable sentence length
* "common questions" responses
* repeat question detection
* non question detection
* custom question prompts to keep the interview going + limit amount of questions
* automatically email a copy of the interview to both parties for record.
