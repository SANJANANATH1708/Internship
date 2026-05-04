# 1. IMPORT LIBRARIES
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter

nltk.download('stopwords')

# =========================================
# 2. CREATE SAMPLE DATASET
# =========================================
data = {
    "Review": [
        "This product is amazing and works perfectly!",
        "Worst experience ever, very bad quality",
        "It is okay, not great but not bad",
        "I love this! Highly recommend it",
        "Terrible, waste of money"
    ]
}

df = pd.DataFrame(data)

print("Original Reviews:")
print(df)


# =========================================
# 3. TEXT PREPROCESSING
# =========================================
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def preprocess(text):
    text = text.lower()
    words = text.split()
    words = [w for w in words if w not in stop_words]
    words = [stemmer.stem(w) for w in words]
    return " ".join(words)

df["Cleaned_Review"] = df["Review"].apply(preprocess)

print("\nCleaned Reviews:")
print(df)


# =========================================
# 4. SENTIMENT ANALYSIS
# =========================================
analyzer = SentimentIntensityAnalyzer()

# TextBlob (original)
df["TextBlob_Original"] = df["Review"].apply(lambda x: TextBlob(x).sentiment.polarity)

# TextBlob (cleaned)
df["TextBlob_Cleaned"] = df["Cleaned_Review"].apply(lambda x: TextBlob(x).sentiment.polarity)

# VADER (original)
df["VADER_Original"] = df["Review"].apply(lambda x: analyzer.polarity_scores(x)["compound"])

# VADER (cleaned)
df["VADER_Cleaned"] = df["Cleaned_Review"].apply(lambda x: analyzer.polarity_scores(x)["compound"])

print("\nSentiment Comparison:")
print(df)


# =========================================
# 5. WORD FREQUENCY ANALYSIS
# =========================================

# Before cleaning
all_words = " ".join(df["Review"]).lower().split()
freq_before = Counter(all_words)

# After cleaning
all_clean_words = " ".join(df["Cleaned_Review"]).split()
freq_after = Counter(all_clean_words)

print("\nTop Words Before Cleaning:")
print(freq_before.most_common(5))

print("\nTop Words After Cleaning:")
print(freq_after.most_common(5))