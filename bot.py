from query import llm, contextualize, retrieve

SYSTEM_PROMPT = """Eres un experto en tributación de Chile llamado 'Louis' y estás ayudando a un usuario con sus preguntas tributarias.

Debes responder de manera SIMPLE y CONSISA, sin entrar en detalles técnicos, y con lenguaje amigable y común.

Puedes utilizar el siguiente contexto para responder a la pregunta del usuario:
"""

def answer(question: str, history: list[dict]) -> str:
    question_with_context = contextualize(question, history)
    context = retrieve(question_with_context)
    prompt_with_context = f"{SYSTEM_PROMPT}\n{context}"

    response = llm.chat.completions.create(
        model="gpt-4o",
        messages=[{ "role": "system", "content": prompt_with_context }] + history + [{ "role": "user", "content": question }],
    )

    return response.choices[0].message.content
