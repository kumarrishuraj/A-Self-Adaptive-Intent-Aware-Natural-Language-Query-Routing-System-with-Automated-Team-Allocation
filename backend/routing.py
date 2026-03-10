import sys
import os
# Allow importing from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ml.predict_intent import predict_intent

def route_query(query):

    # Get predicted intent and probabilities
    intent, probabilities = predict_intent(query)

    # Sort intents by probability (highest first)
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

    # Select top 2 intents
    departments = [sorted_probs[0][0], sorted_probs[1][0]]

    return departments
# Test routing
if __name__ == "__main__":

    query = input("Enter query: ")

    teams = route_query(query)

    print("\nQuery will be sent to these departments:\n")

    for team in teams:
        print(team)