
# quote_generator.py
from embeddings import vector_db

def generate_quote(query: str) -> dict:
    """
    Generate a quote (or service info) based on the user query.
    Returns a dictionary with 'name', 'price', 'description'.
    Uses the Chroma vector database created in embeddings.py.
    """
    try:
        results = vector_db.similarity_search(query, k=1)  # Get top 1 most similar
        if results and len(results) > 0:
            matched = results[0].metadata  # Extract the metadata dictionary
            # Ensure it has the required keys
            service_dict = {
                "name": matched.get("name", "Unknown Service"),
                "price": matched.get("price", 0),
                "description": matched.get("description", "No description available.")
            }
            return service_dict
        else:
            return None  # No matching service found
    except Exception as e:
        return None
