# HTML Parsing

import requests
from bs4 import BeautifulSoup

print('\n\n\n\n')
url = "https://www.thenewboston.com/forum/topic.php?id=1610"
source_code = requests.get(url)
plain_text = source_code.text
soup = BeautifulSoup(plain_text)
results = soup.find_all("code")
for line in results[0]:
    line_str = str(line)
    code_line = line_str.replace("<br>", '\n')
    code_line = code_line.replace("</br>", '').replace('\ufffd', ' ')
    print(code_line)


