import os
import google.generativeai as genai
from dotenv import load_dotenv


def test_api_connection():
    """
    Loads the Gemini API key from the .env file and tests the connection
    by listing available models.
    """
    print("--- Starting API Connection Test ---")

    try:
        # Load environment variables from .env file
        load_dotenv()

        # Get the API key from the environment variables
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("🔴 ERROR: GEMINI_API_KEY not found in .env file.")
            print(
                "Please make sure you have a .env file with GEMINI_API_KEY='your_key'"
            )
            return

        print("✅ API Key loaded successfully.")

        # Configure the generative AI client
        genai.configure(api_key=api_key)
        print("✅ Google Generative AI configured.")

        # Test the connection by listing models
        print("⏳ Listing available models...")
        model_count = 0
        for model in genai.list_models():
            if "generateContent" in model.supported_generation_methods:
                model_count += 1

        if model_count > 0:
            print(f"✅ Success! Found {model_count} compatible models.")
            print("--- API Connection Test Passed ---")
        else:
            print(
                "🟡 WARNING: Could not find any compatible models, but the connection was successful."
            )

    except Exception as e:
        print(f"🔴 ERROR: An exception occurred during the API test: {e}")
        print("--- API Connection Test Failed ---")


if __name__ == "__main__":
    test_api_connection()
