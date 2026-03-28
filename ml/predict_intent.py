import joblib
from sentence_transformers import SentenceTransformer
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "intent_classifier.pkl")
clf = joblib.load(MODEL_PATH)
# Load SBERT model
sbert = SentenceTransformer("all-MiniLM-L6-v2")


def predict_intent(query):

    # Convert query to embedding
    embedding = sbert.encode([query])

    # Predict intent
    prediction = clf.predict(embedding)[0]

    # Predict probabilities
    probs = clf.predict_proba(embedding)[0]

    labels = clf.classes_

    result = dict(zip(labels, probs))

    return prediction, result


# Test model
if __name__ == "__main__":

    query = input("Enter your query: ")

    intent, probabilities = predict_intent(query)

    print("\nPredicted Intent:", intent)

    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

    print("\nTop Predictions:")
    for intent, score in sorted_probs[:3]:
        print(f"{intent}: {score:.2f}")