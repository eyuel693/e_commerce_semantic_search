# Context-Aware Conversational Search System  

##  Project Overview  
This project is a **Flask-based chatbot** that leverages **semantic search**, **intent recognition**, and **query expansion** to provide accurate and context-aware responses. Unlike traditional chatbots, this system retains previous conversation history, enabling more natural and meaningful interactions.  

It is designed for **customer support** or **technical assistance**, where users may ask multiple related questions in a session.  

---

## Features  

 **Semantic Search**: Uses `SentenceTransformer` to understand the meaning of queries and find relevant responses.  
 **Context Retention**: Stores past interactions using a **deque** to provide coherent answers to follow-up questions.  
 **Intent Recognition**: Identifies the user’s intent (e.g., order tracking, product inquiry, customer support).  
 **Query Expansion**: Uses **NLTK WordNet** to enhance queries with synonyms for better response matching.  
 **Flask Web Interface**: Provides an interactive chatbot UI for seamless user interaction.  

---

##  Project Structure 

``` 
semantic-search-chatbot/
│── app.py                 # Flask backend
│── semantic_search.py      # Core logic for intent recognition & query expansion
│── clean_data.py           # Data cleaning functions
│── templates/
│   ├── index.html          # Chatbot UI
│── static/
│   ├── style.css           # Styling for UI
│── requirements.txt        # Required dependencies
│── README.md               # Project documentation

```

# Install dependencies
```
pip install -r requirements.txt
```
# Run the Flask app
```
python app.py
```

# How It Works
**User asks a question**.
**The system identifies the intent** (e.g., order tracking, refund, product inquiry).
**The query is expanded using synonyms to improve search accuracy.**
**The system retrieves the most relevant response using cosine similarity with SBERT embeddings.**
**The chatbot remembers previous interactions for better context understanding.**
**The user receives an accurate and meaningful response.**

# Technologies Used
**Python**
**Flask (Web framework)**
**Pandas (Data handling)**
**NLTK (Natural Language Processing - WordNet for query expansion)**
**Sentence Transformers (all-mpnet-base-v2) for embedding generation**
**Cosine Similarity (For semantic search)**
**HTML, CSS, JavaScript (Frontend UI)**
