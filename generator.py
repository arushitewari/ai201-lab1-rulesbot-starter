from config import GROQ_API_KEY, LLM_MODEL

# Lazily import Groq to avoid import-time errors in editors/linters
_client = None


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    # ensure Groq client is available
    global _client
    if _client is None:
        try:
            import importlib

            groq_module = importlib.import_module("groq")
            Groq = groq_module.Groq
        except Exception:
            return (
                "The Groq client library is not available. "
                "Install the 'groq' package and set GROQ_API_KEY in config."
            )
        _client = Groq(api_key=GROQ_API_KEY)

    context = ""
    for chunk in retrieved_chunks:
        context += f"Game: {chunk['game']}\nRules: {chunk['text']}\n\n"

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are RulesBot. Answer using ONLY the rule text provided below. "
                    "If the answer is not in the provided text, say so explicitly — "
                    "do not draw on outside knowledge or fill in gaps from what you know about board games."
                )
            },
            {
                "role": "user",
                "content": f"Here are the relevant rules:\n\n{context}\nQuestion: {query}"
                
            }
        ]
    )
    return response.choices[0].message.content
    #return "⚙️ Response generation not yet implemented. Complete Milestone 3 to activate answers."
