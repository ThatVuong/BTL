import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os

# Đọc file CSV và thay thế NaN bằng 0
file_path = 'result.csv'
df = pd.read_csv(file_path, sep=';')
df = df.fillna(0)

# Danh sách các cột không cần thiết cho phân loại
exclude_columns = ['Player', 'Nation', 'Team', 'Position', 'Age']

# Lấy tất cả các cột số liệu để phân loại, loại bỏ các cột không cần thiết
columns_to_cluster = df.drop(columns=exclude_columns).select_dtypes(include=['float64', 'int64']).columns.tolist()

# Tiền xử lý: Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[columns_to_cluster])

# Áp dụng thuật toán PCA để giảm số chiều xuống 2
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Áp dụng thuật toán K-means
num_clusters = 4  # Số nhóm bạn muốn phân loại
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Tạo thư mục lưu hình ảnh nếu chưa tồn tại
output_dir = '/Users/nangvuong/Documents/CODE PTIT/Python/Hình vẽ'
os.makedirs(output_dir, exist_ok=True)

# Vẽ hình phân cụm trên mặt phẳng 2D
plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['Cluster'], cmap='viridis', alpha=0.7)

# Thêm nhãn cho các trục
plt.title('PCA - K-means Clustering of Players (2D)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(scatter, label='Cluster')
plt.grid(True)
plt.show()

# Lưu hình ảnh vào thư mục
plt.savefig(os.path.join(output_dir, 'pca_kmeans_clustering_players.png'))
plt.close()  # Đóng hình để giải phóng bộ nhớ
