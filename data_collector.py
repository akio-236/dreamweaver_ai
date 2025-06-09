import os
import requests
from bs4 import BeautifulSoup
import re
import random

# Define a directory to save the text files
RAW_DATA_DIR = "data/raw stories"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Define a directory to save the processed text files
PROCESSED_DATA_DIR = "data/processed stories"
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

project_gutenberg_ids = [
    # Classic Children's Stories
    1635,  # The Adventures of Pinocchio by C. Collodi
    345,  # Alice's Adventures in Wonderland by Lewis Carroll
    74,  # The Adventures of Tom Sawyer by Mark Twain
    1112,  # The Wind in the Willows by Kenneth Grahame
    5200,  # The Wonderful Wizard of Oz by L. Frank Baum
    2139,  # The Secret Garden by Frances Hodgson Burnett
    360,  # Anne of Green Gables by L. M. Montgomery
    25344,  # Peter Pan by J. M. Barrie
    27838,  # The Tale of Peter Rabbit by Beatrix Potter
    36,  # A Little Princess by Frances Hodgson Burnett
    # More diverse/less common ones to add variety
    19706,  # Aesop's Fables
    1284,  # Grimm's Fairy Tales
    1342,  # Andersen's Fairy Tales
]


def download_gutenberg_text(gutenberg_id, output_dir):
    url = f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.txt"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        filepath = os.path.join(output_dir, f"{gutenberg_id}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Downloaded : {filepath}")
        return filepath
    except requests.exceptions.RequestException as e:
        print(f"Error dowloading {url}: {e}")
        return None


def clean_gutenberg_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Remove Project Gutenberg header
    start_match = re.search(
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*\*\*\*", text
    )
    if start_match:
        text = text[start_match.end() :]

    # Remove Project Gutenberg footer
    end_match = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK.*\*\*\*", text)
    if end_match:
        text = text[: end_match.start()]

    # Remove any remaining lines related to Project Gutenberg license/disclaimers
    text = re.sub(r"Project Gutenberg", "", text, flags=re.IGNORECASE)
    text = re.sub(r"http://www.gutenberg.org/.*", "", text)
    text = re.sub(
        r"\[This eBook is for the use of anyone anywhere.*\]", "", text, flags=re.DOTALL
    )
    text = re.sub(r"EBOOK STARTING WITH.*\n", "", text)

    # Text cleanup
    text = re.sub(r"\n\s*\n", "\n\n", text)  # Reduce multiple newlines
    text = re.sub(
        r"[\t ]+", " ", text
    )  # Replace multiple spaces/tabs with single space
    text = text.strip()

    return text


def split_into_stories(text, min_length_sentences=10, max_length_sentences=100):
    paragraphs = text.split("\n\n")
    stories = []
    current_story = []
    current_story_sentence_count = 0

    import nltk

    try:
        nltk.data.find("tokenizers/punkt")
    except nltk.downloader.DownloadError:
        nltk.download("punkt")

    for para in paragraphs:
        if not para.strip():
            continue

        sentences = nltk.sent_tokenize(para)
        sentence_count = len(sentences)

        if (
            current_story_sentence_count + sentence_count >= max_length_sentences
            and current_story
        ):
            stories.append("\n\n".join(current_story))
            current_story = []
            current_story_sentence_count = 0

        current_story.append(para)
        current_story_sentence_count += sentence_count

    if current_story:  # Add the last story
        stories.append("\n\n".join(current_story))

        filtered_stories = [
            s for s in stories if len(nltk.sent_tokenize(s)) >= min_length_sentences
        ]
        return filtered_stories


def save_processed_stories(stories_list, output_dir, original_id):
    for i, story_content in enumerate(stories_list):
        filepath = os.path.join(output_dir, f"story_{original_id}_{i + 1}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(story_content)
        print(f"Saved processed story: {filepath}")


if __name__ == "__main__":
    downloaded_files = []
    for pg_id in project_gutenberg_ids:
        filepath = download_gutenberg_text(pg_id, RAW_DATA_DIR)
        if filepath:
            downloaded_files.append(filepath)

    all_processed_stories = []
    for filepath in downloaded_files:
        print(f"\nProcessing {filepath}...")
        cleaned_text = clean_gutenberg_text(filepath)
        original_id = (
            os.path.basename(filepath).replace("gutenberg_", "").replace(".txt", "")
        )
        extracted_stories = split_into_stories(cleaned_text)
        save_processed_stories(extracted_stories, PROCESSED_DATA_DIR, original_id)
        all_processed_stories.extend(extracted_stories)

    combined_output_file = os.path.join(
        PROCESSED_DATA_DIR, "combined_children_stories.txt"
    )
    with open(combined_output_file, "w", encoding="utf-8") as f:
        for story in all_processed_stories:
            f.write(story)
            f.write("\n\n<ENDOFSTORY>\n\n")
    print(f"\nAll processed stories combined into: {combined_output_file}")
    print(f"Total stories processed: {len(all_processed_stories)}")
