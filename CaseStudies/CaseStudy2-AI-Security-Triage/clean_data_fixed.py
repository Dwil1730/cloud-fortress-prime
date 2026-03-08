import pandas as pd
df = pd.read_csv('tickets.csv')
df = df.dropna(subset=['Category', 'Outcome'])
df['text'] = df['Category'].astype(str) + ' ' + df['Sub Category'].astype(str) + ' ' + df['Outcome'].astype(str) + ' ' + df['Priority'].astype(str) + ' ' + df['Skill Team'].astype(str)
df = df[df['text'].str.len() > 20]
df.to_csv('clean_tickets.csv', index=False)
print("Cleaned dataset:", len(df), "rows")
print("Columns:", df.columns.tolist())
