# AI vs Human Art Classifier 🎨

A stunning, deep-learning-powered web app to distinguish between human-created art and AI-generated masterpieces.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```



2.  **Run the App:**
    Double-click `run_app.bat` in the folder.
    
    *Troubleshooting Info:*
    Because the project path is very long, a dedicated environment was created at `C:\Users\fazri\.gemini\art_check_env` to avoid Windows path limit errors. The `run_app.bat` file uses this environment automatically.

## Uploading to GitHub
To upload the project to GitHub, double-click `push_to_github.bat`.
**Note:** You must have [Git installed](https://git-scm.com/download/win) for this to work.


## Features
-   **Model Inspection**: Automatically loads `model.keras` or `model.h5`.
-   **Visuals**: Modern, dark-themed UI with glassmorphism effects.
-   **Input**: Supports both file upload and image URLs.
