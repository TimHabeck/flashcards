# Flashcard Style Guide

This document defines the rules for creating the content and structure of each flashcard. The agent must adhere to these rules to ensure all cards are effective, consistent, and well-formatted.

## 1. Core Philosophy: Atomicity & Clarity

-   **One Concept Per Card:** Each flashcard should test only one single, atomic piece of information.
-   **Clear Questions:** The front must be a clear, unambiguous question.
-   **Self-Contained Context:** Ensure the question includes all necessary context (e.g., "What is the disadvantage **of symmetric encryption**?"). Do not rely on the user knowing which chapter they are currently studying.
-   **No Source Framing:** Do not reference "slides", "lectures", or specific authors in the question unless essential to the exam content.

## 2. Text Structure & Formatting

This section controls the layout and flow of the answer (Card Back).

### Layout & Lists
-   **Avoid Walls of Text**: Break down complex answers into structured lists.
-   **Unordered Lists**: Use `<ul>` for bullet points.
-   **Ordered Lists**: Use `<ol>` for sequential steps.
-   **Comparisons**: Use `<table>` with a `<thead>` row for comparing items.

### Punctuation Rules (CRITICAL)
-   **No Trailing Periods**: Do NOT put a period at the end of any content that consists of a single sentence. This applies to **both** bullet points and standalone paragraphs.
-   **Exception**: Use periods ONLY if a single bullet point or paragraph contains multiple full sentences.
-   **Formulas**: NEVER put a period after a mathematical formula.

### Quotes & Emphasis
-   **Quotes (`<blockquote>`)**: Use **sparingly**. Only for verbatim definitions or critical statements. **Never** wrap the entire answer in a blockquote.
-   **Emphasis (`<strong>`)**: Use to highlight the most critical terms or keywords in the answer.

## 3. Technical Elements & Syntax

### Mathematical Notation (LaTeX)
-   **Syntax**: Use `\(...\)` for inline and `\[...\]` for display text. **NEVER** use `$` or `$$`.
-   **Robustness**:
    -   Write raw backslashes (e.g., `\frac`, not `\\frac`).
    -   Avoid control characters (`\t`, `\n`) inside formulas.
    -   Use `\text{...}` for text inside math modes.

### Code Snippets
-   **Format**: Wrap in `<pre><code class="hljs language-xyz">...</code></pre>`.
-   **Language**: Infer the correct language (e.g., `python`, `cpp`) for the class. Use `language-plaintext` if unknown.

### Diagrams (Mermaid)
-   **Format**: Wrap Mermaid syntax in `<div class="mermaid">...</div>`.

## 4. Mandatory Footer: The Legend

If the card uses **abbreviations** or **mathematical variables**, you MUST include a legend at the bottom.

-   **Separator**: Add `<br><br>` after the main answer.
-   **Container**: Use `<div class="legend">` (relies on `anki_styling.css`).
-   **Format**: One definition per line. `Term: Definition`.
-   **Example**:
    ```html
    <br><br>
    <div class="legend">
    SSO: Single Sign-On<br>
    M: Probabilistic Matrix<br>
    r: Rank
    </div>
    ```

## 5. Tagging Strategy

-   **Format**: Space-separated string.
-   **Required Tags**:
    1.  **Week**: `week-X`
    2.  **Topic**: `topic-name`
    3.  **Category**: `general-category`
    4.  **Source**: `source::filename` (lowercase, no extension, spaces->hyphens)
