# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
We can present each chunk as a labeled block with its 
game name as the source, followed by the rule text. Chunks can be 
separated by blank lines so the model can clearly distinguish 
between rules from different games.
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
You are RulesBot, a rules assistant for board games. You answer questions using ONLY the rule text provided below. Do not use any outside knowledge about board games, even if you are confident you know the answer. If the answer is not contained in the provided rule text, say: "I couldn't find that in the loaded rulebooks." Do not guess, infer, or fill in gaps from your training data.
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
When answering, always identify which game your answer comes from by starting with "According to the [Game Name] rules," or ending with "[Source: Game Name]".
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
I couldn't find that in the loaded rulebooks. Try rephrasing your question, or it may not be covered in the available rule books.
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
Pass all retrieved chunks in regardless of distance score. Filtering risks losing relevant context if the threshold is too aggressive. The grounding instruction already tells the model to say it doesn't know if the answer isn't in the text, so weak chunks won't cause hallucination.
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
System message: contains the grounding instruction and citation instruction.User message: contains the formatted context blocks (each labeled with [Source: GameName]) followed by the question.
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: [How do you get out of Jail in Monopoly?]
Response: [To get out of Jail, you can: pay a $50 fine before rolling on any of your next three turns, use a Get Out of Jail Free card, or roll doubles on any of your three turns in Jail. If you have not rolled doubles after three turns, you must pay the $50 fine and move the number rolled on your final attempt.]
Correctly grounded? [yes]
Cited the right game? [yes]
```

**One thing you changed from your original spec after seeing the actual output:**

```
Changed the context label format from "[Source: GameName]" to "Game: GameName" during implementation — functionally equivalent but slightly less formal.
```
