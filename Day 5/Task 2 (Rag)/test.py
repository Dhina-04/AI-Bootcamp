import os
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

import fitz  # PyMuPDF
import docx
from io import BytesIO

# 🔐 Set Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBXYiRFNbwvaVVrQMruUDHsvlGrQ5oPOLs"

# 🧠 Load Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

# 📄 Function to extract text from PDF
def extract_pdf_text(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# 📄 Function to extract text from DOCX
def extract_docx_text(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# 📄 Function to extract text based on file type
def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_pdf_text(uploaded_file)
    elif uploaded_file.name.endswith(".docx") or uploaded_file.name.endswith(".doc"):
        return extract_docx_text(uploaded_file)
    else:
        return None

# 🎨 Streamlit UI
st.set_page_config(page_title="📚 Ask Your Docs")
st.title("📚 Ask Questions from Your Document")
st.markdown("Upload a `.pdf` or `.docx` file, then ask a question based on its content using **Google Gemini AI**.")

uploaded_file = st.file_uploader("Upload your document", type=["pdf", "doc", "docx"])
user_question = st.text_input("Ask a question from the document:")

if st.button("Get Answer"):
    if not uploaded_file:
        st.warning("Please upload a document first.")
    elif not user_question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            # 📄 Extract document text
            document_text = extract_text(uploaded_file)
            if not document_text:
                st.error("Unsupported file format.")
            else:
                # 🧾 Prompt
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a document expert. Use the document content to answer the user's question."),
                    ("user", "Document:\n{document}\n\nQuestion:\n{question}")
                ])

                # 🔗 Chain: prompt | llm
                chain: Runnable = prompt | llm

                # 🚀 Run chain
                response = chain.invoke({
                    "document": document_text,
                    "question": user_question
                })

                st.success("Answer retrieved successfully!")
                st.markdown(f"**Answer:**\n\n{response.content}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
