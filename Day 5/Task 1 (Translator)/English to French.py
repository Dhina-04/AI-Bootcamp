import os
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import Runnable

# 🔐 Set your Gemini API key here
os.environ["GOOGLE_API_KEY"] = "AIzaSyDWp65oeNMIwckNs1128aHoD7Zvb2Axp_0"

# 🎯 Streamlit UI
st.set_page_config(page_title="English to French Translator", page_icon="🌍")
st.title("🌍 English to French Translator")
st.markdown("This app uses **Google Gemini via LangChain** to translate English text to French.")

# 📥 User input
english_text = st.text_input("Enter an English sentence:")

# 🔄 Button to trigger translation
if st.button("Translate to French"):
    if not english_text.strip():
        st.warning("Please enter a sentence before translating.")
    else:
        try:
            # 🧠 LLM setup
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

            # 🧾 Prompt template
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant that translates English to French."),
                ("user", "Translate this sentence: {text}")
            ])

            # 🔗 Chain: prompt | llm
            chain: Runnable = prompt | llm

            # 🧪 Run the chain
            response = chain.invoke({"text": english_text})

            # ✅ Display result
            st.success("Translation successful!")
            st.markdown(f"**French Translation:**\n\n> {response.content}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
