import requests
from bs4 import BeautifulSoup
import re

def fetch_and_extract_data(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    data = []
    # Find all 'td' elements which seem to contain the information for each faculty member
    faculty_members = soup.find_all('td', valign='top')
    
    for member in faculty_members:
        # Extract name
        name = member.find('strong').get_text(strip=True)
        
        # Extract phone
        phone_tag = member.find('a', href=re.compile(r'^tel:'))
        phone = phone_tag.get_text(strip=True) if phone_tag else None

        # Extract email and replace placeholders with actual characters
        email_tag = member.find('a', href=re.compile(r'^mailto:'))
        email_raw = email_tag.get_text(strip=True) if email_tag else None
        email = email_raw.replace(' at ', '@').replace(' dot ', '.').replace(' ', '') if email_raw else None

        if name and phone and email:
            data.append((name, phone, email))

    return data

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write('Name Phone Email\n')
        for name, phone, email in data:
            file.write(f'{name} {phone} {email}\n')

url = 'http://cs.qau.edu.pk/faculty.php'
filename = 'faculty_contact_info.txt'

extracted_data = fetch_and_extract_data(url)
save_data_to_file(extracted_data, filename)

print('Data has been successfully extracted and saved.')
