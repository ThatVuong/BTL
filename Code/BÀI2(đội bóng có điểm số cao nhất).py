import pandas as pd

# Đọc dữ liệu từ file results2.csv
df = pd.read_csv('/Users/nangvuong/Documents/CODE PTIT/Python/results2.csv', sep=';')

# Lọc các cột có chỉ số trung bình
mean_columns = [col for col in df.columns if col.startswith('Mean of')]

# Tìm đội bóng có chỉ số cao nhất ở mỗi chỉ số
team_highest_count = {team: 0 for team in df['Team']}

for col in mean_columns:
    max_value = df[col].max()  # Giá trị cao nhất của chỉ số
    team_with_max_value = df.loc[df[col] == max_value, 'Team'].values[0]  # Tên đội bóng có chỉ số cao nhất
    
    # In ra kết quả mà không có "Mean of" trong tên chỉ số
    statistic_name = col.replace('Mean of ', '')  # Bỏ "Mean of" trong tên chỉ số
    print(f"{statistic_name}: {team_with_max_value}")
    
    # Cập nhật số lượng chỉ số cao nhất cho từng đội
    team_highest_count[team_with_max_value] += 1

# Tìm đội bóng có nhiều chỉ số cao nhất
best_team_count = max(team_highest_count.values())
best_teams = [team for team, count in team_highest_count.items() if count == best_team_count]

# In ra đội bóng có phong độ tốt nhất
print("\nĐội bóng có phong độ tốt nhất giải Ngoại Hạng Anh mùa 2023-2024:")
for team in best_teams:
    print(f"{team} với {best_team_count} chỉ số cao nhất.")
