# Flashcard Generation Instructions

This document outlines the process for generating Anki flashcards from course materials. It should be read by the agent at the beginning of every session to ensure consistency.

## 1. Overall Workflow

The process is designed to be robust, stateful, and produce high-quality, formatted flashcards for import into Anki.

1.  **Initialization**: At the start of a session, read:
    - `shared/instructions.md` (this file)
    - `shared/flashcard_style_guide.md`
    - `[COURSE_FOLDER]/course_info.txt` - for course-specific metadata
    - `[COURSE_FOLDER]/flashcards_master.csv` - to load the current state for this course
2.  **Source Processing**: Process one `.txt` file from the `[COURSE_FOLDER]/slides/` directory at a time.
3.  **Card Generation**: For each piece of content in the source file, perform the following:
    a.  **Identify Potential Card**: Find a key concept, definition, code block, or other piece of information suitable for a flashcard.
    b.  **De-duplication**: Perform a semantic check against the `front` text of all cards in the loaded `flashcards_master.csv`. If a similar card already exists, discard the new one and move on.
    c.  **Content Creation**: Generate the raw `front` and `back` text for the card.
    d.  **Formatting**: Using the full context from the source text and the rules in `flashcard_style_guide.md`, create the final HTML-formatted `front_html` and `back_html`.
    a.  **ID Generation**: Generate a unique ID for each card using the format `YYYYMMDD-HHMM-SS-N` (e.g., `20240520-1430-15-1`).
    b.  **Tag Generation**: Create a space-separated tag string that includes:
        - Week tag (e.g., `week-1`)
        - Semester tag from `[COURSE_FOLDER]/course_info.txt` (e.g., `winter-2025-2026`)
        - Topic tags (e.g., `logistic-regression`, `machine-learning`)
        - Source file tag using the format `source::filename` (e.g., `source::week-1-slides-l2-logreg`)
        - **Example**: `week-1 winter-2025-2026 logistic-regression machine-learning source::week-1-slides-l2-logreg`
    c.  **File Updates**:
        i.  Append the new, **raw** content (id, front, back, source_file, tags) to the `[COURSE_FOLDER]/flashcards_master.csv` file. 
        ii. **Data Integrity**: Ensure all CSV fields are double-quoted. Escape literal double quotes by doubling them (`""`).
        iii. Append the new, **HTML-formatted** content (front_html, back_html, tags) to the corresponding Anki export file (e.g., `[COURSE_FOLDER]/anki_exports/week_1_logistic_regression.csv`).
            - **IMPORTANT**: Anki export files should have ONLY 3 columns: `front_html`, `back_html`, `tags`
            - Do NOT include `id` or `source_file` columns in Anki exports
            - Do NOT include a header row in Anki export files (Anki doesn't expect it)
            - The source file information is embedded in the tags as `source::filename`

## 2. Handling Imperfect Text Extractions

The source `.txt` files may contain garbled text from the PDF extraction process.

-   The agent's primary source of truth is the provided text. The agent should **not** invent content or try to guess the meaning of severely garbled text.
-   If a section of text is unreadable but seems to contain a potentially important concept, the agent should create a **placeholder card**.
-   **Placeholder Format**:
    -   **Front**: `[POTENTIALLY CORRUPTED CONTENT]`
    -   **Back**: "The source file `[source_file_name]` contains a section on `[inferred_topic]` that appears to be unreadable or corrupted. Please review the original PDF for this content."

## 3. File Structure

-   **`shared/`**: Common resources used across all courses
    -   `instructions.md`: This file - core instructions (course-agnostic)
    -   `flashcard_style_guide.md`: Formatting and style rules
    -   `anki_styling.css`: CSS for Anki cards (copy to Anki Note Type once)
    -   `session_prompt_template.txt`: Template for starting sessions

-   **`[COURSE_FOLDER]/`**: Course-specific folder (e.g., `deep-learning/`)
    -   `course_info.txt`: Course metadata with format:
        ```
        course_name: Deep Learning
        semester: winter-2025-2026
        ```
    -   `flashcards_master.csv`: Master database for this course only
        - **Format**: `id,front,back,source_file,tags` (5 columns)
        - **Purpose**: Internal tracking and de-duplication within this course
    -   `slides/`: Source lecture slides for this course
    -   `anki_exports/`: Anki-ready CSV files for this course
        - **Format**: `front_html,back_html,tags` (3 columns only, **no header row**)
        - **Purpose**: Direct import into Anki
        - **Note**: Source file information is embedded in tags as `source::filename`

## 4. Card Formatting and Styling

To ensure high-quality, readable, and consistent flashcards, the following tools and standards will be used.

-   **Styling (CSS)**: The visual appearance of the cards (colors, fonts, etc.) is defined in `setup/anki_styling.css`. The content of this file is to be manually copied into the Anki Note Type's styling section one time by the user.
-   **Formatting (HTML)**: All rich text formatting (bold, lists, tables) will be done using standard HTML tags.
-   **Mathematical Notation (LaTeX)**: Use Anki's LaTeX delimiters for mathematical expressions:
    - **Inline math**: Use `\(...\)` for inline expressions (e.g., `\(x^2 + y^2\)`)
    - **Display math**: Use `\[...\]` for display/block expressions (e.g., `\[\sum_{i=1}^{n} x_i\]`)
    - **CRITICAL**: Do NOT use `$...$` or `$$...$$` - these will not render in Anki
    - **Example**: `\(f(x) = w \cdot x + b\)` for inline, `\[\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}\]` for display
-   **Code Blocks**: Code snippets will be formatted using `<pre><code class="hljs language-xyz">...</code></pre>` tags. This dual-class approach ensures compatibility with both standard CSS and Highlight.js. The agent will attempt to infer the correct language (e.g., 'python', 'bash', 'json') from the context. If the language is unknown, use `plaintext`.
-   **Diagrams (Mermaid.js)**: Diagrams will be generated using Mermaid.js syntax. The user must include the rendering script from `setup/anki_scripts.html` in their Anki card template. This ensures diagrams render correctly on all devices.
## 5. "Exam-Ready" Content Principles

To ensure cards are sufficient for exam preparation (especially when the user only reads slides once), follow these additional rules:

-   **Derivations**: Don't just provide the final formula. Create cards for the **key logical steps** or assumptions in a derivation (e.g., "Why can we pull $P(Y_0)$ out of the summation over $Y_1, \dots, Y_n$?").
-   **Visual/Intuitive Understanding**: Create cards that describe or ask about the **shape** of functions (sigmoid, loss curves).
    -   *Example*: "What happens to the logistic sigmoid curve as the scaling factor $c$ increases?" 
    -   *Answer*: "The transition from 0 to 1 becomes **steeper**, eventually approaching a step function."
-   **Edge Cases & Limits**: Always include cards for the behavior of functions at $0, \infty, -\infty$.
-   **Qualitative Reasoning**: Include cards about **uncertainty** and **confidence** based on model outputs.
-   **Inter-theory Connections**: Ask about the *relationship* between concepts (e.g., "What is the connection between Maximum Likelihood and Cross-Entropy?").
-   **Comparison Cards**: Always compare different approaches mentioned in the slides (e.g., "Logistic vs. Probit").

## 6. Course Folder Discovery

To simplify the user's workflow, the agent should be able to identify the `[COURSE_FOLDER]` automatically based on the provided slide file path.

-   **Extraction**: If the user provides a path like `/absolute/path/to/flashcards/course-name/slides/week-2-slides.txt`, the `[COURSE_FOLDER]` is the parent of the `slides/` directory (in this case, `/absolute/path/to/flashcards/course-name/`).
-   **Validation**: After inferring the `[COURSE_FOLDER]`, the agent must verify that it contains the required `course_info.txt` and `flashcards_master.csv` before proceeding.
-   **Fallback**: If the folder structure does not follow this convention, the agent should ask the user to explicitly provide the course folder path.
