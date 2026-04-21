import json

INPUT_FILE = "data/raw/dataset.jsonl"
OUTPUT_FILE = "data/processed/cleaned_stories.jsonl"


def clean_story(story):
    if not story:
        return None

    word_count = len(story.split())

    # Remove very short stories
    if word_count < 300:
        return None

    # Remove extremely long (optional)
    if word_count > 2000:
        return None

    # Remove obvious bad outputs
    bad_phrases = ["error", "sorry", "i cannot", "as an ai"]
    if any(phrase in story.lower() for phrase in bad_phrases):
        return None

    return story.strip()


def main():
    cleaned_count = 0
    total_count = 0

    with (
        open(INPUT_FILE, "r", encoding="utf-8") as infile,
        open(OUTPUT_FILE, "w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            total_count += 1
            data = json.loads(line)

            prompt = data.get("prompt")
            story = clean_story(data.get("story"))

            if story:
                json.dump({"prompt": prompt, "story": story}, outfile)
                outfile.write("\n")
                cleaned_count += 1

    print(f"Total: {total_count}")
    print(f"Cleaned: {cleaned_count}")


if __name__ == "__main__":
    main()
