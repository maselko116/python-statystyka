import pandas as pd
import matplotlib.pyplot as plt
# sieci = pd.read_csv('dane/sieci.csv', sep=',')
# kategorie = pd.read_csv('dane/kategorie.csv', sep=',')
drogi = pd.read_csv('python-statystyka-master/dane/drogi.csv', sep="\t")
kategorie = pd.read_csv('python-statystyka-master/dane/kategorie.csv', sep="\t")
stacje = pd.read_csv('python-statystyka-master/dane/stacje.csv', sep="\t")

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



#WYKRES

srednia_ilosc_stacji_na_drodze = ilosc_stacji_na_drodze / drogi['dlugosc']


# WYKRES 4


plt.figure(figsize=(10, 6))
plt.bar(najdluzsze_drogi['kategoria'], najdluzsze_drogi['dlugosc'])
plt.xlabel('Kategoria Drogowa')
plt.ylabel('Długość Drogi w km')
plt.title('Najdłuższe Drogi w Każdej Kategorii')
plt.xticks(najdluzsze_drogi['kategoria'])
plt.show()

najdluzsze_drogi = drogi.groupby('id_kategorii').apply(lambda x: x.nlargest(3, 'dlugosc')).reset_index(drop=True)



#WYKRES 5

plt.figure(figsize=(10, 6))
colors = ['coral', 'lightblue', 'lightgreen', 'magenta']


for kategoria, colors in zip(najdluzsze_drogi['id_kategorii'].unique(), colors):
    subset = najdluzsze_drogi[najdluzsze_drogi['id_kategorii'] == kategoria]
    
    plt.bar(subset['nazwa'], subset['dlugosc'], color=colors, label=f'kategoria {kategoria}')

plt.xlabel('Nazwa Drogi')
plt.ylabel('Długość Drogi')
plt.title('3 Najdłuższe Drogi dla Każdej Kategorii')
plt.xticks(rotation=45)
plt.legend()
plt.show()



#WYKRES 6 

# dlugosci = stacje_z_drogami.groupby('nazwa')['id_stacji'].count().reset_index()

# srednia_odleglosc = stacje_z_drogami.groupby('nazwa')['id_stacji'].count().reset_index()
# srednia_odleglosc = srednia_odleglosc.rename(columns={'id_stacji': 'ilosc_stacji'})
# srednia_odleglosc['srednia_odleglosc'] = srednia_odleglosc['ilosc_stacji'] / dlugosci['dlugosc']

# # Tworzenie wykresu
# plt.figure(figsize=(10, 6))
# plt.bar(srednia_odleglosc['nazwa'], srednia_odleglosc['srednia_odleglosc'], color='lightblue')
# plt.xlabel('Nazwa Drogi')
# plt.ylabel('Średnia Odległość od Stacji')
# plt.title('Średnia Odległość od Stacji na Drodze')
# plt.xticks(rotation=45)
# plt.show()

stacje_per_droga = stacje.groupby('id_drogi').size().reset_index(name='liczba_stacji')
drogi_stacje = pd.merge(drogi, stacje_per_droga, on='id_drogi', how='left')
drogi_stacje['srednia_odleglosc'] = drogi_stacje.apply(
    lambda row: row['dlugosc'] / (row['liczba_stacji'] - 1) if row['liczba_stacji'] > 1 else None, axis=1
)
drogi_stacje = drogi_stacje.dropna(subset=['srednia_odleglosc'])

# Wybór dróg z największą liczbą stacji
top_drogi_stacje = drogi_stacje.nlargest(10, 'liczba_stacji')

# Tworzenie wykresu
fig, ax1 = plt.subplots(figsize=(14, 7))

# Słupki dla długości drogi
ax1.bar(top_drogi_stacje['nazwa'], top_drogi_stacje['dlugosc'], color='blue', alpha=0.6)
ax1.set_xlabel('Nazwa Drogi')
ax1.set_ylabel('Długość Drogi (km)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_xticklabels(top_drogi_stacje['nazwa'], rotation=90)

# Linia dla liczby stacji
ax2 = ax1.twinx()
ax2.plot(top_drogi_stacje['nazwa'], top_drogi_stacje['liczba_stacji'], color='red', marker='o')
ax2.set_ylabel('Liczba Stacji', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Legenda
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='best')

plt.title('Długość i liczba stacji na najbardziej zatłoczonych drogach')
ax1.grid(True)
plt.tight_layout()
plt.show()