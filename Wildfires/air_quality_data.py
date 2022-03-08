import pandas as pd


#Butte County is served by Pacific Gas & Electric (PGE)
#PGE has 16 million customers with 5.4 million electric distribution accounts
#Butte County has a population of 220,000 which represents ~4.1% of the PGE customer base
#Assumption: Butte County energy demand will represent approximately 4.1% of the total PGE energy demand.



reader = pd.read_csv("hourly_44201_2021.csv", chunksize=10**3)
df = pd.concat([x for x in reader], ignore_index=True)


