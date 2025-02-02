# !pip install wordcloud
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import re
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from collections import Counter
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier  # Step 1: Import RandomForestClassifier
from nltk.stem import WordNetLemmatizer

# Load dataset (replace 'twitter_training (2).csv' with your actual file path)
data = pd.read_csv("/content/twitter_training (2).csv")

print(data.shape)

print(data.tail())

print("Missing values before imputation:")
print(data.isnull().sum())

# Preprocessing
# Handle missing values (address potential issues with 'type' column)
imputer = SimpleImputer(strategy="constant", fill_value="Unknown")
data[['TWEET', 'TYPE']] = imputer.fit_transform(data[['TWEET', 'TYPE']])  # Impute both 'text' and 'type'

# Check for missing values after imputation
print("Missing values after imputation:")
print(data.isnull().sum())

# Download NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Load dataset

# Define preprocessing functions
def preprocess_text(text):
    """Preprocess text data."""
    text = str(text)
    # Convert text to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters, whitespace, newline, and tab characters
    text = re.sub(r"[^\w\s\n\t]+", "", text)
    return text

def remove_stopwords(text):
    """Remove stopwords from text."""
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return ' '.join(filtered_text)

def lemmatize_text(text):
    """Lemmatize words in text."""
    lemmatizer = WordNetLemmatizer()
    word_tokens = word_tokenize(text)
    lemmatized_text = [lemmatizer.lemmatize(word) for word in word_tokens]
    return ' '.join(lemmatized_text)


# Preprocessing
imputer = SimpleImputer(strategy="constant", fill_value="Unknown")
data[['TWEET', 'TYPE']] = imputer.fit_transform(data[['TWEET', 'TYPE']])
print(data)
data['TWEET'] = data['TWEET'].apply(preprocess_text)
data['TWEET'] = data['TWEET'].apply(remove_stopwords)
data['TWEET'] = data['TWEET'].apply(lemmatize_text)

print(data.tail())

# Split data into input (X) and target (y)
X = data['TWEET']
y = data['TYPE']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert non-string elements to string in X_train
X_train = X_train.astype(str)
X_test = X_test.astype(str)
# Vectorize the text data
vectorizer = CountVectorizer()
vectorizer.fit(X_train)
X_train_vec = vectorizer.transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Naive Bayes classifier
classifier = RandomForestClassifier()               #92%
classifier.fit(X_train_vec, y_train)

# Predict
y_pred = classifier.predict(X_test_vec)
# Calculate accuracy (assuming 'type' has multiple classes)
accuracy = accuracy_score(y_test, y_pred)
# Assuming 'new_tweet' contains the new tweet as a string
new_tweet = input("Enter tweet for sentiment analysis : ")

# Preprocess the new tweet
cleaned_tweet = preprocess_text(new_tweet)
cleaned_tweet = remove_stopwords(new_tweet)
cleaned_tweet = lemmatize_text(new_tweet)

# Vectorize the preprocessed new tweet
vectorized_tweet = vectorizer.transform([cleaned_tweet])

# Predict the sentiment
predicted_sentiment = classifier.predict(vectorized_tweet)

print("Predicted Sentiment:", predicted_sentiment)
# Predict the sentiment

# Calculate and print the accuracy
print("Accuracy:", accuracy_score(y_test, y_pred)*100)

# Compute confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()

# Define classes and tick marks
classes = np.unique(np.concatenate((y_test, y_pred)))
tick_marks = np.arange(len(classes))

# Set axis labels and ticks
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)

# Add text annotations
for i in range(len(classes)):
    for j in range(len(classes)):
        plt.text(j, i, conf_matrix[i, j], horizontalalignment="center", color="white" if conf_matrix[i, j] > conf_matrix.max() / 2 else "black")

# Set axis labels
plt.xlabel('Predicted')
plt.ylabel('True')

# Show plot
plt.show()
# Calculate count of correct and incorrect predictions
correct_count = np.sum(y_test == y_pred)
incorrect_count = len(y_test) - correct_count

# Plot bar graph
plt.bar(['Correct Predictions', 'Incorrect Predictions'], [correct_count, incorrect_count], color=['green', 'red'])
plt.title('Correct vs Incorrect Predictions')
plt.xlabel('Prediction')
plt.ylabel('Count')
plt.show()
print()

# Collect text data for each sentiment category
# Check if 'text' column contains string data before joining
positive_text = ' '.join(data[data['TYPE'] == 'Positive']['TWEET'].astype(str))
negative_text = ' '.join(data[data['TYPE'] == 'Negative']['TWEET'].astype(str))
neutral_text = ' '.join(data[data['TYPE'] == 'Neutral']['TWEET'].astype(str))

# Generate word clouds
positive_wordcloud = WordCloud(width=800, height=400, background_color='white', min_font_size=10).generate(positive_text)
negative_wordcloud = WordCloud(width=800, height=400, background_color='white', min_font_size=10).generate(negative_text)
neutral_wordcloud = WordCloud(width=800, height=400, background_color='white', min_font_size=10).generate(neutral_text)

# Plot word clouds
plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.imshow(positive_wordcloud, interpolation='bilinear')
plt.title('Positive Sentiment Word Cloud')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(negative_wordcloud, interpolation='bilinear')
plt.title('Negative Sentiment Word Cloud')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(neutral_wordcloud, interpolation='bilinear')
plt.title('Neutral Sentiment Word Cloud')
plt.axis('off')
plt.tight_layout()
plt.show()
