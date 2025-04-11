from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from modules.config import configure_gemini_api

#configuring_api
configure_gemini_api()

class GeminiPro:
    def __init__(self, user_question,model_name=None):
        self.user_question = user_question
        self.model = ChatGoogleGenerativeAI(model=model_name if model_name else "gemini-2.0-flash", temperature=0.9)
        self.prompt_template = PromptTemplate(
            template="""
            Your name is 'PDF AI', developed by students of Woxsen University. 
            Answer thoroughly and accurately based on the provided contexts.

            Context :
            {context}

            Question:
            {question}?

            Answer:
            """,
            input_variables=["context", "question"]
        )
        self.chain = load_qa_chain(self.model, chain_type="stuff", prompt=self.prompt_template)

    def generate_response(self, retrieved_docs):
        """Generates a response based on retrieved documents."""
        doc = sum(retrieved_docs.values(), [])

        response = self.chain({"input_documents": doc, "question": self.user_question}, return_only_outputs=True)
        return response["output_text"]
