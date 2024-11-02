import requests
from bs4 import BeautifulSoup as bs, Comment
import pandas as pd
import time

# URL của trang web
url = 'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats'

# Gửi yêu cầu và lấy nội dung trang web
r = requests.get(url)
soup = bs(r.content, 'html.parser')

# Tìm tất cả các mục <li> trong <ul> sau <p class="listhead">
data = []
for item in soup.find('p', class_='listhead').find_next('ul').find_all('li'):
    title = item.text.strip()  # Lấy tên mục
    link = 'https://fbref.com' + item.find('a')['href']  # Lấy đường dẫn đầy đủ
    data.append({'title': title, 'link': link})  # Lưu vào danh sách dưới dạng từ điển

# Hàm lấy nội dung HTML từ URL
def get_url(url):
    # Gửi yêu cầu đến URL và tạo BeautifulSoup từ nội dung HTML
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    time.sleep(0.5)
    print('Loading...')
    # Tìm tất cả các comment trong nội dung HTML
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    return comments
def get_goalkeeper_stats(comments):
    # Tìm comment chứa bảng thủ môn
    keeper_table = None
    for comment in comments:
        if 'div_stats_keeper' in comment:
            keeper_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng thủ môn nếu tìm thấy
    if keeper_table:
        # Tìm bảng thủ môn
        table = keeper_table.find('table', {'class': 'stats_table'})

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", "birth_year",
            "gk_games", "gk_games_starts", "gk_minutes", "minutes_90s", "gk_goals_against", 
            "gk_goals_against_per90", "gk_shots_on_target_against", "gk_saves", 
            "gk_save_pct", "gk_wins", "gk_ties", "gk_losses", "gk_clean_sheets", 
            "gk_clean_sheets_pct", "gk_pens_att", "gk_pens_allowed", "gk_pens_saved", 
            "gk_pens_missed", "gk_pens_save_pct", "matches"
        ]
        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                # Chỉ lấy dữ liệu từ thẻ có `data-stat`
                if 'data-stat' in th.attrs:
                    row_data.append(th.text.strip())
            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)
        df.rename(columns={
            'player': 'Player',
            "nationality": "Nation",
            "team": "Team",
            "position": "Position",
            "age": "Age",
            "gk_games": "Matches Played",
            "gk_games_starts": "Starts",
            "gk_minutes": "Minutes",
            "gk_goals_against": "GA",
            "gk_goals_against_per90": "GA90",
            "gk_shots_on_target_against": "SoTA",
            "gk_saves": "Saves",
            "gk_save_pct": "Save%",
            "gk_wins": "W",
            "gk_ties": "D",
            "gk_losses": "L",
            "gk_clean_sheets": "CS",
            "gk_clean_sheets_pct": "CS%",
            "gk_pens_att": "PKatt",
            "gk_pens_allowed": "PKA",
            "gk_pens_saved": "PKsv",
            "gk_pens_missed": "PKm",
            "gk_pens_save_pct": "Save%"
        }, inplace=True)
        columns_to_keep = [
            "Player", "Nation", "Team", "Position", "Age",
            "Matches Played", "Starts", "Minutes", 
            "GA", "GA90", "SoTA", "Saves", "Save%",
            "W", "D", "L", "CS", "CS%",
            "PKatt", "PKA", "PKsv", "PKm"
        ]
        df = df[columns_to_keep]
        df = df[~df['Player'].isin(columns_to_keep)]
        df['Nation'] = df['Nation'].str[-3:]
        return df
    else:
        print("Không tìm thấy bảng thủ môn trong trang web.")
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng  
def get_shooting_stats(comments):
    # Tìm comment chứa bảng shooting
    shooting_table = None
    for comment in comments:
        if 'div_stats_shooting' in comment:
            shooting_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng shooting nếu tìm thấy
    if shooting_table:
        # Tìm bảng shooting
        table = shooting_table.find('table', {'class': 'stats_table'})

        if table is None:
            print("Không tìm thấy bảng thống kê shooting.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", "birth_year",
            "minutes_90s", "goals", "shots", "shots_on_target", "shots_on_target_pct",
            "shots_per90", "shots_on_target_per90", "goals_per_shot", 
            "goals_per_shot_on_target", "average_shot_distance", "shots_free_kicks",
            "pens_made", "pens_att", "xg", "npxg", "npxg_per_shot", 
            "g_minus_xg", "npxg_minus_g_minus_xg", "matches"
        ]
        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                # Chỉ lấy dữ liệu từ thẻ có `data-stat`
                if 'data-stat' in th.attrs:
                    row_data.append(th.text.strip())
            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)

        # Đổi tên các chỉ số theo yêu cầu
        df.rename(columns={
            'player': 'Player',
            "nationality": "Nation",
            "team": "Team",
            "position": "Position",
            "age": "Age",
            "shots": "Sh",  # Shots
            "shots_on_target": "SoT",  # Shots on target
            "shots_on_target_pct": "SoT%",  # Shots on target %
            "shots_per90": "Sh/90",  # Shots per 90 minutes
            "shots_on_target_per90": "SoT/90",  # Shots on target per 90 minutes
            "goals": "Gls",  # Goals
            "goals_per_shot": "G/Sh",  # Goals per shot
            "goals_per_shot_on_target": "G/SoT",  # Goals per shot on target
            "average_shot_distance": "Dist",  # Average shot distance
            "shots_free_kicks":'FK',
            "pens_made": "PK", 
            "pens_att": "PKatt_shooting",  # Penalty kicks attempted
            "xg": "xG",  # Expected goals
            "npxg": "npxG",  # Non-penalty expected goals
            "npxg_per_shot": "npxG/Sh",  # Non-penalty expected goals per shot
            "g_minus_xg": "G-xG",  # Goals minus expected goals
            "npxg_minus_g_minus_xg": "np:G-xG",  # Non-penalty expected goals minus Goals minus expected goals
            "matches": "Matches"  # Matches played
        }, inplace=True)

        # Giữ lại chỉ các cột bạn cần
        columns_to_keep = [
            "Player", "Nation", "Team", "Position", "Age", "Gls", "Sh", "SoT", "SoT%", "Sh/90", "SoT/90", "G/Sh", "G/SoT", "Dist", "FK", "PK", "PKatt_shooting",
            "xG", "npxG", "npxG/Sh", "G-xG", "np:G-xG"
        ]

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        df = df[columns_to_keep]  # Chọn giữ lại các cột cần thiết
        df = df[~df['Player'].isin(columns_to_keep)]
        df['Nation'] = df['Nation'].str[-3:]
        return df
    else:
        print("Không tìm thấy bảng shooting trong trang web.")
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng
def get_standard_stats(comments):
    # Tìm comment chứa bảng standard stats
    standard_table = None
    for comment in comments:
        if 'div_stats_standard' in comment:
            standard_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng standard stats nếu tìm thấy
    if standard_table:
        # Tìm bảng standard stats
        table = standard_table.find('table', {'class': 'stats_table'})

        if table is None:
            print("Không tìm thấy bảng thống kê standard.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", "birth_year",
            "games", "games_starts", "minutes", "minutes_90s", "goals", "assists", 
            "goals_assists", "goals_pens", "pens_made", "pens_att", "cards_yellow", 
            "cards_red", "xg", "npxg", "xg_assist", "npxg_xg_assist", 
            "progressive_carries", "progressive_passes", "progressive_passes_received",
            "goals_per90", "assists_per90", "goals_assists_per90", 
            "goals_pens_per90", "goals_assists_pens_per90", "xg_per90", 
            "xg_assist_per90", "xg_xg_assist_per90", "npxg_per90", 
            "npxg_xg_assist_per90", "matches"
        ]
        
        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                # Chỉ lấy dữ liệu từ thẻ có `data-stat`
                if 'data-stat' in th.attrs:
                    row_data.append(th.text.strip())

            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)

        # Đổi tên các chỉ số theo yêu cầu
        df.rename(columns={
            'player': 'Player',
            'nationality': 'Nation',
            'team': 'Team',
            'position': 'Position',
            'age': 'Age',
            'games': 'Matches Played',
            'games_starts': 'Starts',
            'minutes': 'Minutes',
            'goals': 'Non-Penalty Goals',  
            'goals_pens': 'Penalty Goals',  
            'assists': 'Assists',
            'cards_yellow': 'Yellow Cards',
            'cards_red': 'Red Cards',
            'xg': 'xG',
            'npxg': 'npxG',
            'xg_assist': 'xAG',
            'progressive_carries': 'PrgC',
            'progressive_passes': 'PrgP',
            'progressive_passes_received': 'PrgR',
            'goals_per90': 'Gls/90',
            'assists_per90': 'Ast/90',
            'goals_assists_per90': 'G+A/90',
            'goals_pens_per90': 'G-PK/90',
            'goals_assists_pens_per90': 'G+A-PK/90',
            'xg_per90': 'xG/90',
            'xg_assist_per90': 'xAG/90',
            'xg_xg_assist_per90': 'xG + xAG/90',
            'npxg_per90': 'npxG/90',
            'npxg_xg_assist_per90': 'npxG + xAG/90',
        }, inplace=True)

        # Chọn các cột cần thiết theo thứ tự được yêu cầu
        columns_to_keep = [
            'Player', 'Nation', 'Team', 'Position', 'Age', 
            'Non-Penalty Goals', 'Penalty Goals', 'Assists',  # Performance
            'PrgC', 'PrgP', 'PrgR',  # Progression
            'Gls/90', 'Ast/90', 'G+A/90', 'G-PK/90', 'G+A-PK/90',  # Per 90 minutes (Performance)
            'xG/90', 'xAG/90', 'xG + xAG/90', 'npxG/90', 'npxG + xAG/90'  # Per 90 minutes (Expected)
        ]

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        df = df[columns_to_keep]  # Chọn giữ lại các cột cần thiết
        df = df[~df['Player'].isin(columns_to_keep)]
        df['Nation'] = df['Nation'].str[-3:]
        return df
    else:
        print("Không tìm thấy bảng standard trong trang web.")
        return pd.DataFrame() 
def get_passing_stats(comments):
    # Tìm comment chứa bảng passing stats
    passing_table = None
    for comment in comments:
        if 'div_stats_passing' in comment:
            passing_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng passing stats nếu tìm thấy
    if passing_table:
        # Tìm bảng passing stats
        table = passing_table.find('table', {'class': 'stats_table'})

        if table is None:
            print("Không tìm thấy bảng thống kê passing.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", "birth_year",
            "minutes_90s", "passes_completed", "passes", "passes_pct",
            "passes_total_distance", "passes_progressive_distance", "passes_completed_short",
            "passes_short", "passes_pct_short", "passes_completed_medium",
            "passes_medium", "passes_pct_medium", "passes_completed_long",
            "passes_long", "passes_pct_long", "assists", "xg_assist",
            "pass_xa", "xg_assist_net", "assisted_shots", "passes_into_final_third",
            "passes_into_penalty_area", "crosses_into_penalty_area", "progressive_passes",
            "matches"
        ]

        
        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                # Chỉ lấy dữ liệu từ thẻ có `data-stat`
                if 'data-stat' in th.attrs:
                    row_data.append(th.text.strip())

            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)

        # Đổi tên các chỉ số theo yêu cầu (nếu cần thiết)
        df.rename(columns={
            'player': 'Player',
            'nationality': 'Nation',
            'team': 'Team',
            'position': 'Position',
            'age': 'Age',
            'passes_completed': 'Cmp',
            'passes': 'Att',
            'passes_pct': 'Cmp%',
            'passes_total_distance': 'TotDist',
            'passes_progressive_distance': 'PrgDist',
            'passes_completed_short': 'Cmp_Short',
            'passes_short': 'Att_Short',
            'passes_pct_short': 'Cmp%_Short',
            'passes_completed_medium': 'Cmp_Medium',
            'passes_medium': 'Att_Medium',
            'passes_pct_medium': 'Cmp%_Medium',
            'passes_completed_long': 'Cmp_Long',
            'passes_long': 'Att_Long',
            'passes_pct_long': 'Cmp%_Long',
            'assists': 'Ast',
            'xg_assist': 'xAG',
            'pass_xa': 'xA',
            'xg_assist_net': 'A-xAG',
            'assisted_shots': 'KP',
            'passes_into_final_third': '1/3',
            'passes_into_penalty_area': 'PPA',
            'crosses_into_penalty_area': 'CrsPA',
            'progressive_passes': 'PrgP'
        }, inplace=True)

        # Giữ lại chỉ các cột bạn cần (nếu cần)
        columns_to_keep = [
            'Player', 'Nation', 'Team', 'Position', 'Age' , 'Cmp', 'Att', 'Cmp%', 'TotDist', 'PrgDist',
            'Cmp_Short', 'Att_Short', 'Cmp%_Short',
            'Cmp_Medium', 'Att_Medium', 'Cmp%_Medium',
            'Cmp_Long', 'Att_Long', 'Cmp%_Long',
            'Ast', 'xAG', 'xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP'
        ]

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        df = df[columns_to_keep]
        df = df[~df['Player'].isin(columns_to_keep)]
        df['Nation'] = df['Nation'].str[-3:]
        return df
    else:
        print("Không tìm thấy bảng passing trong trang web.")
        return pd.DataFrame()
def get_passing_types_stats(comments):
    # Tìm comment chứa bảng Passing Stats
    passing_table = None
    for comment in comments:
        if 'div_stats_passing_types' in comment:
            passing_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng Passing Stats nếu tìm thấy
    if passing_table:
        # Tìm bảng Passing Stats
        table = passing_table.find('table', {'class': 'stats_table'})

        if table is None:
            print("Không tìm thấy bảng thống kê Passing Stats.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", 
            "birth_year", "minutes_90s", "passes", "passes_live", 
            "passes_dead", "passes_free_kicks", "through_balls", 
            "passes_switches", "crosses", "throw_ins", 
            "corner_kicks", "corner_kicks_in", "corner_kicks_out", 
            "corner_kicks_straight", "passes_completed", "passes_offsides", 
            "passes_blocked", "matches"
        ]

        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for header in headers:
                cell = row.find(attrs={'data-stat': header})
                row_data.append(cell.text.strip() if cell else None)

            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)

        # Đổi tên các chỉ số theo yêu cầu
        df.rename(columns={
            'player': 'Player',
            'nationality': 'Nation',
            'team': 'Team',
            'position': 'Position',
            'age': 'Age',
            'birth_year': 'Birth Year',
            'minutes_90s': 'Minutes (90s)',
            'passes': 'Total Passes',
            'passes_live': 'Live',
            'passes_dead': 'Dead',
            'passes_free_kicks': 'FK_pass',  # Free Kicks
            'through_balls': 'TB',  # Through Balls
            'passes_switches': 'Sw',  # Switches
            'crosses': 'Crs',  # Crosses
            'throw_ins': 'TI',  # Throw Ins
            'corner_kicks': 'CK',  # Total Corners
            'corner_kicks_in': 'In',  # Corners In
            'corner_kicks_out': 'Out',  # Corners Out
            'corner_kicks_straight': 'Str',  # Straight Corners
            'passes_completed': 'Cmp_pass',  # Completed Passes
            'passes_offsides': 'Off',  # Offsides Passes
            'passes_blocked': 'Blocks',  # Blocked Passes
        }, inplace=True)

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        columns_to_keep = [
            'Player', 'Nation', 'Team', 'Position', 'Age',
            'Total Passes', 'Live', 'Dead', 
            'FK_pass', 'TB', 'Sw', 
            'Crs', 'TI', 'CK', 
            'In', 'Out', 'Str', 
            'Cmp_pass', 'Off', 'Blocks'
        ]

        # Sắp xếp lại thứ tự các cột
        df = df[columns_to_keep]
        
        # Loại bỏ hàng không hợp lệ
        df = df[~df['Player'].isin(columns_to_keep)]
        
        # Chuẩn hóa dữ liệu quốc gia
        df['Nation'] = df['Nation'].str[-3:]
        
        return df
    else:
        print("Không tìm thấy bảng Passing Stats trong trang web.")
        return pd.DataFrame()


    # Tìm comment chứa bảng passing types
    passing_types_table = None
    for comment in comments:
        if 'div_stats_passing_types' in comment:
            # Phân tích comment như HTML
            passing_types_table = bs(comment, 'html.parser')
            break
        table = passing_types_table.find('table', {'id': 'stats_passing_types'})

        if table:
            # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
            headers = [
                "ranker", "player", "nationality", "position", "team", "age", "birth_year",
                "minutes_90s", "passes", "passes_live", "passes_dead", "passes_free_kicks", 
                "through_balls", "passes_switches", "crosses", "throw_ins", "corner_kicks", 
                "corner_kicks_in", "corner_kicks_out", "corner_kicks_straight", 
                "passes_completed", "passes_offsides", "passes_blocked", "matches"
            ]

            # Lấy dữ liệu từng hàng trong bảng
            rows = []
            for row in table.find('tbody').find_all('tr'):
                row_data = []
                for th in row.find_all(['th', 'td']):
                    if 'data-stat' in th.attrs:
                        row_data.append(th.text.strip())

                if len(row_data) == len(headers):
                    rows.append(row_data)

            # Tạo DataFrame từ dữ liệu bảng
            df = pd.DataFrame(rows, columns=headers)

            # Đổi tên các chỉ số theo yêu cầu
            df.rename(columns={
                'player': 'Player',
                'nationality': 'Nation',
                'team': 'Team',
                'position': 'Position',
                'age': 'Age',
                'birth_year': 'Birth_Year',
                'passes_completed': 'Cmp',
                'passes': 'Att',
                'passes_live': 'Live',
                'passes_dead': 'Dead',
                'passes_free_kicks': 'FK',
                'through_balls': 'TB',
                'passes_switches': 'Sw',
                'crosses': 'Crs',
                'throw_ins': 'TI',
                'corner_kicks': 'CK',
                'corner_kicks_in': 'In',
                'corner_kicks_out': 'Out',
                'corner_kicks_straight': 'Str',
                'passes_offsides': 'Off',
                'passes_blocked': 'Blocks',
                'matches': 'Matches'
            }, inplace=True)

            # Giữ lại chỉ các cột bạn cần
            columns_to_keep = [
                'Player', 'Nation', 'Team', 'Position', 'Age',
                'minutes_90s', 'Cmp', 'Att', 'Live', 'Dead', 
                'FK', 'TB', 'Sw', 'Crs', 'TI', 'CK', 
                'In', 'Out', 'Str', 'Off', 'Blocks'
            ]
            df = df[columns_to_keep]

            return df
        else:
            print("Không tìm thấy bảng stats_passing_types.")
            return pd.DataFrame()
    else:
        print("Không tìm thấy bảng passing types trong comment.")
        return pd.DataFrame()
def get_gca_stats(comments):
    # Tìm comment chứa bảng GCA
    gca_table = None
    for comment in comments:
        if 'div_stats_gca' in comment:
            gca_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng GCA nếu tìm thấy
    if gca_table:
        # Tìm bảng GCA
        table = gca_table.find('table', {'class': 'stats_table'})

        if table is None:
            print("Không tìm thấy bảng thống kê GCA.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", "birth_year",
            "minutes_90s", "sca", "sca_per90", "sca_passes_live", "sca_passes_dead", 
            "sca_take_ons", "sca_shots", "sca_fouled", "sca_defense",
            "gca", "gca_per90", "gca_passes_live", "gca_passes_dead", 
            "gca_take_ons", "gca_shots", "gca_fouled", "gca_defense", 
            "matches"
        ]

        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                # Chỉ lấy dữ liệu từ thẻ có `data-stat`
                if 'data-stat' in th.attrs:
                    row_data.append(th.text.strip())

            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)

        # Đổi tên các chỉ số theo yêu cầu
        df.rename(columns={
            'player': 'Player',
            'nationality': 'Nation',
            'team': 'Team',
            'position': 'Position',
            'age': 'Age',
            'minutes_90s': 'Minutes (90s)',
            'sca': 'SCA',
            'sca_per90': 'SCA90',
            'sca_passes_live': 'SCA - PassLive',
            'sca_passes_dead': 'SCA - PassDead',
            'sca_take_ons': 'SCA - TO',  # Take-Ons
            'sca_shots': 'SCA - Sh',      # Shots
            'sca_fouled': 'SCA - Fld',    # Fouled
            'sca_defense': 'SCA - Def',    # Defense
            'gca': 'GCA',
            'gca_per90': 'GCA90',
            'gca_passes_live': 'GCA - PassLive',
            'gca_passes_dead': 'GCA - PassDead',
            'gca_take_ons': 'GCA - TO',    # Take-Ons
            'gca_shots': 'GCA - Sh',        # Shots
            'gca_fouled': 'GCA - Fld',      # Fouled
            'gca_defense': 'GCA - Def'      # Defense
        }, inplace=True)

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        columns_to_keep = [
            'Player', 'Nation', 'Team', 'Position', 'Age', 
            'SCA', 'SCA90', 
            'SCA - PassLive', 'SCA - PassDead', 'SCA - TO', 
            'SCA - Sh', 'SCA - Fld', 'SCA - Def',
            'GCA', 'GCA90', 
            'GCA - PassLive', 'GCA - PassDead', 'GCA - TO', 
            'GCA - Sh', 'GCA - Fld', 'GCA - Def', 
        ]

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        df = df[columns_to_keep]
        df = df[~df['Player'].isin(columns_to_keep)]
        df['Nation'] = df['Nation'].str[-3:]
        return df
    else:
        print("Không tìm thấy bảng GCA trong trang web.")
        return pd.DataFrame()
def get_defense_stats(comments):
    # Tìm comment chứa bảng Defense
    defense_table = None
    for comment in comments:
        if 'div_stats_defense' in comment:
            defense_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng Defense nếu tìm thấy
    if defense_table:
        # Tìm bảng Defense
        table = defense_table.find('table', {'class': 'stats_table'})

        if table is None:
            print("Không tìm thấy bảng thống kê Defense.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", "birth_year",
            "minutes_90s", "tackles", "tackles_won", "tackles_def_3rd", 
            "tackles_mid_3rd", "tackles_att_3rd", "challenge_tackles", 
            "challenges", "challenge_tackles_pct", "challenges_lost", 
            "blocks", "blocked_shots", "blocked_passes", "interceptions", 
            "tackles_interceptions", "clearances", "errors", "matches"
        ]

        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                # Chỉ lấy dữ liệu từ thẻ có `data-stat`
                if 'data-stat' in th.attrs:
                    row_data.append(th.text.strip())

            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)

        # Đổi tên các chỉ số theo yêu cầu
        df.rename(columns={
            'player': 'Player',
            'nationality': 'Nation',
            'team': 'Team',
            'position': 'Position',
            'age': 'Age',
            'minutes_90s': 'Minutes (90s)',
            'tackles': 'Tkl',
            'tackles_won': 'TklW',
            'tackles_def_3rd': 'Def 3rd',
            'tackles_mid_3rd': 'Mid 3rd',
            'tackles_att_3rd': 'Att 3rd',
            'challenge_tackles': 'Tkl_challenge',
            'challenges': 'Att',
            'challenge_tackles_pct': 'Tkl%',
            'challenges_lost': 'Lost',
            'blocks': 'Blocks',
            'blocked_shots': 'Sh',
            'blocked_passes': 'Pass',
            'interceptions': 'Int',
            'tackles_interceptions': 'Tkl + Int',
            'clearances': 'Clr',
            'errors': 'Err'
        }, inplace=True)

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        columns_to_keep = [
            'Player', 'Nation', 'Team', 'Position', 'Age', 
            'Tkl', 'TklW', 
            'Def 3rd', 'Mid 3rd', 'Att 3rd', 
            'Tkl_challenge', 'Att', 'Tkl%', 'Lost', 
            'Blocks', 'Sh', 'Pass', 'Int', 
            'Tkl + Int', 'Clr', 'Err',
        ]

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        df = df[columns_to_keep]
        df = df[~df['Player'].isin(columns_to_keep)]
        df['Nation'] = df['Nation'].str[-3:]
        return df
    else:
        print("Không tìm thấy bảng Defense trong trang web.")
        return pd.DataFrame()
def get_possession_stats(comments):
    # Tìm comment chứa bảng Possession
    possession_table = None
    for comment in comments:
        if 'div_stats_possession' in comment:
            possession_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng Possession nếu tìm thấy
    if possession_table:
        # Tìm bảng Possession
        table = possession_table.find('table', {'class': 'stats_table'})

        if table is None:
            print("Không tìm thấy bảng thống kê Possession.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", "birth_year",
            "minutes_90s", "touches", "touches_def_pen_area", "touches_def_3rd", 
            "touches_mid_3rd", "touches_att_3rd", "touches_att_pen_area", 
            "touches_live_ball", "take_ons", "take_ons_won", 
            "take_ons_won_pct", "take_ons_tackled", "take_ons_tackled_pct", 
            "carries", "carries_distance", "carries_progressive_distance", 
            "progressive_carries", "carries_into_final_third", 
            "carries_into_penalty_area", "miscontrols", "dispossessed", 
            "passes_received", "progressive_passes_received", "matches"
        ]

        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                # Chỉ lấy dữ liệu từ thẻ có `data-stat`
                if 'data-stat' in th.attrs:
                    row_data.append(th.text.strip())

            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)

        # Đổi tên các chỉ số theo yêu cầu
        df.rename(columns={
            'player': 'Player',
            'nationality': 'Nation',
            'team': 'Team',
            'position': 'Position',
            'age': 'Age',
            'minutes_90s': 'Minutes (90s)',
            'touches': 'Touches',
            'touches_def_pen_area': 'Def Pen',
            'touches_def_3rd': 'Def 3rd',
            'touches_mid_3rd': 'Mid 3rd',
            'touches_att_3rd': 'Att 3rd',
            'touches_att_pen_area': 'Att Pen',
            'touches_live_ball': 'Live',
            'take_ons': 'Att',
            'take_ons_won': 'Succ',
            'take_ons_won_pct': 'Succ%',
            'take_ons_tackled': 'Tkld',
            'take_ons_tackled_pct': 'Tkld%',
            'carries': 'Carries',
            'carries_distance': 'TotDist',
            'carries_progressive_distance': 'ProDist',
            'progressive_carries': 'ProgC',
            'carries_into_final_third': '1/3',
            'carries_into_penalty_area': 'CPA',
            'miscontrols': 'Mis',
            'dispossessed': 'Dis',
            'passes_received': 'Rec',
            'progressive_passes_received': 'PrgR',
        }, inplace=True)

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        columns_to_keep = [
            'Player', 'Nation', 'Team', 'Position', 'Age', 'Touches', 'Def Pen', 
            'Def 3rd', 'Mid 3rd', 'Att 3rd', 
            'Att Pen', 'Live', 'Att', 
            'Succ', 'Succ%',
            'Carries', 'TotDist', 
            'ProDist', 'ProgC', '1/3', 
            'CPA', 'Mis', 'Dis', 
            'Rec', 'PrgR'
        ]

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        df = df[columns_to_keep]
        df = df[~df['Player'].isin(columns_to_keep)]
        df['Nation'] = df['Nation'].str[-3:]
        return df
    else:
        print("Không tìm thấy bảng Possession trong trang web.")
        return pd.DataFrame()
def get_playing_time_stats(comments):
    # Tìm comment chứa bảng Playing Time
    playing_time_table = None
    for comment in comments:
        if 'div_stats_playing_time' in comment:
            playing_time_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng Playing Time nếu tìm thấy
    if playing_time_table:
        # Tìm bảng Playing Time
        table = playing_time_table.find('table', {'class': 'stats_table'})

        if table is None:
            print("Không tìm thấy bảng thống kê Playing Time.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", "birth_year",
            "games", "minutes", "minutes_per_game", "minutes_pct", "minutes_90s",
            "games_starts", "minutes_per_start", "games_complete", "games_subs",
            "minutes_per_sub", "unused_subs", "points_per_game", "on_goals_for",
            "on_goals_against", "plus_minus", "plus_minus_per90", "plus_minus_wowy",
            "on_xg_for", "on_xg_against", "xg_plus_minus", "xg_plus_minus_per90",
            "xg_plus_minus_wowy", "matches"
        ]

        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                # Chỉ lấy dữ liệu từ thẻ có `data-stat`
                if 'data-stat' in th.attrs:
                    row_data.append(th.text.strip())

            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)

        # Đổi tên các chỉ số theo yêu cầu
        df.rename(columns={
            'player': 'Player',
            'nationality': 'Nation',
            'team': 'Team',
            'position': 'Position',
            'age': 'Age',
            'games': 'Matches',
            'minutes': 'Total Minutes',
            'minutes_per_game': 'Mn/Game',
            'minutes_pct': 'Min %',
            'minutes_90s': '90s',
            'games_starts': 'Starts',
            'minutes_per_start': 'Mn/Start',
            'games_complete': 'Compl',
            'games_subs': 'Subs',
            'minutes_per_sub': 'Mn/Sub',
            'unused_subs': 'unSub',
            'points_per_game': 'PPM',
            'on_goals_for': 'onG',
            'on_goals_against': 'onGA',
            'on_xg_for': 'onxG',
            'on_xg_against': 'onxGA',
            'plus_minus': 'Plus/Minus',
            'plus_minus_per90': 'Plus/Minus/90',
            'plus_minus_wowy': 'Plus/Minus/WoWy',
        }, inplace=True)

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        columns_to_keep = [
            'Player', 'Nation', 'Team', 'Position', 'Age', 'Matches', 'Total Minutes',
            'Mn/Game', 'Min %', '90s', 'Starts', 'Mn/Start', 'Compl',
            'Subs', 'Mn/Sub', 'unSub', 'PPM', 'onG', 'onGA',
            'onxG', 'onxGA', 'Plus/Minus', 'Plus/Minus/90', 'Plus/Minus/WoWy',
        ]

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        df = df[columns_to_keep]
        df = df[~df['Player'].isin(columns_to_keep)]
        df['Nation'] = df['Nation'].str[-3:]
        return df
    else:
        print("Không tìm thấy bảng Playing Time trong trang web.")
        return pd.DataFrame()
def get_misc_stats(comments):
    # Tìm comment chứa bảng Miscellaneous Stats
    misc_stats_table = None
    for comment in comments:
        if 'div_stats_misc' in comment:
            misc_stats_table = bs(comment, 'html.parser')
            break

    # Kiểm tra và xử lý bảng Miscellaneous Stats nếu tìm thấy
    if misc_stats_table:
        # Tìm bảng Miscellaneous Stats
        table = misc_stats_table.find('table', {'class': 'stats_table'})

        if table is None:
            print("Không tìm thấy bảng thống kê Miscellaneous Stats.")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu không tìm thấy bảng

        # Lấy tiêu đề cột từ các thẻ `data-stat` trong hàng tiêu đề
        headers = [
            "ranker", "player", "nationality", "position", "team", "age", "birth_year",
            "minutes_90s", "cards_yellow", "cards_red", "cards_yellow_red", 
            "fouls", "fouled", "offsides", "crosses", "interceptions", 
            "tackles_won", "pens_won", "pens_conceded", "own_goals", 
            "ball_recoveries", "aerials_won", "aerials_lost", "aerials_won_pct", 
            "matches"
        ]

        # Lấy dữ liệu từng hàng trong bảng
        rows = []
        for row in table.find('tbody').find_all('tr'):
            row_data = []
            for th in row.find_all(['th', 'td']):
                # Chỉ lấy dữ liệu từ thẻ có `data-stat`
                if 'data-stat' in th.attrs:
                    row_data.append(th.text.strip())

            # Kiểm tra nếu số lượng cột dữ liệu khớp với headers
            if len(row_data) == len(headers):
                rows.append(row_data)

        # Tạo DataFrame từ dữ liệu bảng
        df = pd.DataFrame(rows, columns=headers)

        # Đổi tên các chỉ số theo yêu cầu
        df.rename(columns={
            'player': 'Player',
            'nationality': 'Nation',
            'team': 'Team',
            'position': 'Position',
            'age': 'Age',
            'birth_year': 'Birth Year',
            'minutes_90s': 'Matches Played (90s)',
            'cards_yellow': 'Yellow Cards',
            'cards_red': 'Red Cards',
            'cards_yellow_red': 'Yellow-Red Cards',
            'fouls': 'Fls',  # Performance: Fls
            'fouled': 'Fld',  # Fld
            'offsides': 'Off',  # Off
            'crosses': 'Crs',  # Crs
            'own_goals': 'OG',  # OG
            'ball_recoveries': 'Recov',  # Recov
            'aerials_won': 'Won',  # Aerial Duels: Won
            'aerials_lost': 'Lost',  # Lost
            'aerials_won_pct': 'Won%',  # Won%
            'matches': 'Matches',
        }, inplace=True)

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        columns_to_keep = [
            'Player', 'Nation', 'Team', 'Position', 'Age', 'Yellow Cards', 'Red Cards', 
            'Yellow-Red Cards', 'Fls', 'Fld', 'Off', 
            'Crs', 'Won', 'Lost', 'Won%', 'Recov',
        ]

        # Lọc DataFrame chỉ giữ lại các cột cần thiết
        df = df[columns_to_keep]
        df = df[~df['Player'].isin(columns_to_keep)]  # Loại bỏ hàng không hợp lệ
        df['Nation'] = df['Nation'].str[-3:]  # Giữ lại 3 ký tự cuối của tên quốc gia
        return df
    else:
        print("Không tìm thấy bảng Miscellaneous Stats trong trang web.")
        return pd.DataFrame()

dataframes = [
    get_standard_stats(get_url(data[0]['link'])),
    get_goalkeeper_stats(get_url(data[1]['link'])),
    get_shooting_stats(get_url(data[3]['link'])),
    get_passing_stats(get_url(data[4]['link'])),
    get_passing_types_stats(get_url(data[5]['link'])),
    get_gca_stats(get_url(data[6]['link'])),
    get_defense_stats(get_url(data[7]['link'])),
    get_possession_stats(get_url(data[8]['link'])),
    get_playing_time_stats(get_url(data[9]['link'])),
    get_misc_stats(get_url(data[10]['link']))
]

# Khởi tạo DataFrame kết quả với DataFrame đầu tiên
df = dataframes[0]

# Gộp tất cả các DataFrame vào df_combined
for df_clone in dataframes[1:]:
    df = pd.merge(df, df_clone, on=['Player', 'Nation', 'Team', 'Position', 'Age'], how='outer')
df['First Name'] = df['Player'].apply(lambda x: x.split()[0])  # Lấy tên đầu tiên

df = df.sort_values(by=['First Name', 'Age'], ascending=[True, False])
df = df.drop(columns=['First Name'])
# Kiểm tra kết quả
df.to_csv('result.csv', sep=';', index=False)
print('Lấy dữ liệu thành công')
