import json

INPUT_FILE = "data/raw/dataset.jsonl"
OUTPUT_FILE = "data/processed/cleaned_stories.jsonl"


def clean_story(story):
    if not story:
        return None

    story = story.strip()
    word_count = len(story.split())

    # Remove very short stories
    if word_count < 300:
        return None

    # Remove very long stories (optional)
    if word_count > 2000:
        return None

    # Remove obvious bad outputs
    bad_phrases = ["error", "sorry", "i cannot", "as an ai"]
    if any(phrase in story.lower() for phrase in bad_phrases):
        return None

    return story


def normalize_prompt(prompt):
    if not prompt:
        return None

    prompt = prompt.strip()

    # Standardize field names
    prompt = prompt.replace("Genre:", "GENRE:")
    prompt = prompt.replace("Setting:", "SETTING:")
    prompt = prompt.replace("Character:", "CHARACTER:")
    prompt = prompt.replace("Plot:", "PLOT:")
    prompt = prompt.replace("Tone:", "TONE:")

    return prompt


def main():
    cleaned_count = 0
    total_count = 0

    seen_stories = set()  # For duplicate removal
    lengths = []  # For stats

    with (
        open(INPUT_FILE, "r", encoding="utf-8") as infile,
        open(OUTPUT_FILE, "w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            total_count += 1

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            prompt = normalize_prompt(data.get("prompt"))
            story = clean_story(data.get("story"))

            # Skip invalid entries
            if not prompt or not story:
                continue

            # Remove duplicates (using hash for efficiency)
            story_hash = hash(story)
            if story_hash in seen_stories:
                continue

            seen_stories.add(story_hash)

            # Track length for stats
            lengths.append(len(story.split()))

            # Convert to training format
            formatted_data = {
                "messages": [
                    {"role": "system", "content": "You are a creative story writer."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": story},
                ]
            }

            json.dump(formatted_data, outfile, ensure_ascii=False)
            outfile.write("\n")

            cleaned_count += 1

    # Print stats
    print(f"Total samples: {total_count}")
    print(f"Cleaned samples: {cleaned_count}")

    if lengths:
        print(f"Average story length: {sum(lengths) / len(lengths):.2f} words")
        print(f"Min length: {min(lengths)} words")
        print(f"Max length: {max(lengths)} words")


if __name__ == "__main__":
    main()
