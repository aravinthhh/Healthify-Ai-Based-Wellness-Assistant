import google.generativeai as genai
import os
import streamlit as st
import pandas as pd

api = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = api)

model = genai.GenerativeModel('gemini-2.5-flash-lite')


#Create Title
st.title(':yellow[Healthify] - :blue[AI Powered Personel Health Assistant]')
st.markdown('''##### This application will assist yoy to have a better and healthify life. You can ask your health related question and get personalized advice.''')
tips = '''Follow the Steps
* Enter the details in the sidebar.
* Enter your gender, age, height (cms), weight(kgs).
* Select the number on the fitness scale (0-5).  [5 - Fit and 0 - Not Fit]
* After filling the details, write your query here and get customised response.'''

st.write(tips)

#Create Sidebar
st.sidebar.header(':orange[Enter Your Details]')
name = st.sidebar.text_input('Enter your name')
gender = st.sidebar.selectbox('Select your Gender', ['Male','Female','Other']) 
age = st.sidebar.text_input('Enter your age in years')
smoking = st.sidebar.selectbox('Smoking Habit', ['Yes','No'])
alcohol = st.sidebar.selectbox('Drinking Habit', ['Yes','No'])
weight = st.sidebar.text_input('Enter your weight in kgs')
height = st.sidebar.text_input('Enter your height in cms')

bmi = pd.to_numeric(weight)/(pd.to_numeric(height)/100)**2

fitness = st.sidebar.slider('Rate your Fitness between 0-5', 0 , 5, step=1)

st.sidebar.write(f'{name} your BMI: {round(bmi,2)} Kg/m^2')

#Using GenAi model to get the output
user_query = st.text_input('Enter your question here')

prompt = f'''Assume you are a health and diet expert. 
You are requried to answered the question asked by the user.
Use the following details provided by the user. 
name of the user is {name}
gender is {gender}
age is {age}
smoker is {smoking}
drinking alcohol is {alcohol}
weight is {weight}
height is {height}
bmi is {bmi} kg/m^2
and user rates his/her fittness as {fitness} out of 5

Your output should be in the following format 
* It should start by giving one or two line comment on the details that have been given by user.
* It should explain what the real problem is based on the query asked by the use.
* What could be the possible reason for the problem.
* What are the possible solutions for the problem.
* You can also mention which doctor should the user consult (specialization) if required.
* Suggest whether the user must quit few habits for a better life.
* Suggest a diet plan to the user as per the details and query provided by the user, this can be in a table. 
* Strictly don not recommend or advise any medication, even if it is been asked by user.
* output should be in both paragraph, bullet point and use tables wherever it is required.

here is the query from the user{user_query} '''


if user_query:
    response = model.generate_content(prompt)
    st.write(response.text)