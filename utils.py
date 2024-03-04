from bs4 import BeautifulSoup
import requests

def make_request(url, payload):
	response = requests.post(url, data=payload)
	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup
	return None


def find_player_from_overall(soup, overall_rank):
    # Find all 'td' elements with class 'right' that potentially contain the overall rank
    rank_cells = soup.find_all('td', class_='right')
    for rank_cell in rank_cells:
        # Check if this 'td' contains the overall rank we're looking for
        if rank_cell.text.replace(',', '').strip() == str(overall_rank):
            next_sibling = rank_cell.find_next_sibling('td', class_='left')
            if next_sibling and next_sibling.a:
                return next_sibling.a.text.strip().replace('\xa0', ' ') #escape sequence \xa0 and is commonly found in HTML content
    return None


