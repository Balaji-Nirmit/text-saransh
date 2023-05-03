import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
# pip install spacy
# python -m spacy download en_core_web_sm

text="There has been discussion as to whether the first and the last volumes (Bala Kanda and Uttara Kanda) of Valmiki's Ramayana were composed by the original author. The uttarākāṇḍa, the bālakāṇḍa, although frequently counted among the main ones, is not a part of the original epic. Though Balakanda is sometimes considered in the main epic, according to many Uttarakanda is certainly a later interpolation and thus is not attributed to the work of Maharshi Valmiki. This fact is reaffirmed by the absence of these two Kāndas in the oldest manuscript. Many Hindus don't believe they are integral parts of the scripture because of some style differences and narrative contradictions between these two volumes and the rest."
stopwords=list(STOP_WORDS)
nlp=spacy.load("en_core_web_sm")
doc=nlp(text)
tokens=[token.text for token in doc]
# calculating the word frequency
word_frequency={}
for word in doc:
  if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
    if word.text not in word_frequency.keys():
      word_frequency[word.text]=1
    else:
      word_frequency[word.text] +=1

max_frequency=max(word_frequency.values())

# calculating the normalised frequency
for word in word_frequency.keys():
  word_frequency[word]=word_frequency[word]/max_frequency

sentence_tokens=[sent for sent in doc.sents]
sentence_scores={}

for sent in sentence_tokens:
  for word in sent:
    if word.text in word_frequency.keys():
      if sent not in sentence_scores.keys():
        sentence_scores[sent]=word_frequency[word.text]
      else:
        sentence_scores[sent]+=word_frequency[word.text]

select_len=int(len(sentence_tokens)*0.45)#taking 60%

summary=nlargest(select_len,sentence_scores,key=sentence_scores.get)
final_summary=[word.text for word in summary]
summary=" ".join(final_summary)
print(summary)