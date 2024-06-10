import networkx as nx
import matplotlib.pyplot as plt

# Etykiety
labels = [
    'wynagrodzenia', 'służba wojskowa żołnierzy', 'żołnierz zawodowy', 'fundusze', 'inwestycje',
    'pomoc finansowa', 'ochrona środowiska', 'podatki', 'lotnicze prawo', 'opłaty', 'kontrola', 'szkolnictwo',
    'egzaminy', 'oświata i wychowanie', 'nauczyciele', 'umowy międzynarodowe', 'podatek dochodowy od osób fizycznych',
    'ewidencja', 'podatek od towarów i usług', 'rolnictwo', 'rozwój obszarów wiejskich', 'nadzór', 'kwalifikacje',
    'dokumenty', 'świadczenia lecznicze', 'choroby zakaźne', 'opieka zdrowotna', 'ochrona zdrowia', 'ochrona przyrody',
    'rolnicy', 'formularze', 'programy wieloletnie', 'produkty rolne', 'prawo o ruchu drogowym', 'niepełnosprawni',
    'samorząd terytorialny', 'dotacje', 'wybory', 'pojazdy mechaniczne', 'wojsko', 'cudzoziemcy', 'obrona narodowa',
    'sądy powszechne', 'finanse publiczne', 'budżet', 'rolne prawo', 'rejestry', 'systemy teleinformatyczne',
    'informatyzacja', 'emerytury i renty', 'przedsiębiorstwa', 'ubezpieczenia społeczne', 'bankowe prawo',
    'ratownictwo', 'budowlane prawo', 'energetyka', 'kredyty i pożyczki', 'badania lekarskie', 'gminy', 'praca',
    'podatek dochodowy od osób prawnych', 'planowanie społeczno-gospodarcze', 'paliwa', 'lekarze', 'szkolnictwo wyższe',
    'funkcjonariusz publiczny', 'prokuratura', 'odpady', 'energetyczna gospodarka', 'energetyczne prawo', 'szkolenie zawodowe',
    'świadczenia', 'naczelne i centralne organy administracji', 'dzieci', 'leki i artykuły sanitarne', 'pomoc publiczna',
    'uposażenie', 'finansowanie', 'organizacja i zakres działania', 'stawki', 'statut', 'ministrowie'
]

# Tworzenie grafu
G = nx.Graph()

# Dodawanie węzłów do grafu
G.add_nodes_from(labels)

# Definiowanie krawędzi na podstawie podobieństwa etykiet
# Tutaj można zaimplementować własną logikę definiującą podobieństwo między etykietami
for label1 in labels:
    for label2 in labels:
        if label1 != label2:
            if 'ochrona środowiska' in label1 and 'ochrona środowiska' in label2:
                G.add_edge(label1, label2)
            elif label1.startswith('ochrona') and label2.startswith('ochrona'):
                G.add_edge(label1, label2)

# Rysowanie grafu
plt.figure(figsize=(20, 20))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Mapa etykiet", fontsize=20)
plt.show()
