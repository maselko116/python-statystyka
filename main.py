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

#WYKRES 1 suma długości dróg

plt.figure(figsize=(8, 6))
plt.bar(wyniki['kategoria'], wyniki['suma_dlugosci'])
plt.xlabel('Kategoria')
plt.ylabel('Suma Długości Dróg')
plt.title('Suma Długości Dróg według Kategorii')
plt.show()

# WYKRES 2 dla ilości dróg
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

polaczone_dane = pd.merge(ilosc_stacji_na_drodze, drogi, on='id_drogi')
top_5_drogi = polaczone_dane.sort_values(by='ilosc_stacji', ascending=False).head(5)

# WYKRES 3 ilość stacji na drogach
plt.figure(figsize=(10, 6))
plt.bar(top_5_drogi['nazwa'], top_5_drogi['ilosc_stacji'])
plt.xlabel('nazwa')
plt.ylabel('Ilość Stacji')
plt.title('Top 5 Drog według Ilości Stacji')
plt.xticks(rotation=45)  
plt.show()


print(wyniki)

najdluzsze_drogi = drogi_z_kategoriami.loc[drogi_z_kategoriami.groupby('kategoria')['dlugosc'].idxmax()]

# WYKRES 4
plt.figure(figsize=(10, 6))
plt.bar(najdluzsze_drogi['kategoria'], najdluzsze_drogi['dlugosc'])
plt.xlabel('Kategoria Drogowa')
plt.ylabel('Długość Drogi w km')
plt.title('Najdłuższe Drogi w Każdej Kategorii')
plt.xticks(najdluzsze_drogi['kategoria'])
plt.show()