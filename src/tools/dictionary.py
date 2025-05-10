import requests

def dictionary_tool(query):
    """
    A simple dictionary tool that defines words.
    """
    # Extract the word to define from the query
    word = query.lower().replace("define", "").replace("what is", "").replace("meaning of", "").strip()
    
    try:
        # Use a free dictionary API
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                meanings = data[0].get("meanings", [])
                if meanings:
                    definition = meanings[0].get("definitions", [{}])[0].get("definition", "No definition found")
                    return f"Definition of {word}: {definition}"
            
            return f"I couldn't find a definition for '{word}'."
        else:
            return f"I couldn't find a definition for '{word}'."
    except Exception as e:
        return f"I encountered an error while looking up the definition: {str(e)}"