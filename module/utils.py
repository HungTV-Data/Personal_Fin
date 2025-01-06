import requests
from bs4 import BeautifulSoup
import time

def get_logo_links(url):
    start = time.time()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    logo_links = soup.find_all('a')
    download_links = {}
    for link in logo_links:
        logo_page_url = link.get('href')
        if logo_page_url in ('/', '#', '/about.html', '/logos/index.html', '/support/index.html', 'https://github.com/VectorLogoZone/vectorlogozone/blob/main/CONTRIBUTING.md'\
                             , '/report/index.html', '/index.html', 'https'):
            continue
        else:
            # print(logo_page_url)
            response_child = requests.get('https://www.vectorlogo.zone'+logo_page_url)
            # print('https://www.vectorlogo.zone'+logo_page_url)
            soup_child = BeautifulSoup(response_child.content, 'html.parser')
            table = soup_child.find('table', attrs={'class':'table table-striped border-bottom'})
            tbody = table.find('tbody')
            for row in tbody.find_all('tr'):
                # print(row)
                row_name = row.find('td', attrs={'class':'d-none d-sm-table-cell'}).text.strip()
                if 'icon' in str.lower(row_name):
                    logo_link = row.find('td', attrs={'class':'d-none d-md-table-cell'}).find('button', attrs={'class': 'btn btn-secondary btn-sm copy2cb'}).get('data-clipboard-text')
                else:
                    continue
                download_links[row_name] = logo_link
        print(f"Time taken: {time.time()-start}")
    return download_links            


    #     logo_page_response = requests.get(logo_page_url)
    #     logo_page_soup = BeautifulSoup(logo_page_response.content, 'html.parser')
        
    #     download_button = logo_page_soup.select_one('a.btn-download')
    #     if download_button:
    #         download_link = download_button.get('href')
    #         logo_name = logo_page_soup.select_one('h1').text.strip()
    #         download_links[logo_name] = download_link

    # return download_links

if __name__ == "__main__":
    url = 'https://www.vectorlogo.zone/logos/'
    download_links = get_logo_links(url)
    for name, link in download_links.items():
        print(f"{name}: {link}")