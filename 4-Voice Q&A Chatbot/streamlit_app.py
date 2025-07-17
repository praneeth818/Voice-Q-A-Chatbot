import streamlit as st
import speech_recognition as sr
import pyttsx3
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Set up Text-to-Speech (TTS)
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Step 2: Record voice from microphone and convert to text
def listen_to_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info(" Please speak your question...")
        audio = recognizer.listen(source)
    try:
        # Convert speech to text using Google Speech Recognition
        question = recognizer.recognize_google(audio)
        st.success(f" You said: {question}")
        return question
    except sr.UnknownValueError:
        st.error(" Could not understand what you said.")
    except sr.RequestError:
        st.error(" Failed to connect to the speech recognition service.")
    return ""

# Step 3: Set up Local LLM using Ollama (e.g., mistral)
llm = Ollama(model="mistral")  

# Step 4: Define the prompt format for the AI
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])

# Step 5: Create a chain to process the input and get output
chain = prompt | llm | StrOutputParser()

# Step 6: Build the Streamlit UI
st.title(" Voice GenAI Chatbot")
st.markdown("Click the button, speak your question, and get an AI-powered answer.")

if st.button(" Ask a Question"):
    user_question = listen_to_voice()
    
    if user_question:
        # Step 7: Send question to LLM and get response
        with st.spinner(" Generating answer..."):
            ai_answer = chain.invoke({"question": user_question})

        # Step 8: Show and speak the answer
        st.success(" AI Answer:")
        st.write(ai_answer)
        speak(ai_answer)
