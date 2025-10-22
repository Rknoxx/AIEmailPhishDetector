## AIEmailPhishingDetector(ML):

It is a machine learning project driven by artificial intelligence that uses NLP (Natural Language Processing) and Logistic Regression to identify phishing vs. safe emails. This project, which was created using Python, scikit-learn, and pandas, shows how machine learning can distinguish between malicious and legitimate emails. 

## Features: 
•	Cleans and preprocesses raw email text, eliminating special characters, URLs, and other elements. 
•	Transforms text into TF-IDF(Term Frequency – Inverse Document Frequency) vectors so that it can be represented numerically.
•	Trains a Logistic Regression classifier - Uses precision, recall, and F1-score to assess performance 
•	Preserves the vectorizer and trained model for deployment. 
•	I have used Streamlit app for phishing detection in real time.

## Installation & Setup:
1. Clone repo
git clone https://github.com/Rknoxx/AIEmailPhishingDetector.git 
cd AIEmailPhishingDetector

2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # for PowerShell

3. Install dependencies
pip install -r requirements.txt

4. Train the model
cd backend
python train.py

## What this will do:
Preprocess emails -> Train the ML model -> Print classification report -> Save model + vectorizer in /models

## Future Improvements:
•	Add deep learning models (LSTM / BERT for NLP)
•	Deploy as a Streamlit web app
•	Build a browser/email plugin for real-time phishing detection
•	Use a larger dataset (Enron dataset, Kaggle phishing email dataset)

## Tech Stack:
•	Python
•	Pandas / scikit-learn
•	TfidfVectorizer
•	Logistic Regression
•	Joblib (for model persistence)

## License:
This project is licensed under the MIT License.

## Author:
Raj Patil
Master’s in Information Technology (Cybersecurity focus)
Interested in SOC Analyst, Threat Hunter, Cloud Security Engineer, and GRC roles
LinkedIn: https://www.linkedin.com/in/raj-patil834/ 


