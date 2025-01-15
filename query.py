from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

llm = OpenAI()

# Inicializa los embeddings (deben coincidir con los usados al guardar)
embeddings = OpenAIEmbeddings()

# Carga el vectorstore persistido desde la carpeta "data"
chroma_db = Chroma(
    persist_directory="data", 
    embedding_function=embeddings, 
    collection_name="dl_824"
)

# Usaremos este prompt (obtenido de https://github.com/pinecone-io/canopy/blob/main/src/canopy/chat_engine/query_generator/instruction.py)
# para generar preguntas a partir de conversaciones
SYSTEM_PROMPT = """You are an expert on formulating a search query for a search engine,
to assist in responding to the user's question.

Given the following conversation, create a standalone question summarizing
 the user's last question, in its original language.

Reply to me in JSON in this format:

 {"question": {The question you generated here}}.

   Example:

        User: What is the weather today?

        Expected Response:
            ```json
            {"question": "What is the weather today?"}
            ```

    Example 2:

        User: How should I wash my white clothes in the laundry?
        Assistant: Separate from the colorful ones, and use a bleach.
        User: Which temperature?

        Expected Response:
         ```json
         {"question": "What is the right temperature for washing white clothes?"}
         ```


   Do not try to answer the question; just try to formulate a question representing the user's question.
   Do not return any other format other than the specified JSON format and keep it really short.

"""

USER_PROMPT = "Return only a JSON containing a single key 'question' and the value."


class Question(BaseModel):
    question: str


def contextualize(query: str, messages: list[dict]) -> str:
    new_history = [{ "role": "system", "content": SYSTEM_PROMPT }]
    new_history +=  messages + [{ "role": "user", "content": query }] + [{ "role": "user", "content": USER_PROMPT }]

    response = llm.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=new_history,
        response_format=Question
    )

    return response.choices[0].message.parsed.question


def retrieve(query: str) -> str:
    results = chroma_db.similarity_search(query, k=5)
    context = ''

    for result in results:
        context += result.page_content + '\n\n'

    return context
