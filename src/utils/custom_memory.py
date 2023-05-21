from langchain.vectorstores import VectorStore, Chroma
from langchain.memory.buffer import ConversationBufferMemory
from langchain.schema import Document, HumanMessage, AIMessage, SystemMessage, ChatMessage


class ConversationMemory(ConversationBufferMemory):
    def to_document(
            self,
            human_prefix='Human',
            ai_prefix='AI'
        ) -> Document:
        history = self.chat_memory.messages
        
        # Storing the full chat history between human and AI.
        full_text = []

        # Storing the necessary metadata for recovery.
        # For now, the only metadata needed is the source of chat.
        # TODO: After testing, I want to add more metadata (date of message generation/input, etc)
        # though that in and of itself will need _more_ tampering with the models, so that will be later.
        metadata = []

        for message in history:
            full_text.append(message.content)
            
            # code is based on the get_buffer_string() function in langchain.schema.
            if isinstance(message, HumanMessage):
                role = human_prefix
            elif isinstance(message, AIMessage):
                role = ai_prefix
            elif isinstance(message, SystemMessage):
                role = "System"
            elif isinstance(message, ChatMessage):
                role = message.role
            else:
                raise ValueError(f"Got unsupported message type: {message}")
            
            metadata.append({"source": role})

        return Document(
            page_content=full_text,
            metadata=metadata
        )
    
    def save_to_db(self, v_db: VectorStore, human_prefix = "Human", ai_prefix = "AI"):
        db = v_db.from_documents([self.to_document(human_prefix, ai_prefix)])
        if isinstance(db, Chroma):
            db.persist()
            db = None
        # im not entirely sure for other vector dbs, so thats there for now.