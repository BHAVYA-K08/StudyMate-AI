from langchain_core.prompts import ChatPromptTemplate
from src.llm import get_llm

def summarize_text(text):
    """GENERATE A SUMMARY OF THE PROVIDED TEXT."""

    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert study assistant.

        Summarize the following study material clearly.
        Include:
        1. Main Topic
        2. Important Content
        3. Key definitions
        4. Important points for revision

        Keep the summary concise and easy to understand.

        Study Material:
        {input_text}
        """
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "input_text" : text
        }
    )

    return response.content


def map_summaries(chunks, batch_size = 5):
    """GENERATE AN INDIVIDUAL SUMMARY FOR EVERY TEXT CHUNK."""

    summaries =  []

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]

        combined_text = "\n\n".join(
            chunk['text'] for chunk in batch
        )

        summary = summarize_text(combined_text)

        summaries.append(
            {
                "page" : batch[0]["page"],
                "chunk" : batch[0]["chunk"],
                "summary" : summary
            }
        )

    return summaries

def reduce_summaries(summaries):
    """COMBINE INDIVIDUAL CHUNK SUMMARIES INTO ONE FINAL SUMMARY."""

    if not summaries:
        raise ValueError("No summaries provided.")

    combined_text = "\n\n".join(
        item["summary"] for item in summaries
    )

    final_summary = summarize_text(
        f"""
        Combine the following section summaries into one 
        comprehensive set of study notes.
        
        Instructions:
        1. Organize the content using meaningful headings.
        2. Preserve important definitions and concepts.
        3. Remove repetitive information.
        4. Use bullet points whenever appropriate.
        5. Do not introduce information that is not present 
           in the provided summaries.
           
        Section Summaries:
        
        {combined_text}
        """
    )

    return final_summary

def summarize_chunks(chunks):
    """GENERATE FINAL SUMMARY FROM MILTIPLE PDF CHUNKS."""

    if not chunks:
        raise ValueError("No chunks provided.")

    #MAP: Summarize each chunk individually.
    summaries = map_summaries(chunks)

    #REDUCE: Combine all individual summaries.
    final_summary = hierarchical_reduce_summaries(
        summaries,
        batch_size = 5
    )

    return final_summary


def hierarchical_reduce_summaries(summaries, batch_size = 5):
    """COMBINE SUMMARIES IN SMALLER GROUPS UNTIL ONE REMAINS"""

    if not summaries:
        raise ValueError("No summaries provided.")

    if batch_size < 2:
        raise ValueError("The batch size must be at least 2.")


    current_summaries = summaries

    while len(current_summaries) > 1:
        next_summaries = []

        for i in range(0, len(current_summaries), batch_size):
            batch = current_summaries[i: i + batch_size]

            combined_summary = reduce_summaries(batch)

            next_summaries.append({
                "summary" : combined_summary
            })

        current_summaries = next_summaries

    return current_summaries[0]["summary"]