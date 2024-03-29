import os
import re
import geoip2.database
import tkinter as tk
from tkinter import filedialog

def process_files(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
         # 使用正则表达式查找IP地址并去重处理
        ip_addresses = list(set(re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', data)))  # 去重处理

        reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
        country_ip_map = {}
        for ip in ip_addresses:
            try:
                response = reader.country(ip)
                country_code = response.country.iso_code
                if country_code not in country_ip_map:
                    country_ip_map[country_code] = []
                country_ip_map[country_code].append(ip)
            except:
                pass

        folder_name = os.path.splitext(os.path.basename(file_path))[0] + "_processed"
        output_folder = os.path.join(os.path.dirname(file_path), folder_name)
        os.makedirs(output_folder, exist_ok=True)

        for country_code, ips in country_ip_map.items():
            output_filename = os.path.join(output_folder, f'{country_code}.txt')
            with open(output_filename, 'a') as output_file:
                for ip in ips:
                    output_file.write(f'{ip}\n')

        reader.close()

def process_files_in_folder(folder_path):
    output_folder = 'IPV4'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                data = file.read()
                ip_addresses = list(set(re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', data)))  # 去重处理

                reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
                country_ip_map = {}
                for ip in ip_addresses:
                    try:
                        response = reader.country(ip)
                        country_code = response.country.iso_code
                        if country_code not in country_ip_map:
                            country_ip_map[country_code] = []
                        country_ip_map[country_code].append(ip)
                    except:
                        pass

                for country_code, ips in country_ip_map.items():
                    output_filename = os.path.join(output_folder, f'{country_code}.txt')
                    with open(output_filename, 'a') as output_file:
                        for ip in ips:
                            output_file.write(f'{ip}\n')

                reader.close()

    print("任务完成！")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
    if file_path:
        process_files(file_path)
        print("处理完成！")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_files_in_folder(folder_path)
        print("处理完成！")

# 创建 Tkinter 窗口
root = tk.Tk()
root.title("IP 地址处理程序")

# 创建选择文件按钮
select_file_button = tk.Button(root, text="选择文件", command=select_file)
select_file_button.pack(pady=10)

# 创建选择文件夹按钮
select_folder_button = tk.Button(root, text="选择文件夹", command=select_folder)
select_folder_button.pack(pady=10)

root.mainloop()
