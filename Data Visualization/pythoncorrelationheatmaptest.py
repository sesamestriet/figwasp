import seaborn
import pandas as pd

df = pd.read_excel('correlationtest.xlsx')

print(df.corr())