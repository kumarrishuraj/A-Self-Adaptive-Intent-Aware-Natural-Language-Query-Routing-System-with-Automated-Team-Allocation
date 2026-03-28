import joblib
clf = joblib.load('c:/Users/Rishuraj Kumar/NLP-Routing-System/models/intent_classifier.pkl')
print(list(clf.classes_))
