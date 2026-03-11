import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ml.predict_intent import predict_intent


def route_query(query):

    intent, probabilities = predict_intent(query)

    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

    departments = [
        sorted_probs[0][0],
        sorted_probs[1][0]
    ]

    return departments