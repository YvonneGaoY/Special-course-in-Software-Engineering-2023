import nltk  

from nltk.corpus import gutenberg  
from nltk.tokenize import word_tokenize  
from nltk.tag import pos_tag  
from nltk.corpus import stopwords  
from collections import Counter  
from nltk.stem import WordNetLemmatizer  
import collections  
import nltk
import matplotlib.pyplot as plt  
import string
import matplotlib
matplotlib.use('Agg')
from nltk.sentiment import SentimentIntensityAnalyzer
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('gutenberg')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('vader_lexicon')

moby_dick = gutenberg.raw("melville-moby_dick.txt")  
  
# 1.Tokenization
# tokens = word_tokenize(moby_dick) 
tokens = [token for token in word_tokenize(moby_dick) if token not in string.punctuation]
print('/////////////Tokenization////////////')
print(tokens)
 
# 2.Filter stop words 
stop_words = set(stopwords.words('english'))  
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]  
# filtered_tokens = [token for token in tokens if token.lower() not in stop_words and token not in string.punctuation]
print('/////////////Stop-words filtering////////////')
print(filtered_tokens)
  
# 3.Parts-of-Speech (POS) tagging
tagged = pos_tag(tokens)
tagged_stop_words = [token for token in tagged if token[0].lower() in stop_words]  
# Remove PART-of-speech tagging for stop words
# tagged_without_stop_words = [token for token in tagged if token[0].lower() not in stop_words]  
tagged_without_stop_words = [token for token in tagged if token[0].lower() not in stop_words and token[0] not in string.punctuation]

print('/////////////Parts-of-Speech (POS) tagging////////////')
for token, tag in tagged_without_stop_words:
    print(f"{token}: {tag}")
    
# 4.POS frequency
pos_freq = Counter([tag for token, tag in tagged if token not in string.punctuation])

# Print the 5 most common parts of speech and their frequencies
print('/////////////POS frequency////////////')
for pos, count in pos_freq.most_common(5):  
    print(f"{pos}: {count}")
    

# 5.Lemmatization
lemmatizer = WordNetLemmatizer()
pos_freq = Counter([lemmatizer.lemmatize(token[0]) for token in tagged_without_stop_words])

print('/////////////Lemmatization////////////')
for lemma, count in pos_freq.most_common(20):
    print(f"{lemma}: {count}")
    
    
# 6.Plotting frequency distribution
# pos_freq = Counter([tag for token, tag in tagged if token not in string.punctuation])
pos_freq = Counter([tag for token, tag in tagged_without_stop_words if token[0] not in string.punctuation])

all_pos = [pos for pos, count in pos_freq.most_common()]
all_freq = [count for pos, count in pos_freq.most_common()]

plt.figure(figsize=(10, 5))
plt.title('Plotting frequency distribution')
plt.xlabel('Parts of Speech')
plt.ylabel('occurrences')
plt.bar(all_pos, all_freq, color='C0', edgecolor='black')

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('Plotting frequency distribution.png')


# 7.Sentiment analysis
sentiment_analyzer = SentimentIntensityAnalyzer()
 
sentiment_scores = []
for sentence in nltk.sent_tokenize(moby_dick):
    sentiment = sentiment_analyzer.polarity_scores(sentence)
    sentiment_scores.append(sentiment['compound'])

#Calculate average sentiment score
average_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)

# Judging positive or negative
overall_sentiment = 'positive' if average_sentiment_score > 0.05 else 'negative'

print("/////////////Sentiment analysis/////////////")
print("Average Sentiment Score: ", average_sentiment_score)
print("Overall Text Sentiment: ", overall_sentiment)
