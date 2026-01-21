# Flashcard Generation Instructions

This document outlines the process for generating Anki flashcards from the course materials. It should be read by the agent at the beginning of every session to ensure consistency.

## 1. Overall Workflow

The process is designed to be robust, stateful, and produce high-quality, formatted flashcards for import into Anki.

1.  **Initialization**: At the start of a session, read this file (`setup/instructions.md`), the `setup/flashcard_style_guide.md`, and the entire `setup/flashcards_master.csv` to load the current state.
2.  **Source Processing**: Process one `.txt` file from the `textfiles_for_searching/` directory at a time.
3.  **Card Generation**: For each piece of content in the source file, perform the following:
    a.  **Identify Potential Card**: Find a key concept, definition, code block, or other piece of information suitable for a flashcard.
    b.  **De-duplication**: Perform a semantic check against the `front` text of all cards in the loaded `flashcards_master.csv`. If a similar card already exists, discard the new one and move on.
    c.  **Content Creation**: Generate the raw `front` and `back` text for the card.
    d.  **Formatting**: Using the full context from the source text and the rules in `flashcard_style_guide.md`, create the final HTML-formatted `front_html` and `back_html`.
    a.  **ID Generation**: Generate a unique ID for each card using the format `YYYYMMDD-HHMM-SS-N` (e.g., `20240520-1430-15-1`).
    b.  **File Updates**:
        i.  Append the new, **raw** content (id, front, back, source_file, tags) to the `setup/flashcards_master.csv` file. 
        ii. **Data Integrity**: Ensure all CSV fields are double-quoted. Escape literal double quotes by doubling them (`""`).
        iii. Append the new, **HTML-formatted** content to the corresponding Anki export file (e.g., `anki_exports/week_1_logistic_regression.csv`).

## 2. Handling Imperfect Text Extractions

The source `.txt` files may contain garbled text from the PDF extraction process.

-   The agent's primary source of truth is the provided text. The agent should **not** invent content or try to guess the meaning of severely garbled text.
-   If a section of text is unreadable but seems to contain a potentially important concept, the agent should create a **placeholder card**.
-   **Placeholder Format**:
    -   **Front**: `[POTENTIALLY CORRUPTED CONTENT]`
    -   **Back**: "The source file `[source_file_name]` contains a section on `[inferred_topic]` that appears to be unreadable or corrupted. Please review the original PDF for this content."

## 3. File Structure

-   **`setup/instructions.md`**: This file.
-   **`setup/flashcard_style_guide.md`**: Defines the specific formatting rules (HTML structure, styling) for the Anki cards.
-   **`setup/flashcards_master.csv`**: The central database of all card *content* for de-duplication. Simple, raw text format.
-   **`anki_exports/`**: A directory containing the final, per-chapter/topic `.csv` files with rich HTML formatting, ready for Anki import.

## 4. Card Formatting and Styling

To ensure high-quality, readable, and consistent flashcards, the following tools and standards will be used.

-   **Styling (CSS)**: The visual appearance of the cards (colors, fonts, etc.) is defined in `setup/anki_styling.css`. The content of this file is to be manually copied into the Anki Note Type's styling section one time by the user.
-   **Formatting (HTML)**: All rich text formatting (bold, lists, tables) will be done using standard HTML tags.
-   **Code Blocks**: Code snippets will be formatted using `<pre><code class="hljs language-xyz">...</code></pre>` tags. This dual-class approach ensures compatibility with both standard CSS and Highlight.js. The agent will attempt to infer the correct language (e.g., 'python', 'bash', 'json') from the context. If the language is unknown, use `plaintext`.
-   **Diagrams (Mermaid.js)**: Diagrams will be generated using Mermaid.js syntax. The user must include the rendering script from `setup/anki_scripts.html` in their Anki card template. This ensures diagrams render correctly on all devices.
