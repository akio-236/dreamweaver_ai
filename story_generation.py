import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuration ---
PROMPT_FILE = "prompts.json"
# We use .jsonl (JSON Lines) because it's great for streaming data.
# Each line is a separate JSON object.
OUTPUT_FILE = "dataset.jsonl"
MODEL_NAME = "gemini-1.5-flash"  # Use a fast and capable model


def load_prompts(filename):
    """Loads the list of prompts from the specified JSON file."""
    print(f"Loading prompts from {filename}...")
    with open(filename, "r") as f:
        return json.load(f)


def main():
    """
    Main function to generate stories from prompts and save them to a dataset.
    """
    # --- API Setup ---
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(MODEL_NAME)

    prompts = load_prompts(PROMPT_FILE)

    print(f"Found {len(prompts)} prompts. Starting story generation...")

    # --- Story Generation Loop ---
    # We'll open the file in 'append' mode so we can add to it.
    # This way, if the script crashes, we don't lose our progress.
    with open(OUTPUT_FILE, "a") as f:
        for i, prompt in enumerate(prompts):
            print(f"--> Generating story {i + 1}/{len(prompts)}...")

            # This is our instruction template for the "Ghostwriter" AI.
            # It's a detailed prompt that tells the AI exactly what to do.
            request_to_ghostwriter = (
                "You are an obedient, creative author. Your task is to write a short story (between 500 and 1500 words) "
                "that perfectly and clearly incorporates all five of the following creative controls. "
                "The story must be coherent, well-written, and stay on topic. Do not repeat the controls in your response, just write the story.\n\n"
                "---\n"
                f"{prompt}"
            )

            try:
                # Make the API call
                response = model.generate_content(request_to_ghostwriter)

                # Create the JSON object for this entry
                story_text = response.text.strip()
                dataset_entry = {"prompt": prompt, "story": story_text}

                # Write the JSON object as a new line in our output file
                f.write(json.dumps(dataset_entry) + "\n")

                print(f"    ✅ Story {i + 1} generated and saved.")

            except Exception as e:
                # If something goes wrong, we log the error and continue.
                print(f"    🔴 ERROR generating story {i + 1}: {e}")

            # Be a good citizen and don't spam the API. A small delay helps.
            time.sleep(1)

    print(f"\n🎉 All done! Your dataset is ready in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
