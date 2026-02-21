# Flashcard Style Guide

This document defines the rules for creating the content and structure of each flashcard. The agent must adhere to these rules to ensure all cards are effective, consistent, and well-formatted.

## 1. Core Philosophy: Atomicity

-   **One Concept Per Card:** Each flashcard should test only one single, atomic piece of information. Avoid creating cards that ask multiple questions or cover broad topics.
-   **Example:**
    -   **Bad:** "What are CNNs and RNNs and when are they used?"
    -   **Good:** "What is the primary use case for a Recurrent Neural Network (RNN)?"

## 2. Card Front: The Question

-   **Always a Question:** The front of every card must be phrased as a clear, specific question. This forces active recall rather than passive review.
-   **Clarity is Key:** Avoid ambiguous or overly complex questions. The user should know exactly what is being asked.
-   **No source framing:** Avoid phrasing like “in the slides/lecture” or “in the introduction.” Cards should read as general, exam-ready questions.
-   **Avoid trivial attribution:** Do not ask for definitions tied to a specific author/group unless the distinction itself is exam-relevant.

## 3. Card Back: The Answer

-   **Concise and Direct:** The back of the card should provide a direct and concise answer to the question on the front.
-   **Elaborate with Formatting:** Use the specific formatting rules below to structure the information for clarity and readability.
-   **Highlight Key Terms:** Use `<strong>` tags to emphasize the most critical terms in the answer.

## 4. Specific Formatting Rules

This section dictates how to use HTML to format the content on the back of a card.

-   **Structure & Flow**:
    -   **Detailed Structure**: Break down complex answers into bullet points (`<ul>`) or numbered lists (`<ol>`) whenever possible. Avoid large blocks of text.
    -   **Punctuation**:
        -   **No Trailing Periods**: Do NOT put a period at the end of any content that consists of a single sentence. This applies to **both** bullet points and standalone paragraphs.
        -   **Exception**: Use periods ONLY if a single bullet point or paragraph contains multiple sentences.
        -   **Formulas**: NEVER put a period after a mathematical formula.

-   **Quotes & Definitions**:
    -   **Use Sparingly**: Only use `<blockquote>` for verbatim definitions or critical, emphasized statements.
    -   **Don't Quote Everything**: Never wrap the entire answer in a blockquote. It loses its impact.
    -   **Example**: `<blockquote>Authentication is the process of verifying identity.</blockquote>`

-   **Mathematical Notation (LaTeX)**:
    -   Use `\(...\)` for inline expressions and `\[...\]` for display expressions.
    -   **CRITICAL**: Do NOT use `$...$` or `$$...$$`.
    -   **LaTeX Robustness**:
        -   Write LaTeX as **raw backslashes** (no escaping for CSV/JSON).
        -   Avoid sequences that can be interpreted as escapes (`\t`, `\f`, `\r`, `\n`) by keeping them inside valid LaTeX commands (e.g., `\text{...}`, `\frac{...}`, `\right`).
        -   Never emit double backslashes in the final field (e.g., `\\frac` or `\\(`).
        -   Use explicit LaTeX for spacing and text in math (`\text{...}`) so spaces render correctly.
        -   Prefer standard commands for structure (`\frac`, `\left...\right`, `\lvert...\rvert`) over ad‑hoc ASCII approximations.

-   **Lists:**
    -   Use `<ul>` for unordered (bulleted) lists.
    -   Use `<ol>` for ordered (numbered) lists, such as steps in a process.

-   **Comparisons:**
    -   When comparing and contrasting two or more items, use a `<table>`.
    -   Include a header row (`<thead>`) to label the columns.

-   **Code Snippets:**
    -   All code must be placed within `<pre><code class="hljs language-xyz">...</code></pre>`.
    -   The agent must infer the correct language (`python`, `bash`, `json`, etc.) and set it as the class. Use `hljs language-plaintext` if the language is unknown.

-   **Diagrams (Mermaid):**
    -   Diagrams should be generated using Mermaid syntax.
    -   The Mermaid script must be wrapped in a `<div class="mermaid">` tag.
    -   **Example:**
        ```html
        <div class="mermaid">
        graph TD;
            A[Input Layer] --> B(Hidden Layer);
            B --> C{Output Layer};
        </div>
        ```

-   **Legends (Abbreviations & Variables):**
    -   Creating a "legend" at the bottom of the card is **mandatory** if the card uses abbreviations or mathematical variables.
    -   **Placement**: Add a `<br><br>` separator after the main answer content.
    -   **Format**: Use a simple `<div>` with `class="legend"` (if available, otherwise plain div) containing lines for each term.
    -   **Structure**: `Term: Definition`. One per line. No bullet points.
    -   **Example**:
        ```html
        <br><br>
        <div>
        SSO: Single Sign-On<br>
        M: Probabilistic Matrix<br>
        r: Rank
        </div>
        ```

-   **Reasoning and Edge Cases:**
    -   Use `<ul>` to list conditions or consequences.
    -   **Example:**
        -   **Front:** "What happens to the Binary Cross-Entropy loss if the model predicts 0 but the ground truth is 1?"
        -   **Back:** "The loss approaches **infinity**" (followed by formula without period)

## 5. Tagging Strategy

-   Tags are crucial for organizing cards in Anki.
-   The `tags` field in both CSVs should be a space-separated string.
- **Convention:** Include at least four types of tags:
    1.  **Week:** A tag for the week (e.g., `week-1`, `week-2`).
    2.  **Topic:** At least one tag for the specific chapter or topic (e.g., `logistic-regression`, `neural-networks`).
    3.  **Category:** General category tags (e.g., `machine-learning`, `linear-algebra`).
    4.  **Source:** A tag indicating the source file using the format `source::filename` (e.g., `source::week-1-slides-l2-logreg`).
        - Convert the filename to lowercase and replace spaces/underscores with hyphens
        - Remove the `.txt` extension
-   **Example:** `week-1 logistic-regression machine-learning gradient-descent source::week-1-slides-l2-logreg`

