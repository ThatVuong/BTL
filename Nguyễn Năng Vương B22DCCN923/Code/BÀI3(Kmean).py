import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os

# Đọc file CSV và thay thế NaN bằng 0
file_path = '/Users/nangvuong/Documents/CODE PTIT/Python/result.csv'
df = pd.read_csv(file_path, sep=';')
df = df.fillna(0)

# Danh sách các cột không cần thiết cho phân loại
exclude_columns = ['Player', 'Nation', 'Team', 'Position', 'Age']

# Lấy tất cả các cột số liệu để phân loại, loại bỏ các cột không cần thiết
columns_to_cluster = df.drop(columns=exclude_columns).select_dtypes(include=['float64', 'int64']).columns.tolist()

# Chuyển đổi kiểu dữ liệu cho các cột thành số (nếu cần)
df[columns_to_cluster] = df[columns_to_cluster].apply(pd.to_numeric, errors='coerce')

# Tiền xử lý: Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[columns_to_cluster])

# Áp dụng thuật toán K-means
num_clusters = 3  # Số nhóm bạn muốn phân loại (ví dụ 3)
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Hiển thị kết quả
print(df[['Player', 'Team', 'Cluster'] + columns_to_cluster])

# Tạo thư mục lưu hình ảnh nếu chưa tồn tại
output_dir = '/Users/nangvuong/Documents/CODE PTIT/Python/Hình vẽ'
os.makedirs(output_dir, exist_ok=True)

# Vẽ biểu đồ phân bố nhóm
plt.figure(figsize=(10, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=df['Cluster'], cmap='viridis', marker='o')
plt.title('K-means Clustering of Players')
plt.xlabel('Save')
plt.ylabel('Goals')
plt.colorbar(label='Cluster')

# Lưu hình ảnh vào thư mục
plt.savefig(os.path.join(output_dir, 'kmeans_clustering_players.png'))
plt.close()  # Đóng hình để giải phóng bộ nhớ
