import datasets
import os
import pandas

script_dir = os.path.dirname(__file__)
dataset_folder = os.path.join(script_dir, "../../datasets/PCOP/data")
annotations_folder = os.path.join(script_dir, "../../datasets/PCOP")
output_folder = os.path.join(script_dir, "../../datasets/PCOP")

dataset = datasets.load_from_disk(annotations_folder)

dataset.set_format(type="pandas")
df = dataset[:]
print(df.head())