from ollama import Client
from modules.utils.docker_utils import is_running_in_docker


class OllamaModel:
    def __init__(self, user_question, model_name, host=None):
        """Initializes the Ollama model for processing user queries."""
        self.user_question = user_question
        self.model_name = model_name

        # Check if running inside a Docker container
        self.is_docker = is_running_in_docker()

        # Determine connection type
        if host:
            self.connection_type = "external"
        elif self.is_docker:
            host = "http://host.docker.internal:11434"
            self.connection_type = "docker_internal"
        else:
            self.connection_type = "internal"

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

        if all_contexts:
            context_text = "\n\n".join(all_contexts)
            messages = [{
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {self.user_question}\n\nAnswer:"
            }]
            context = True
        else:
            messages = [{
                "role": "user",
                "content": f"\n\nQuestion: {self.user_question}\n\nAnswer:"
            }]
            context = False

        try:
            response = self.client.chat(model=self.model_name, messages=messages)
            return response.message.content, context
        except Exception:
            return "Failed to generate response from Ollama."

    @staticmethod
    def list_models(host=None):
        """
        Lists available Ollama models.

        Returns:
            dict: {
                'models': list of model names or a message if not connected,
                'connected': boolean indicating connection status,
                'docker': boolean indicating if running inside Docker,
                'connection_type': 'external' | 'docker_internal' | 'internal'
            }
        """
        # Check if running inside a Docker container
        is_docker = is_running_in_docker()

        # Determine connection type
        connection_type = 'internal'  # default
        if host:
            connection_type = 'external'
        elif is_docker:
            host = "http://host.docker.internal:11434"
            connection_type = 'docker_internal'

        try:
            client = Client(host=host) if host else Client()
            model_list = client.list()
            models = [model.model for model in getattr(model_list, "models", [])]

            return {
                "models": models,
                "connected": True,
                "docker": is_docker,
                "connection_type": connection_type
            }

        except Exception as e:
            a = f"[OllamaModel] Connection failed: {e}"
            return {
                "models": ["Ollama not connected"],
                "connected": False,
                "docker": is_docker,
                "connection_type": connection_type
            }
