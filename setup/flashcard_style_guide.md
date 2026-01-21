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

## 3. Card Back: The Answer

-   **Concise and Direct:** The back of the card should provide a direct and concise answer to the question on the front.
-   **Elaborate with Formatting:** Use the specific formatting rules below to structure the information for clarity and readability.
-   **Highlight Key Terms:** Use `<strong>` tags to emphasize the most critical terms in the answer.

## 4. Specific Formatting Rules

This section dictates how to use HTML to format the content on the back of a card.

-   **Definitions:**
    -   Place concise definitions inside a `<blockquote>`.
    -   **Example:** `<blockquote>A model that processes data in sequences, using its internal memory to remember previous inputs.</blockquote>`

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

## 5. Tagging Strategy

-   Tags are crucial for organizing cards in Anki.
-   The `tags` field in the master CSV should be a space-separated string.
- **Convention:** Include at least three types of tags:
    1.  **Week:** A tag for the week (e.g., `week-1`, `week-2`).
    2.  **Topic:** At least one tag for the specific chapter or topic (e.g., `logistic-regression`, `neural-networks`).
    3.  **Source:** A tag indicating the underlying source material if relevant (e.g., `lecture-slides`).
-   **Example:** `week-1 logistic-regression machine-learning gradient-descent`
