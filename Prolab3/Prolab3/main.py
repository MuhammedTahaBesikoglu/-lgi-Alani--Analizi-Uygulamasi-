import json
import networkx as nx
import matplotlib.pyplot as plt

class Dugum:
    def __init__(tut,key,value,next_dugum = None):
        tut.key = key
        tut.value =value
        tut.next_dugum = next_dugum

class MyHashMap: 
    def __init__(tut, kapasite=16):
        tut.demet = [None] * kapasite
        tut.size = 0

    def get_demet_index(tut, key):
        hash_code = hash(key)
        return hash_code% len(tut.demet)

    def put(tut, key, value):
        demet_index = tut.get_demet_index(key)

        #  bu demet boşsa yeni bir giriş oluştur
        if tut.demet[demet_index] is None:
            tut.demet[demet_index] = Dugum(key, value)
            tut.size += 1
            return

        #  bu demet doluysa, zinciri kontrol et ve ekle veya güncelle
        simdiki = tut.demet[demet_index]
        while simdiki is not None:
            if simdiki.key ==key:
                simdiki.value = value  # Anahtar zaten varsa güncelle
                return
            simdiki = simdiki.next_dugum

        # Zincir sonuna yeni bir giriş ekle
        new_giris = Dugum(key, value, tut.demet[demet_index])
        tut.demet[demet_index] = new_giris
        tut.size += 1

    def get(tut, key):
        demet_index = tut.get_demet_index(key)
        simdiki = tut.demet[demet_index]

        while simdiki is not None:
            if simdiki.key == key:
                return simdiki.value
            simdiki =simdiki.next_dugum

        return None 

    def size(tut):
        return tut.size

    def values(tut):
        deger_listesi=[]
        for giris in tut.demet:
            while giris is not None:
                deger_listesi.append(giris.value)
                giris = giris.next_dugum

        return deger_listesi


with open('C:/Users/tahab/Desktop/Prolab3/fakeData1.json', 'r') as dosya:
    veriler = json.load(dosya)


username=input("Lütfen bir username girin: ")


hashmap = MyHashMap()

for kullanici in veriler:
    if kullanici['username'] == username:
        takipci = kullanici['followers']
        takip_edilen = kullanici['following']
        hashmap.put(username, kullanici)

print("Hashmap İçeriği:")
for giris in hashmap.demet:
    while giris is not None:
        print(f"Key: {giris.key}, Value: {giris.value}")
        giris = giris.next_dugum
        print("\n")


graf_takipci = nx.Graph()
graf_takip_edilen = nx.Graph()


for kullanici in veriler:
    if kullanici['username'] == username:
        takipci = kullanici['followers']
        takip_edilen = kullanici['following']

      
        graf_takipci.add_node(username)
        graf_takipci.add_edges_from((username, follower) for follower in takipci)

        graf_takip_edilen.add_node(username)
        graf_takip_edilen.add_edges_from((username, followed) for followed in takip_edilen)


plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
nx.draw(graf_takipci, with_labels=True, font_weight='bold', node_color='skyblue')
plt.title(f"{username}'in Takipçileri")

plt.subplot(1, 2, 2)
nx.draw(graf_takip_edilen, with_labels=True, font_weight='bold', node_color='lightcoral')
plt.title(f"{username}'in Takip Ettikleri")

plt.show()


graph_data_file = 'takipci_takipEdilen.txt'



with open(graph_data_file, 'w' , encoding='utf-8') as file:
    file.write(f"Takipçi bilgileri:\n")
    for edge in graf_takipci.edges():
        file.write(f"{edge[0]} -> {edge[1]}\n")

    file.write(f"\nTakip edilen bilgileri:\n")
    for edge in graf_takip_edilen.edges():
        file.write(f"{edge[0]} -> {edge[1]}\n")



