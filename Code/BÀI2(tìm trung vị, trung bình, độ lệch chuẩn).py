import pandas as pd

# Đọc dữ liệu từ file result.csv
df = pd.read_csv('/Users/nangvuong/Documents/CODE PTIT/Python/result.csv', sep=';')

# Thay thế các giá trị NaN bằng 0
df.fillna(0, inplace=True)

# Lọc các cột chỉ số cần tính toán
stat_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Tính các giá trị thống kê cho toàn bộ giải
overall_stats = {
    'Team': ['All'],
    **{f'Median of {col}': [round(df[col].median(), 2)] for col in stat_columns},
    **{f'Mean of {col}': [round(df[col].mean(), 2)] for col in stat_columns},
    **{f'Std of {col}': [round(df[col].std(), 2)] for col in stat_columns}
}

# Tạo DataFrame cho thống kê toàn bộ giải
overall_df = pd.DataFrame(overall_stats)

# Tính các giá trị thống kê cho từng đội
team_stats = df.groupby('Team').agg(
    **{f'Median of {col}': (col, lambda x: round(x.median(), 2)) for col in stat_columns},
    **{f'Mean of {col}': (col, lambda x: round(x.mean(), 2)) for col in stat_columns},
    **{f'Std of {col}': (col, lambda x: round(x.std(), 2)) for col in stat_columns}
).reset_index()

# Gộp dữ liệu toàn bộ giải và từng đội lại
final_df = pd.concat([overall_df, team_stats], ignore_index=True)

# Ghi kết quả ra file results2.csv
final_df.to_csv('/Users/nangvuong/Documents/CODE PTIT/Python/results2.csv', sep=';', index=False)
