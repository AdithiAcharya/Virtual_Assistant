import wikipedia
from wolframalpha import Client
from googlesearch import search

class Infow:
    def __init__(self):
        # Initialize Wolfram Alpha client
        self.wolfram_client = Client("843KKU-XK275P75UT")
    
    def get_info(self, query):
        # 1. Try Wolfram Alpha
        try:
            res = self.wolfram_client.query(query)
            answer = next(res.results).text
            return f"According to Wolfram Alpha: {answer}"
        except Exception:
            pass
        
        # 2. Try Wikipedia
        try:
            summary = wikipedia.summary(query, sentences=3)
            return f"According to Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Your query was ambiguous, here are some options: {e.options}"
        except wikipedia.exceptions.PageError:
            pass
        
        # 3. Fallback to Google Search
        try:
            search_results = list(search(query, num_results=1))
            if search_results:
                return f"I found this result: {search_results[0]}"
        except Exception as e:
            return f"An error occurred: {e}"

        return "Sorry, I couldn't find any information on that."
