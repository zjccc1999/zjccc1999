import tkinter as tk
from tkinter import filedialog
import csv
import os
import datetime

COUNTRY_CODES = {
    "HK": "香港",
    "DE": "德国",
    "GB": "英国",
    "TW": "台湾",
    "SG": "新加坡阿里云notls",
    "KR": "韩国",
    "US": "美国",
    "JP": "日本阿里云notls",
    "FR": "法国",
    "NL": "荷兰",
    # 添加更多国家代码和对应的国家名称
    # "OTHER_CODE": "OTHER_NAME",
}

def extract_ip_and_port_with_country(file_name):
    ip_and_port_with_country = []
    country_data = {}  # 用于存储每个国家的数据
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # 跳过第一行
        next(reader)
        for row in reader:
            ip = row[0].replace(" ", "")
            port = row[1].replace(",", "")
            country = row[4].replace(" ", "")
            country_code = COUNTRY_CODES.get(country, country)
            if country_code not in country_data:
                country_data[country_code] = []
            country_data[country_code].append((ip, port, country))
    return country_data

def process_csv(file_path):
    country_data = extract_ip_and_port_with_country(file_path)

    # 获取当前日期（年月日）
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")

    # 获取文件名（不含扩展名）和扩展名
    base_name, _ = os.path.splitext(os.path.basename(file_path))

    for country_code, ip_ports in country_data.items():
        output_file_name = f"{base_name}_{country_code}_{date_str}.txt"
        with open(output_file_name, 'w', encoding='utf-8') as output_file:
            index = 1  # 序号从1开始
            for ip, port, country in ip_ports:
                output_file.write(f"{ip}:{port}#{country_code}_{index}\n")
                index += 1

    print("处理后的数据已保存到文件中。")

def select_file():
    file_path = filedialog.askopenfilename(title="选择CSV文件", filetypes=[("CSV files", "*.csv")])
    if file_path:
        process_csv(file_path)

# 创建Tkinter窗口
root = tk.Tk()
root.title("选择CSV文件")

# 添加选择文件按钮
select_button = tk.Button(root, text="选择CSV文件", command=select_file)
select_button.pack(pady=20)

root.mainloop()
