# Trivia-Text-Analytics
Text Topic Clustering to Determine Topics to Study for Jeopardy Trivia 
Jeopardy Clustering Project Proposal: Blue Team 10
Jonah Schiestle, Levi Lovell, Sarah Ocampo, Mark Senay, and Sarah Stephens

Problem Statement:
New Jeopardy contestants have an extensive list of previous question categories that they could study in order to prepare to be on the show. Our team seeks to reclassify the “category” of each question with a new “subject” that is more general using clustering techniques (i.e., based on word/phrase frequency in Jeopardy questions). Using our analysis, contestants will be able to focus their preparation on the most frequent and highest value subjects.  

Questions our team seeks to answer:
Our team plans to answer the following questions:
Is it possible to reclassify categories more generally using a clustering analysis based on text similarity?
What is the optimal way to win the show? 
Which subjects (reclassified) tend to show up most frequently?
What kinds of questions (i.e., short vs long or by subject) tend to be assigned the highest value?
How have Jeopardy questions changed over time? 
Have questions become more difficult? More lengthy?

Dataset Description: 
The data set contains 216,930 Jeopardy questions, answers and other descriptors. The JSON file is an unordered list of questions where each question has the following information:
'category': the question category, e.g. "HISTORY"
'value': $ value of the question as string, e.g. "$200" ("None" for Final Jeopardy/Tiebreaker questions)
'question': text of question (Hyperlinks and messy text when there's a picture or video question)
'answer': text of answer
'round': one of "Jeopardy!","Double Jeopardy!","Final Jeopardy!" or "Tiebreaker"
Note: Tiebreaker questions do happen but they're very rare (like once every 20 years)
'show_number': string of show number, e.g '4680'
'air_date': the show air date in format YYYY-MM-DD
 
Types of Analysis: 
We plan to utilize one or more of the following types of analysis: text representation, frequency analysis, and/or clustering. 

Why Data Supports Problem:
The data contain the questions, answers, categories, and dates they were asked. With this information we can look at patterns over time and patterns within categories. The provided categories are often ambiguous and written to be entertaining. The text provided in the ‘question’ field provides the potential to classify questions within broader subjects as a more efficient way for contestants to evaluate their own knowledge. 

Challenges:
We might encounter some difficulty cleaning the data, particularly the questions with video or image questions. Additionally, we may not be able to identify a logical clustering of the questions (i.e., for reclassification of subjects).

Deliverables:
Upon completion, we will create the following deliverables:
Frequency of subjects over the years
Breakdown of question value by subject and analyze question complexity by question value
Description of patterns in Final Jeopardy questions
