import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os

# Đọc file CSV và thay thế NaN bằng 0
file_path = '/Users/nangvuong/Documents/CODE PTIT/Python/result.csv'
df = pd.read_csv(file_path, sep=';')
df = df.fillna(0)

# Chọn các cột đại diện cho các thống kê
columns_to_plot = [
    'Non-Penalty Goals', 'Penalty Goals', 'Assists', 'Matches Played',
    'Saves', 'Save%', 'Sh_x', 'SoTA',
    'Total Passes', 'Cmp%', 'xG', 'xAG',
    'Tkl', 'Int', 'Minutes', 'Starts_x',
    'Yellow Cards', 'Red Cards'
]

# Chia thành 2 phần
columns_part1 = columns_to_plot[:9]
columns_part2 = columns_to_plot[9:]

# Chuyển đổi kiểu dữ liệu cho các cột cần thiết thành số
for column in columns_to_plot:
    df[column] = pd.to_numeric(df[column], errors='coerce')

colormap = mcolors.LinearSegmentedColormap.from_list("blue_yellow", ["blue", "yellow"])

# Tạo thư mục lưu hình ảnh nếu chưa tồn tại
output_dir = '/Users/nangvuong/Documents/CODE PTIT/Python/Hình vẽ'
os.makedirs(output_dir, exist_ok=True)

# Hàm vẽ histogram và lưu hình ảnh
def plot_histograms(data, columns, title, file_name):
    num_columns = len(columns)
    n_rows = (num_columns // 3) + (num_columns % 3 > 0)  # Số hàng cần thiết
    plt.figure(figsize=(12, 3 * n_rows))  # Điều chỉnh chiều cao
    for i, column in enumerate(columns, 1):
        plt.subplot(n_rows, 3, i)  # 3 cột
        n, bins, patches = plt.hist(data[column], bins=20, color='skyblue', edgecolor='black')
        for patch, color in zip(patches, colormap(n / np.maximum(n.max(), 1))):  # Tránh chia cho 0
            patch.set_facecolor(color)
        plt.title(column)
        plt.xlabel(column)
        plt.ylabel('Tần suất') 
    plt.tight_layout() 
    plt.suptitle(title, fontsize=16)
    plt.subplots_adjust(top=0.9)
    plt.savefig(file_name)  # Lưu hình ảnh vào file
    plt.close()  # Đóng hình để giải phóng bộ nhớ

# Vẽ histogram cho toàn giải
plot_histograms(df, columns_part1, 'Biểu đồ phân bố cho toàn giải', os.path.join(output_dir, 'distribution_overall_part1.png'))
plot_histograms(df, columns_part2, 'Biểu đồ phân bố cho toàn giải', os.path.join(output_dir, 'distribution_overall_part2.png'))

# Vẽ histogram cho từng đội
teams = df['Team'].unique()
for team in teams:
    team_data = df[df['Team'] == team]
    plot_histograms(team_data, columns_part1, f'Biểu đồ phân bố cho câu lạc bộ {team}', os.path.join(output_dir, f'distribution_{team}_part1.png'))
    plot_histograms(team_data, columns_part2, f'Biểu đồ phân bố cho câu lạc bộ {team}', os.path.join(output_dir, f'distribution_{team}_part2.png'))
