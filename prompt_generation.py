import random
import json

# Idea Banks
genres = [
    "Science Fiction",
    "Fantasy",
    "Mystery",
    "Horror",
    "Romance",
    "Thriller",
    "Western",
    "Dystopian",
    "Cyberpunk",
    "Steampunk",
]

settings = [
    "a forgotten library on the Moon",
    "a bustling Victorian London market",
    "an underwater city powered by geothermal vents",
    "a sentient forest that rearranges itself at night",
    "a high-tech high school for cyborgs",
    "a derelict spaceship adrift in a nebula",
    "a magical university hidden within a volcano",
    "a post-apocalyptic city built from scrap metal",
    "a quiet teahouse in feudal Japan",
    "a jazz club in 1920s New Orleans",
]

characters = [
    "a timid chef who can talk to animals",
    "a retired starship captain haunted by their last mission",
    "a master thief who only steals memories",
    "a young sorcerer allergic to magic",
    "an android detective programmed with the personality of a film noir hero",
    "a lone botanist on a terraforming colony",
    "a street musician whose songs can alter reality",
    "a skeptical journalist investigating a haunted town",
    "a royal cartographer mapping a cursed land",
]

plot_elements = [
    "a mysterious map that only reveals itself in moonlight",
    "a broken compass that points to what the holder desires most",
    "a locked box that whispers secrets",
    "a rare flower that blooms only once a century",
    "an unexpected solar flare that disables all technology",
    "the discovery of an ancient, forgotten prophecy",
    "a message in a bottle from a parallel universe",
    "a recurring dream that starts to come true",
    "a secret society that controls the city from the shadows",
    "a peculiar pocket watch that can stop time for one minute",
]

tones = [
    "Humorous and witty",
    "Tense and suspenseful",
    "Melancholy and reflective",
    "Action-packed and fast-paced",
    "Hopeful and optimistic",
    "Dark and cynical",
    "Whimsical and magical",
    "Mysterious and eerie",
]


def generate_prompt():
    """
    Randomly combines elements from the idea banks to create a structured prompt.
    """
    genre = random.choice(genres)
    setting = random.choice(settings)
    character = random.choice(characters)
    plot_element = random.choice(plot_elements)
    tone = random.choice(tones)

    prompt = (
        "GENRE: " + genre + "\n"
        "SETTING: " + setting + "\n"
        "CHARACTER: " + character + "\n"
        "PLOT_ELEMENT: " + plot_element + "\n"
        "TONE: " + tone
    )
    return prompt


if __name__ == "__main__":
    # --- Configuration ---
    # Let's start with a small number to test.
    # You can increase this to 5000+ later.
    num_prompts_to_generate = 50
    output_file = "prompts.json"

    print(f"Generating {num_prompts_to_generate} prompts...")

    # Generate the list of prompts
    all_prompts = [generate_prompt() for _ in range(num_prompts_to_generate)]

    # Save the prompts to a JSON file

    with open(output_file, "w") as f:
        json.dump(all_prompts, f, indent=4)

    print(
        f"✅ Successfully generated and saved {len(all_prompts)} prompts to {output_file}"
    )
