import pandas as pd
import matplotlib.pyplot as plt
# sieci = pd.read_csv('dane/sieci.csv', sep=',')
# kategorie = pd.read_csv('dane/kategorie.csv', sep=',')
drogi = pd.read_csv('dane/drogi.csv', sep="\t")
kategorie = pd.read_csv('dane/kategorie.csv', sep="\t")
stacje = pd.read_csv('dane/stacje.csv', sep="\t")

# stacje = pd.read_csv('dane/stacje.csv', sep=',')


drogi_z_kategoriami = pd.merge(drogi,kategorie, on= 'id_kategorii')



typy_drog = drogi['id_kategorii']



#print(drogi.sort_values(by='dlugosc', ascending=False))

grupowane = drogi_z_kategoriami.groupby('kategoria')
wyniki = grupowane.agg({'dlugosc': 'sum', 'id_drogi': 'count'}).reset_index()
wyniki = wyniki.rename(columns={'dlugosc': 'suma_dlugosci', 'id_drogi': 'ilosc_drog'})

#print(wyniki)

plt.figure(figsize=(8, 6))
plt.bar(wyniki['kategoria'], wyniki['suma_dlugosci'])
plt.xlabel('Kategoria')
plt.ylabel('Suma Długości Dróg')
plt.title('Suma Długości Dróg według Kategorii')
plt.show()

# Tworzenie wykresu słupkowego dla ilości dróg
plt.figure(figsize=(8, 6))
plt.bar(wyniki['kategoria'], wyniki['ilosc_drog'])
plt.xlabel('Kategoria')
plt.ylabel('Ilość Dróg')
plt.title('Ilość Dróg według Kategorii')
plt.show()

stacje_z_drogami = pd.merge(drogi,stacje, on= 'id_drogi')
# grupowane2 = stacje_z_drogami.groupby('id_drogi')
# wyniki2 = grupowane2.agg({'id_drogi': 'count'}).reset_index()
# print(wyniki2)

ilosc_stacji_na_drodze = stacje_z_drogami.groupby('id_drogi')['id_stacji'].count().reset_index()
ilosc_stacji_na_drodze = ilosc_stacji_na_drodze.rename(columns={'id_stacji': 'ilosc_stacji'})

print(ilosc_stacji_na_drodze.head(5).sort_values(by='ilosc_stacji', ascending=False))


