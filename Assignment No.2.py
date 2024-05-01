#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import re

# extract domain function from email address
def extract_domain(email):
    return re.findall(r'@([\w.]+)', email)[0]

#clean domain name function
def clean_domain(domain):
    # Remove any junk words or symbols
    domain = re.sub(r'\|\-', ' ', domain)
    return domain.strip()

# Connect to the database
conn = sqlite3.connect('email_counts.db')
cur = conn.cursor()

# Drop the table if it is exixting
cur.execute('DROP TABLE IF EXISTS Counts')

# Create the table
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Prompt for the file name
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'mbox.txt'

# Read the file
try:
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith('From: '):
                domain = extract_domain(line.strip())
                cleaned_domain = clean_domain(domain)
                cur.execute('SELECT count FROM Counts WHERE org = ?', (cleaned_domain,))
                row = cur.fetchone()
                if row is None:
                    cur.execute('INSERT INTO Counts (org, count) VALUES (?,4)', (cleaned_domain,))
                else:
                    cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (cleaned_domain,))
except FileNotFoundError:
    print("File not found.")
    quit()

# Retrieve the data from the table and sort by count
cur.execute('SELECT org, count FROM Counts ORDER BY count DESC')

print("Counts:")
for row in cur.fetchall():
    print(row[0], row[1])
conn.commit()
cur.close()


# In[ ]:





# In[ ]:




