from ollama import Client

class OllamaModel:
    def __init__(self, user_question, model_name, host=None):
        """Initializes the Ollama model for processing user queries."""
        self.user_question = user_question
        self.model_name = model_name
        try:
            self.client = Client(host=host) if host else Client()
            self.connected = True
        except Exception:
            self.client = None
            self.connected = False

    def generate_response(self, retrieved_docs):
        """Generates a response using an open-source model via Ollama."""
        if not self.connected:
            return "Ollama is not connected."

        all_contexts = [doc.page_content for doc in sum(retrieved_docs.values(), [])]

        if  all_contexts:
            context_text = "\n\n".join(all_contexts)
            print("Context")
            messages = [{
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {self.user_question}\n\nAnswer:"
            }]
        else:
            print("No context")
            messages = [{
                "role": "user",
                "content": f"\n\nQuestion: {self.user_question}\n\nAnswer:"
            }]


        try:
            response = self.client.chat(model=self.model_name, messages=messages)
            return response.message.content
        except Exception:
            return "Failed to generate response from Ollama."

    @staticmethod
    def list_models(host=None):
        """Lists available Ollama models locally or on an external host."""
        try:
            client = Client(host=host) if host else Client()
            return client.list()
        except Exception:
            return None