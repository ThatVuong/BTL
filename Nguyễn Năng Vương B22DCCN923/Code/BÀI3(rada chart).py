import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

# Hàm để vẽ radar chart
def radar_chart(player1_data, player2_data, attributes, player1_name, player2_name):
    num_vars = len(attributes)

    # Tạo góc cho mỗi trục trong radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Hoàn tất vòng radar bằng cách quay về điểm đầu
    player1_data += player1_data[:1]
    player2_data += player2_data[:1]
    angles += angles[:1]

    # Vẽ radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, player1_data, color="blue", alpha=0.25, label=player1_name)
    ax.fill(angles, player2_data, color="red", alpha=0.25, label=player2_name)

    # Vẽ đường bao quanh các giá trị của từng cầu thủ
    ax.plot(angles, player1_data, color="blue", linewidth=2, label=player1_name)
    ax.plot(angles, player2_data, color="red", linewidth=2, label=player2_name)

    # Thêm nhãn cho mỗi trục
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)

    # Thêm tiêu đề và chú thích
    plt.title(f'So sánh cầu thủ {player1_name} và {player2_name}')
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    plt.show()

# Hàm chính để nhận input và xử lý dữ liệu
def main():
    parser = argparse.ArgumentParser(description='Radar Chart Comparison for Two Players')
    parser.add_argument('--p1', required=True, help='Tên cầu thủ thứ nhất')
    parser.add_argument('--p2', required=True, help='Tên cầu thủ thứ hai')
    parser.add_argument('--Attribute', required=True, help='Danh sách các chỉ số cần so sánh, cách nhau bởi dấu phẩy')
    args = parser.parse_args()

    player1_name = args.p1
    player2_name = args.p2
    attributes = args.Attribute.split(';')

    # Đọc dữ liệu từ file CSV và chuyển NaN thành 0
    df = pd.read_csv('result.csv', sep=';')
    df = df.fillna(0)  # Chuyển NaN thành 0

    # Kiểm tra sự tồn tại của các cầu thủ
    if player1_name not in df['Player'].values:
        print(f"Lỗi: Cầu thủ {player1_name} không tồn tại trong dữ liệu.")
        return
    if player2_name not in df['Player'].values:
        print(f"Lỗi: Cầu thủ {player2_name} không tồn tại trong dữ liệu.")
        return

    # Kiểm tra sự tồn tại của các chỉ số
    for attr in attributes:
        if attr not in df.columns:
            print(f"Lỗi: Chỉ số {attr} không tồn tại trong dữ liệu.")
            return

    # Lấy dữ liệu của hai cầu thủ và các chỉ số cần so sánh
    player1_data = df[df['Player'] == player1_name][attributes].values.flatten().tolist()
    player2_data = df[df['Player'] == player2_name][attributes].values.flatten().tolist()

    # Kiểm tra số lượng dữ liệu
    if len(player1_data) == 0 or len(player2_data) == 0:
        print("Lỗi: Dữ liệu không đầy đủ cho một trong hai cầu thủ.")
        return

    # Gọi hàm vẽ radar chart
    radar_chart(player1_data, player2_data, attributes, player1_name, player2_name)

if __name__ == '__main__':
    main()

# python3 "/Users/nangvuong/Documents/CODE PTIT/Python/BÀI3(rada chart).py" --p1 "Erling Haaland" --p2 "Mohamed Salah" --Attribute "Gls/90;Ast/90;G+A/90;G-PK/90;G+A-PK/90;xG/90;xAG/90;xG + xAG/90"
