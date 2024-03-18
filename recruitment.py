import pandas as pd
from sklearn import tree
from pymongo import MongoClient

df = pd.read_csv("reading_data/DecisionTreesClassificationDataSet.csv")

duzeltme_mapping = {'Y': 1, 'N': 0}
df['IseAlindi'] = df['IseAlindi'].map(duzeltme_mapping)
df['StajBizdeYaptimi?'] = df['StajBizdeYaptimi?'].map(duzeltme_mapping)
df['Top10 Universite?'] = df['Top10 Universite?'].map(duzeltme_mapping)
df['SuanCalisiyor?'] = df['SuanCalisiyor?'].map(duzeltme_mapping)

duzeltme_mapping_egitim = {'BS': 0, 'MS': 1, 'PhD': 2}
df['Egitim Seviyesi'] = df['Egitim Seviyesi'].map(duzeltme_mapping_egitim)

y = df['IseAlindi']
X = df.drop(['IseAlindi'], axis=1)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)

print("=============================\n")
print("İşe alma yapay zekası")
print("\n=============================\n")

while True:
    print("\n=============================\n")
    deneyim = int(input("\nKaç yıl deneyiminiz oldu: \n"))
    print("\n=============================\n")
    print("\n=============================\n")
    print("Evet için 1\nHayır için 0'a basın\n")
    suan = int(input("\nŞuan bir yerde çalışıyor musunuz: \n"))
    print("\n=============================\n")
    print("\n=============================\n")
    farkli = int(input("\nKaç farklı şirkette çalıştınız: \n"))
    print("\n=============================\n")
    print("\n=============================\n")
    print("Lisans için 0\nYüksek Lisans için 1\nMaster için 2'ye basın")
    egitim = int(input("\nEğitim Seviyeniz nedir: \n"))
    print("\n=============================\n")
    print("\n=============================\n")
    print("Evet için 1\nHayır için 0'a basın\n")
    uni = int(input("\nEn iyi 10 okuldan mı mezunsunuz: \n"))
    print("\n=============================\n")
    print("\n=============================\n")
    print("Evet için 1\nHayır için 0'a basın\n")
    staj = int(input("Stajı bizde mi yaptınız: "))
    print("\n=============================\n")
    print("\n=============================\n")

    if deneyim >= 0 and suan >= 0 and farkli >= 0 and egitim >= 0 and uni >= 0 and staj >= 0:
        sonuc = clf.predict([[deneyim, suan, farkli, egitim, uni, staj]])

        if sonuc == 1:
            print("İşe alındınız, hayırlı olsun.\n\n\n")
            sonuc_str = 'alındı'
        else:
            print("Maalesef işe alınamadınız.\n\n\n")
            sonuc_str = 'alınamadı'
        # MongoDB connection and document insertion
        client = MongoClient('"""Mongodb connection"""')
      
        db = client['my_veri']
        collection = db['veri_seti']

        if suan == 1:
            suan = 'evet'
        elif suan == 0:
            suan = 'hayır'

        if egitim == 0:
            egitim = 'Lisans'
        elif egitim == 1:
            egitim = 'Yüksek Lisans'
        elif egitim == 2:
            egitim = 'Master'

        if uni == 1:
            uni = 'evet'
        elif uni == 0:
            uni = 'hayır'

        if staj == 1:
            staj = 'evet'
        elif staj == 0:
            staj = 'hayır'

        document = {
            'Deneyim (yıl)': deneyim,
            'Suan çalışma durumu': suan,
            'Kaç farklı şirkette çalıştı': farkli,
            'Eğitim Durumu': egitim,
            'En iyi 10 okuldan mezun mu': uni,
            'Stajı girmek istediği şirkette mi yaptı': staj,
            'İşe alındı mı': sonuc_str
        }
        collection.insert_one(document)

        # Close the database connection
        client.close()
        break
    else:
        print("Yanlış değer girdiniz. Tekrar deneyiniz.")
        continue
 