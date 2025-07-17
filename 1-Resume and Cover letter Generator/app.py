import streamlit as st
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize Ollama LLM (Make sure Ollama and model like mistral is running)
llm = Ollama(model="mistral")

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert resume and cover letter generator."),
    ("human", "Generate resume bullet points, a summary, and a personalized cover letter using this data:\n\n"
     "Name: {name}\n"
     "Target Role: {role}\n"
     "Experience: {experience}\n"
     "Skills: {skills}\n"
     "Job Description: {jd}")
])

# Output parser
output_parser = StrOutputParser()

# Streamlit UI
st.title("🧠 Gen AI Resume & Cover Letter Generator (Ollama)")
st.write("Fill in the details below to generate tailored content:")

name = st.text_input("Your Name")
role = st.text_input("Target Role")
skills = st.text_area("Your Skills")
experience = st.text_area("Your Experience")
jd = st.text_area("Job Description (Paste from job portal)")

if st.button("Generate"): 
    if not all([name, role, skills, experience, jd]):
        st.warning("Please fill in all fields.")
    else:
        # Format and run the chain
        chain = prompt | llm | output_parser
        response = chain.invoke({
            "name": name,
            "role": role,
            "skills": skills,
            "experience": experience,
            "jd": jd
        })
        
        st.subheader("📝 Generated Content")
        st.text_area("Output", response, height=400)
        st.download_button("Download as .txt", response, file_name="generated_resume_cover_letter.txt")