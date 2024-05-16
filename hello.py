#libraries Here
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  #For parsing HTML
import re  #regular expressions



#Functions part here
# Function to get faculty data
def get_faculty_data(site_url):
    #requesting the specified url here
    response = requests.get(site_url)
    # now from response getting html content
    html_content = response.text
    # Now parsing the content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initializing an empty list 
    faculty_data = []
    
    #As i have inspected the page 'td' contains the info for faculty data so getting it
    members = soup.find_all('td', valign='top')
    
    # now iterating over each faculty data
    for member in members:
        # name of member
        faculty_name = member.find('strong').get_text(strip=True)
        
        # phone number
        phone_tag = member.find('a', href=re.compile(r'^tel:'))
        faculty_phone = phone_tag.get_text(strip=True) if phone_tag else None

        # email of the  member and replacing it actual characters
        email_tag = member.find('a', href=re.compile(r'^mailto:'))
        email_raw = email_tag.get_text(strip=True) if email_tag else None
        faculty_email = email_raw.replace(' at ', '@').replace(' dot ', '.').replace(' ', '') if email_raw else None

       # If all necessary information (name, phone, email) is available, add it to the list
        if faculty_name and faculty_phone and faculty_email:
            faculty_data.append((faculty_name, faculty_phone, faculty_email))

    # Returning the list which contains faculty data
    return faculty_data




# Function to save faculty data to a file
def save_faculty_data(data, output_filename):
    # Opening it to the output file in write mode
    with open(output_filename, 'w') as file:
        # Writing the header row format
        file.write('Name Phone Email\n')
        # now iterating over each tuple in the data list
        for name, phone, email in data:
            # Writing each faculty member's information to the file
            file.write(f'{name} {phone} {email}\n')


#defining files info here

# URL of cs faculty info
url = 'http://cs.qau.edu.pk/faculty.php'

# Output filename for saving the extracted data
filename = 'faculty_contact_info.txt'


# calling the function to get faculty data
faculty_info = get_faculty_data(url)
# Calling the function to save the extracted data to the file
save_faculty_data(faculty_info, filename)

# message indicating that the process is complete
print('Faculty contact information extracted and saved successfully.')
