import pandas as pd
# sieci = pd.read_csv('dane/sieci.csv', sep=',')
# kategorie = pd.read_csv('dane/kategorie.csv', sep=',')
drogi = pd.read_csv('dane/drogi.csv', sep="\t")
# stacje = pd.read_csv('dane/stacje.csv', sep=',')

# print(sieci.index)
# print(kategorie.index)
# print(drogi.index)
# print(stacje.index)

#print(drogi.head())
#print(drogi['tid_kategorii'])
#print(drogi.value_counts())
typy_drog = drogi['id_kategorii']
print(typy_drog)

print(drogi.value_counts().head(10))
