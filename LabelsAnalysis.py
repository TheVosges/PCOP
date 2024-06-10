import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import ast

script_dir = os.path.dirname(__file__)
annotations_folder = os.path.join(script_dir, "../../datasets/PCOP")
annotations = {}
with open(annotations_folder + "/anns.json") as json_file:
    annotations = json.load(json_file)

all_labels = [label for sublist in annotations.values() for label in ast.literal_eval(sublist)]
label_counts = Counter(all_labels)
label_counts = {label: count for label, count in label_counts.items() if count >= 20}
label_counts = Counter(label_counts)
# for keyword, count in label_counts.items():
#     print(keyword, ":", count)
print(label_counts.keys())
print(len(label_counts.keys()))

top_20_keywords = label_counts.most_common(20)
labels, counts = zip(*top_20_keywords)
print(labels)
plt.figure(figsize=(10, 6))
plt.bar(labels, counts, color='skyblue')
plt.xlabel('Wartość')
plt.ylabel('Ilość wystąpień')
plt.title('Histogram 20 najczęściej występujących wartości')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

