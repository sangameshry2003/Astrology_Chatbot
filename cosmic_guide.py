import streamlit as st
from anthropic import Anthropic, APIError, APIConnectionError, BadRequestError
from datetime import datetime
import os

# Set up Anthropic API key (replace with your key)
try:
    anthropic = Anthropic(api_key="X")
except Exception as e:
    st.error(f"Error initializing Anthropic client: {e}")
    st.stop()

# Initialize session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def add_to_history(role, content):
    st.session_state.conversation_history.append({"role": role, "content": content})

def get_claude_response(prompt):
    try:
        messages = st.session_state.conversation_history + [{"role": "user", "content": prompt}]
        response = anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=messages,
            temperature=0.7
        )
        response_text = response.content[0].text.strip()
        add_to_history("assistant", response_text)
        return response_text
    except (BadRequestError, APIError, APIConnectionError) as e:
        return f"API Error: {e}"

# Function to get zodiac sign
def get_zodiac_sign(dob):
    return get_claude_response(f"Given the date of birth {dob}, what is the zodiac sign?")

def get_horoscope(zodiac_sign):
    return get_claude_response(f"Generate a daily horoscope for {zodiac_sign}.")

def check_compatibility(sign1, sign2):
    return get_claude_response(f"How compatible are {sign1} and {sign2}?")

def get_lucky_numbers_and_colors(zodiac_sign):
    return get_claude_response(f"What are today's lucky numbers and colors for {zodiac_sign}?")

def get_planetary_influences(zodiac_sign):
    return get_claude_response(f"How are current planetary movements affecting {zodiac_sign}?")

def get_love_life_predictions(zodiac_sign):
    return get_claude_response(f"What insights can you provide about love for {zodiac_sign}?")

def get_career_advice(zodiac_sign):
    return get_claude_response(f"What career advice do you have for {zodiac_sign}?")

def get_daily_affirmation(zodiac_sign):
    return get_claude_response(f"Create an empowering daily affirmation for {zodiac_sign}.")

def get_birthstone_and_element(zodiac_sign):
    return get_claude_response(f"What are the birthstone and element for {zodiac_sign}?")

# Streamlit UI
def astrology_chatbot():
    st.title("🔮 Astrology Chatbot")
    name = st.text_input("What's your name?")
    dob = st.text_input("Enter your date of birth (YYYY-MM-DD)")
    
    if st.button("Get My Zodiac Sign") and dob:
        try:
            datetime.strptime(dob, "%Y-%m-%d")
            zodiac_sign = get_zodiac_sign(dob)
            st.session_state["zodiac_sign"] = zodiac_sign
            st.success(f"Your zodiac sign has been identified: {zodiac_sign}!")
        except ValueError:
            st.error("Invalid date format. Use YYYY-MM-DD.")
    
    if "zodiac_sign" in st.session_state:
        zodiac_sign = st.session_state["zodiac_sign"]

        if st.button("📜 Daily Horoscope"):
            st.write(get_horoscope(zodiac_sign))
        if st.button("❤️ Love Life"):
            st.write(get_love_life_predictions(zodiac_sign))
        if st.button("💼 Career Advice"):
            st.write(get_career_advice(zodiac_sign))
        if st.button("🔢 Lucky Numbers & Colors"):
            st.write(get_lucky_numbers_and_colors(zodiac_sign))
        if st.button("🌌 Planetary Influences"):
            st.write(get_planetary_influences(zodiac_sign))
        if st.button("💎 Birthstone & Element"):
            st.write(get_birthstone_and_element(zodiac_sign))
        if st.button("🔮 Daily Affirmation"):
            st.write(get_daily_affirmation(zodiac_sign))
    
        st.subheader("💞 Compatibility Check")
        other_sign = st.text_input("Enter another zodiac sign to check compatibility")
        if st.button("Check Compatibility") and other_sign:
            st.write(check_compatibility(zodiac_sign, other_sign))
    
    st.subheader("💬 Ask a Custom Astrology Question")
    custom_question = st.text_area("Type your astrology-related question:")
    if st.button("Get Answer") and custom_question:
        st.write(get_claude_response(f"Answer this astrology question for {zodiac_sign}: {custom_question}"))

if __name__ == "__main__":
    astrology_chatbot()
