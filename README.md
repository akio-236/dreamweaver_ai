Dreamweaver AI

An instruction following AI that transforms a user's creative vision of genre, setting, character, plot, and tone—into a complete, original short story.

## 🚀 Project Status

**Built:** The 5,000+ prompt/story synthetic dataset (Phases 0 and 1 complete).

**Planned:** GPT-2 fine-tuning, a FastAPI interface, and evaluation.

## About The Project

The Dreamweaver AI is an instruction-following narrative generator. Its core purpose is to empower user creativity by transforming a structured set of creative ideas into a fully formed, coherent short story. The user acts as the "director," providing the high level vision, and the AI acts as the "obedient author," executing that vision with creative flair.

The plan is to fine-tune a `gpt2-medium` model on the custom, synthetically generated dataset.



## 🛠️ Tools & Technologies

* **AI Development:** `Python`, `PyTorch`, `Hugging Face (transformers, datasets)`, `GPT-2`, `Google Gemini API`
* **Web Application:** `FastAPI`, `HTML`, `CSS`, `JavaScript`
* **Version Control:** `Git`, `GitHub`, `Git LFS`

## 🗺️ Project Roadmap

This project is being executed in five distinct phases.

* **✅ Phase 0: Environment Setup & Preparation**
    * **Status:** Complete
    * **Summary:** Set up the local Python environment, created the GitHub repository, and established a secure connection to the Google Gemini API for data generation.

* **✅ Phase 1: Synthetic Dataset Generation**
    * **Status:** Complete
    * **Summary:** Developed scripts to programmatically generate 5,000+ unique creative prompts and use a "Ghostwriter" LLM to generate corresponding stories. The final dataset has been created and is tracked using Git LFS.

* **➡️ Phase 2: Model Fine-Tuning (Next Up)**
    * **Objective:** To teach the GPT-2 model the specific skill of being an "Obedient Author." This involves writing and running the training script on a GPU using our custom dataset.

* **➡️ Phase 3: Application Interface & Deployment**
    * **Objective:** Create a web application for users to interact with the model. This includes building a FastAPI backend and a simple HTML/CSS/JS frontend.

* **➡️ Phase 4: Evaluation & Refinement**
    * **Objective:** Test the model's performance by providing a diverse range of prompts and analyzing its ability to follow instructions, maintain coherence, and adhere to the specified tone.

## ⚙️ Setup & Usage

To get a local copy up and running, follow these steps.

### Prerequisites

* Python 3.8+
* Git
* [Git LFS](https://git-lfs.github.com/)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/akio-236/dreamweaver_ai.git
    cd dreamweaver_ai
    ```

2.  **Download the large data files:**
    ```sh
    git lfs pull
    ```

3.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

5.  **Set up your environment variables:**
    * Create a file named `.env` in the root of the project.
    * Add your API key to it:
        ```env
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```
