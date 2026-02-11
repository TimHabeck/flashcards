# Flashcard Generation Instructions

This document outlines the workflow and core principles for generating exam-ready Anki flashcards. It acts as the "Controller" for the flashcard generation process.

## 1. Overall Workflow

The agent follows this loop for every source file:

1.  **Initialization**: Read `instructions/flashcard_style_guide.md`, `[COURSE_FOLDER]/course_info.txt`, and load `flashcards_master.csv`.
2.  **Source Processing**: Read one `.txt` file from `slides/`.
3.  **Card Generation**:
    a.  **Identify Concept**: Select an exam-relevant topic.
    b.  **De-duplication**: Check `flashcards_master.csv` (Front column) to avoid duplicates.
    c.  **Draft Content**: Create the raw Question and Answer text.
    d.  **Apply Formatting**: Use `instructions/flashcard_style_guide.md` to format the content (HTML/LaTeX).
    e.  **Generate ID & Tags**: Create unique ID and tags (including `source::filename`).
4.  **Saving Data**:
    a.  **Append to Master CSV**: Add `id,front,back,source_file,tags` to `flashcards_master.csv`.
        -   *Crucial*: Double-quote all fields. Escape literal quotes as `""`.
    b.  **Append to Anki Export CSV**: Add `front_html,back_html,tags` to `anki_exports/[week_file].csv`.
        -   *Crucial*: NO Header row. ONLY 3 columns.

## 2. Content Principles ("Exam-Ready")

These rules ensure the **content** (not format) is high quality:

-   **Derivations**: Don't just show formulas. Ask about logical steps and assumptions.
-   **Visual Intuition**: Ask about the *shape* and behavior of functions (e.g., "What happens as $x \to \infty$?").
-   **Relationships**: Connect concepts (e.g., "Compare X vs Y").
-   **Uncertainty**: Include questions about model confidence and limitations.
-   **Context**: 
    -   **Avoid Source References**: Don't say "In the slides...".
    -   **Ensure Topic Context**: The question MUST clearly state the topic it refers to. A card like "What are the 3 types?" is invalid; it must be "What are the 3 types of **access control**?".

## 3. Formatting Standards

All visual formatting is governed by **`instructions/flashcard_style_guide.md`**.

-   **Refer to the Style Guide for:**
    -   Detailed HTML structure (Lists, Tables)
    -   Exact LaTeX syntax (`\(...\)`)
    -   Code block classes (`hljs`)
    -   Mermaid diagrams
    -   Mandatory Legends (Abbreviations)
-   **CSS**: The visual theme is defined in `instructions/anki_styling.css`.

## 4. Handling Imperfect Text

-   **Truth**: Do not invent content if text is garbled.
-   **Placeholder**: If a key section is unreadable, create a placeholder card:
    -   **Front**: `[POTENTIALLY CORRUPTED CONTENT]`
    -   **Back**: "The source file `[filename]` contains unreadable text on `[topic]`. Please check PDF."

## 5. File & Folder Logic

-   **Folder Structure**:
    -   All course folders are located in `[PROJECT_ROOT]/courses/`.
    -   Example: `flashcards/courses/deep-learning/`
-   **Course Folder Discovery**:
    -   Infer `[COURSE_FOLDER]` from the slide path (e.g., if slide is in `.../courses/deep-learning/slides/`, then course folder is `.../courses/deep-learning`).
    -   Verify using `course_info.txt`.
-   **Path Handling**:
    -   Use absolute paths for all file operations.
    -   Convert filenames to lowercase/hyphenated for `source::...` tags.
