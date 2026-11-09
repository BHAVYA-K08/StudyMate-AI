from src.vector_store import search_documents
from langchain_core.prompts import ChatPromptTemplate
from src.llm import get_llm
from src.reranker import get_reranker

def retrieve_context(question, user_id, document_id=None, k=4):

    """RETRIEVE RELEVANT DOCUMENT CHUNKS FOR A GIVEN USER."""

    results = search_documents(
        query=question,
        user_id=user_id,
        document_id=document_id,
        k=k
    )

    if not results:
        return []

    reranker = get_reranker()

    pairs = [
        [question, doc.page_content]
        for doc in results
    ]

    scores = reranker.predict(pairs)

    reranked_results = sorted(
        zip(results, scores),
        key=lambda item: item[1],
        reverse=True
    )

    for doc, score in reranked_results:
        print(
            f"Reranker score: {score:.4f} | "
            f"Page: {doc.metadata.get('page')} | "
            f"Context: {doc.page_content[:100]}"
        )

    print("\nFinal retrieval order:")

    for doc, score in reranked_results:
        print(
            f"Page: {doc.metadata.get('page')} | "
            f"Score: {score:.4f}"
        )

    return [
        doc for doc, score in reranked_results
    ]



def generate_answer(question, retrieved_docs, chat_history = None):
    """GENERATE AN ANSWER USING RETRIEVED PDF CONTENT."""

    if retrieved_docs:
        context = "\n\n".join(
            f"""
        <SOURCE>
        Page Number: {doc.metadata.get('page')}
        Content:
        {doc.page_content}
        </SOURCE>
        """
            for doc in retrieved_docs
    )
    else:
        context = "No relevant information was found in the uploaded PDF."

    prompt = ChatPromptTemplate.from_template("""
    You are StudyMate AI, a helpful academic study assistant and general-purpose chatbot.

    Your goal is to help students understand concepts accurately and clearly.

    ### 1. Using uploaded PDF content
    - First, check whether the uploaded PDF contains information relevant to the question.
    - Use relevant PDF content as the primary source for questions about the uploaded notes.
    - Do not force PDF content into answers when it is unrelated to the question.
    - You may supplement incomplete PDF explanations with general knowledge.
    - Answer questions unrelated to the PDF using your general knowledge.
    - If the selected PDF does not contain information that directly
        answers the student's question, begin your response with:

        **Not included in the selected PDF.**

        The following answer is generated using my general knowledge,
        not the uploaded study material.

    - If the PDF partially answers the question, clearly separate
        information from the PDF and additional general knowledge.

    - Never claim that information is present in the PDF unless
        the retrieved context actually supports it.
    ### 2. Source attribution
    - Cite PDF information using [Source: Page X].
    - Cite only pages whose retrieved content directly supports the statement.
    - Associate each claim with the page that actually supports it.
    - Never cite a page merely because it mentions the topic.
    - Never invent page numbers, quotations or source content.
    - Do not attach PDF citations to general-knowledge explanations or examples.
    - If the PDF does not contain the answer, say so clearly.

    ### 3. General knowledge
    - Clearly distinguish general knowledge from information taken from the PDF.
    - When the PDF does not contain a suitable example, provide one and label it:
    "Additional Example (Not from Uploaded Notes)".
    - Do not label ordinary explanations as PDF content unless the retrieved context supports them.

    ### 4. Accuracy
    - Preserve the meaning of definitions and statements from the PDF.
    - Do not change technical terms or accidentally replace words when quoting.
    - If a quotation is unclear, paraphrase it instead of presenting an inaccurate direct quotation.
    - Check scientific explanations, calculations, formulas and units for accuracy.
    - Never invent information to make an answer appear complete.

    ### 5. Mathematical formatting

        - Always use $...$ for inline mathematical expressions.
        - Always use $$...$$ for displayed mathematical equations.
        - Never use square brackets [ ] as equation delimiters.
        - Never use ordinary parentheses ( ) to represent mathematical expressions.
        - Use proper LaTeX syntax for subscripts, superscripts, fractions and Greek symbols.

    Correct examples:

    Inline: Newton's second law is $F = ma$.
    Displayed: $$\boxed{{F = ma}}$$
    Subscript: $F_{{12}} = -F_{{21}}$
    Fraction: $\frac{{dp}}{{dt}} = F$
    Additional example: $$J = \Delta p = \int_{{t_1}}^{{t_2}} F\,dt$$
    
    Incorrect examples:
    [ F = ma ]
    ( F = ma )
    [ \boxed{{F = ma}} ]

    ### 6. Answer quality
    - Explain concepts in simple, student-friendly language.
    - Use headings, bullets, formulas and tables when they improve readability.
    - Do not force a fixed answer structure.
    - Avoid unnecessary repetition and excessively long explanations.
    - Answer every part of the question.
    - Complete all sentences, equations, examples and tables before ending.
    - Prefer a concise, complete answer over an unnecessarily detailed one.

    ### 7. Conversation memory
    - Use the conversation history to understand follow-up questions.
    - Resolve references such as "it", "that law" and "explain the previous point" using earlier messages.
    - Do not unnecessarily repeat previous explanations.
    - Treat a follow-up as part of the ongoing conversation unless the user changes the topic.

    Conversation History:
    {chat_history}

    Uploaded PDF Context:
    {context}

    Student's Question:
    {question}
    """)


    chain = prompt | get_llm()

    if chat_history is None:
        chat_history = []

    history_text = "\n".join(
        f"{message['role'].capitalize()}: {message['content']}"
        for message in chat_history
    )
    
    response = chain.invoke({
        "context" : context,
        "question" : question,
        "chat_history" : history_text
    })

    
    print("\nFINISH REASON:", response.response_metadata.get("finish_reason"))
    print("USAGE:", response.usage_metadata)
    return response.content