import json
import networkx as nx
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import pos_tag


class Dugum:
    def __init__(tut, key, value, pos=None, next_Dugum=None):
        tut.key = key
        tut.value = value
        tut.pos = pos
        tut.next_Dugum = next_Dugum

class MyHashMap:
    def __init__(tut, kapasite=16):
        tut.demet = [None] * kapasite
        tut.size = 0

    def get_demet_index(tut, key):
        hash_code = hash(key)
        return hash_code % len(tut.demet)

    def put(tut, key, value, pos=None):
        demet_index = tut.get_demet_index(key)

        #  bu demet boşsa yeni bir giriş oluştur
        if tut.demet[demet_index] is None:
            tut.demet[demet_index] = Dugum(key, value, pos)
            tut.size += 1
            return

        # bu demet doluysa, zinciri kontrol et ve ekle veya güncelle
        simdiki = tut.demet[demet_index]
        while simdiki is not None:
            if simdiki.key == key:
                simdiki.value = value 
                simdiki.pos = pos
                return
            simdiki = simdiki.next_Dugum

        # Zincir sonuna yeni bir giriş ekle
        new_giris = Dugum(key, value, pos, tut.demet[demet_index])
        tut.demet[demet_index] = new_giris
        tut.size += 1

    def get(tut, key):
        demet_index = tut.get_demet_index(key)
        simdiki = tut.demet[demet_index]

        while simdiki is not None:
            if simdiki.key == key:
                return simdiki.value, simdiki.pos
            simdiki = simdiki.next_Dugum

        return None 

    def size(tut):
        return tut.size

    def values(tut):
        deger_listesi = []
        for giris in tut.demet:
            while giris is not None:
                deger_listesi.append((giris.value, giris.pos))
                giris = giris.next_Dugum

        return deger_listesi



with open('C:/Users/tahab/Desktop/Prolab3/fakeData1.json', 'r') as dosya:
    veriler = json.load(dosya)


hashmap = MyHashMap()


for kullanici in veriler[:1000]:
    username = kullanici['username']
    tweets = kullanici['tweets']


    all_tweets = ' '.join(tweets)
    tokenized_tweets = word_tokenize(all_tweets.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tweets = [word for word in tokenized_tweets if word.isalpha() and word not in stop_words]

    
    freq_dist = FreqDist(filtered_tweets)


    most_common_word = freq_dist.max()

   
    
    pos_tags = pos_tag(filtered_tweets)

  
    hashmap.put(username, most_common_word, pos_tags)


print("Hashmap İçeriği:")
for giris in hashmap.demet:
    while giris is not None:
        print(f"Key: {giris.key}, Value: {giris.value}, POS: {giris.pos}")
        giris = giris.next_Dugum
        print("\n")


graf_most_common_words = nx.Graph()


for giris1 in hashmap.demet:
    while giris1 is not None:
        for giris2 in hashmap.demet:
            while giris2 is not None:
                if giris1.key != giris2.key and giris1.value == giris2.value:
                    # Birbirleriyle bağlantı kurmuş kullanıcıları ekle
                    graf_most_common_words.add_edge(giris1.key, giris2.value)
                giris2 = giris2.next_Dugum
        giris1 = giris1.next_Dugum


plt.figure(figsize=(8, 8))
pos = nx.spring_layout(graf_most_common_words)
nx.draw(graf_most_common_words, pos, with_labels=True, font_weight='bold')
plt.title("İlk 10 Kullanıcının Ortak En Çok Geçen Kelimeleri Arasındaki Bağlantılar")
plt.show()


ilgi_alani = 'ilgi_alani.txt'


with open(ilgi_alani, 'w') as ilgi_alani:
  
    for kullanici in veriler[:30000]:
        username = kullanici['username']
        tweets = kullanici['tweets']

       
        all_tweets = ' '.join(tweets)
        tokenized_tweets = word_tokenize(all_tweets.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tweets = [word for word in tokenized_tweets if word.isalpha() and word not in stop_words]

 
        freq_dist = FreqDist(filtered_tweets)

      
        most_common_word = freq_dist.max()

      
        pos_tags = pos_tag(filtered_tweets)

        
        hashmap.put(username, most_common_word, pos_tags)

      
        ilgi_alani.write(f"Kullanici Adi: {username}, Ilgi Alani: {most_common_word}\n")
