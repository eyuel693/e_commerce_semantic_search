from sentence_transformers import SentenceTransformer, util
from collections import deque
import nltk
from nltk.corpus import wordnet
from clean_data import load_and_clean_data 


nltk.download('wordnet')


model = SentenceTransformer('all-mpnet-base-v2')

INTENT_MAP = {
    "order tracking": ["track", "shipment", "where is my order", "delivery"],
    "return policy": ["return", "refund", "exchange"],
    "product inquiry": ["price", "cost", "features", "specs", "availability"],
    "customer support": ["help", "issue", "support", "service"],
}

def identify_intent(query):
    query_lower = query.lower()
    for intent, keywords in INTENT_MAP.items():
        if any(keyword in query_lower for keyword in keywords):
            return intent
    return "general inquiry"

def expand_query(query):
    words = query.split()
    expanded_words = []
    for word in words:
        synonyms = wordnet.synsets(word)
        synonym_list = set([syn.lemmas()[0].name().replace("_", " ") for syn in synonyms])
        expanded_words.append(word)  
        expanded_words.extend(synonym_list) 
    return " ".join(expanded_words)


file_path = 'ecommerce_customer_support2.csv'
df = load_and_clean_data(file_path)  


documents = df['Customer Support Info'].tolist()
document_embeddings = model.encode(documents, convert_to_tensor=True)


conversation_history = deque(maxlen=3)

def get_best_response(user_query):
    """Finds the most relevant answer while considering context, intent, and query expansion."""
    intent = identify_intent(user_query)
    expanded_query = expand_query(user_query)

    # Append conversation history for context
    contextual_query = " ".join(conversation_history) + " " + expanded_query

    # Encode the updated query
    query_embedding = model.encode(contextual_query, convert_to_tensor=True)

    # Compute cosine similarity
    cosine_scores = util.cos_sim(query_embedding, document_embeddings)

    # Find the best match
    best_match_idx = cosine_scores.argmax().item()
    best_product = df.iloc[best_match_idx]
    best_answer = best_product['Customer Support Info']

    confidence = cosine_scores[0][best_match_idx].item()

    # If confidence is low, suggest related topics
    if confidence < 0.3:
        suggested_topics = [intent] if intent != "general inquiry" else ["order tracking", "return policy", "product inquiry"]
        response_text = f"I'm not sure I fully understand your question. Were you asking about {', '.join(suggested_topics)}?"
        return {
            'Intent': intent,
            'Response': response_text,
            'Confidence': confidence
        }

    # Return extracted response as a structured dictionary
    return {
        'Intent': intent,
        'Product ID': best_product['Product ID'],
        'Product Name': best_product['Product Name'],
        'Category': best_product['Category'],
        'Price (USD)': best_product['Price (USD)'],
        'Stock Status': best_product['Stock Status'],
        'Return Policy': best_product['Return Policy'],
        'Customer Support Info': best_answer,
        'Confidence': confidence
    }
