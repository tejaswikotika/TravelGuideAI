import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Generation settings (as portal style)
generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize model (using available model)
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    generation_config=generation_config,
)

# Function to generate travel itinerary
def generate_itinerary(destination, days, nights):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Write me a travel itinerary to {destination} for {days} days and {nights} nights."
                ],
            }
        ]
    )

    response = chat_session.send_message(
        f"Create a detailed travel itinerary for {days} days and {nights} nights in {destination}."
    )

    return response.text

# Streamlit App
def main():
    st.title("Travel Itinerary Generator")

    destination = st.text_input("Enter your desired destination:")
    days = st.number_input("Enter the number of days:", min_value=1)
    nights = st.number_input("Enter the number of nights:", min_value=0)

    if st.button("Generate Itinerary"):
        if destination.strip() and days > 0 and nights >= 0:
            try:
                itinerary = generate_itinerary(destination, days, nights)
                st.text_area("Generated Itinerary:", value=itinerary, height=300)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please make sure all inputs are provided and valid.")

if __name__ == "__main__":
    main()