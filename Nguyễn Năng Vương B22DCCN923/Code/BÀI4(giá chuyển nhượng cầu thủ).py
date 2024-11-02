from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def read_url(url):
    driver = webdriver.Safari()
    driver.get(url)
    time.sleep(5)  # Đợi trang tải xong
    page_source = driver.page_source
    driver.quit()
    soup = bs(page_source, 'html.parser')
    return soup

def extract_player_data(soup):
    players = []
    
    # Lấy tất cả các hàng có dữ liệu cầu thủ
    rows = soup.select('tr')  # Giả định mỗi cầu thủ nằm trong một hàng <tr>
    
    for row in rows:
        # Tên cầu thủ
        name_tag = row.select_one('td.td-player span[aria-hidden="false"]')
        player_name = name_tag.get_text(strip=True) if name_tag else 'N/A'

        # Đội bóng
        team_tag = row.select_one('td.td-team a .td-team__teamname')
        team_name = team_tag.get_text(strip=True) if team_tag else 'N/A'

        # Giá trị chuyển nhượng
        price_tag = row.select_one('span.player-tag')
        transfer_value = price_tag.get_text(strip=True) if price_tag else 'N/A'

        if player_name != 'N/A' and team_name != 'N/A' and transfer_value != 'N/A':
            players.append({
                'Player Name': player_name,
                'Team': team_name,
                'Transfer Value': transfer_value
            })
        
    
    return players

# Tạo DataFrame rỗng để lưu dữ liệu
all_players_data = pd.DataFrame(columns=['Player Name', 'Team', 'Transfer Value'])

# Đọc dữ liệu từ trang 1
url_page_1 = 'https://www.footballtransfers.com/en/values/players/most-valuable-players/playing-in-uk-premier-league'
soup_page_1 = read_url(url_page_1)
players_data_page_1 = extract_player_data(soup_page_1)
all_players_data = pd.concat([all_players_data, pd.DataFrame(players_data_page_1)], ignore_index=True)

# Đọc dữ liệu từ trang 2 đến trang 24
for page in range(2, 25):
    url = f'https://www.footballtransfers.com/en/values/players/most-valuable-players/playing-in-uk-premier-league/{page}'
    soup = read_url(url)
    players_data = extract_player_data(soup)
    all_players_data = pd.concat([all_players_data, pd.DataFrame(players_data)], ignore_index=True)
    print(f"Data from page {page} added to DataFrame.")

# Lưu dữ liệu vào file CSV
output_path = '/Users/nangvuong/Documents/CODE PTIT/Python/test.csv'
all_players_data.to_csv(output_path, sep=';', index=False, encoding='utf-8')
print(f"Data saved to {output_path}")
