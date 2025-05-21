import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Send a request to the webpage and fetch the HTML content
url = 'https://www.cmegroup.com/markets/metals/base/copper.settlements.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Step 2: Extract the table data
# The copper settlement data is in a table with class 'market-data-table'
table = soup.find('table', {'class': 'market-data-table'})

# Step 3: Parse the table headers
headers = []
for th in table.find_all('th'):
    headers.append(th.get_text(strip=True))

# Step 4: Parse the table rows (data)
data = []
for tr in table.find_all('tr')[1:]:  # Skipping the header row
    row = [td.get_text(strip=True) for td in tr.find_all('td')]
    if row:
        data.append(row)

# Step 5: Create a pandas DataFrame from the extracted data
df = pd.DataFrame(data, columns=headers)

# Step 6: Write the DataFrame to an Excel file, adding a new sheet
excel_filename = 'copper_settlements.xlsx'
with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Copper Settlements', index=False)

print(f"Data has been successfully scraped and saved to {excel_filename}.")