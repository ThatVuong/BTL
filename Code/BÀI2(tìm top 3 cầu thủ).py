import pandas as pd

# Đọc file result.csv
df = pd.read_csv('/Users/nangvuong/Documents/CODE PTIT/Python/result.csv', sep=';')

# Lọc các cột chỉ số cần xếp hạng
stat_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Lưu trữ kết quả
top3_high = {}
top3_low = {}

for col in stat_columns:
    # Tìm top 3 cầu thủ có điểm cao nhất ở chỉ số `col`
    top3_high[col] = df.nlargest(3, col)[['Player', col]]
    
    # Tìm top 3 cầu thủ có điểm thấp nhất ở chỉ số `col`
    top3_low[col] = df.nsmallest(3, col)[['Player', col]]

# Hiển thị kết quả
for col in stat_columns:
    print(f"Top 3 cầu thủ có {col} cao nhất:")
    print(top3_high[col])
    print(f"\nTop 3 cầu thủ có {col} thấp nhất:")
    print(top3_low[col])
    print("\n")
