import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
import re
from konlpy.tag import Okt

# 28행을 한 뒤 함수를 만듦
def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    gameiIdx = [i[0] for i in simScore]
    recGameList = df_reviews.iloc[gameiIdx, 0]
    return recGameList


df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
Tfidf_matrix = mmread('./models/Tfidf_game_review.mtx').tocsr() # 매트릭스로 저장된 거 불러옴
with open('./models/tfidf.pickle', 'rb') as f: # 피클 저장한 거 불러옴
    Tfidf = pickle.load(f)

# 문장 기반 추천, 사용자가 입력한 문장 기반으로 추천
# sentence = '룸미러가 보이는 레이싱 게임'
sentence = ('Looter Shooter')

p_sentence = sentence.split()
print(p_sentence)

okt = Okt()

# 불용어 제거, 형태소 분리
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])

count = 0
cleaned_sentences = []

for review in p_sentence:
    review = re.sub('[^가-힣|a-z|A-Z|0-9]', ' ', review)
    # 형태소 분리
    tokened_review = okt.pos(review, stem=True)

    df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Alpha') |
                        (df_token['class'] == 'Adjective')]

    words = []  # 불용어 제거
    for word in df_token.word:
        if 1 < len(word):  # 길이가 1보다 크고
            if word not in stopwords:  # 스톱워드에 없는
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

print(cleaned_sentences)

joined_cleaned_sentences = ' '.join(cleaned_sentences)
print(joined_cleaned_sentences)

sentence_vec = Tfidf.transform([joined_cleaned_sentences])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommandation = getRecommendation(cosine_sim)
print(recommandation)