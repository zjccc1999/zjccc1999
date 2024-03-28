import pandas as pd
import os
import random
# 假设您的CSV文件是以'gbk'编码的
csv_encoding = 'gbk'  # 如果是其他编码，请将'gbk'改为正确的编码
csv_dir = 'C:\\\\Users\\\\Administrator\\\\Desktop\\\\反代IP库'
csv_files = [file for file in os.listdir(csv_dir) if file.endswith('.csv')]
first_csv = random.choice(csv_files)
header = None
# 尝试使用确定的编码打开文件
try:
    with open(os.path.join(csv_dir, first_csv), 'r', encoding=csv_encoding) as file:
        header = file.readline().strip().split(',')
except UnicodeDecodeError as e:
    print(f"读取{first_csv}出错: {e}。请检查文件的编码。")
if header:
    combined_csv = pd.DataFrame(columns=header)
    for file in csv_files:
        temp_df = pd.read_csv(os.path.join(csv_dir, file), skiprows=1, names=header, encoding=csv_encoding)
        combined_csv = pd.concat([combined_csv, temp_df])
    if '速度(MB/s)' in combined_csv.columns:
        sorted_csv = combined_csv.sort_values('速度(MB/s)', ascending=False)
    else:
        print("列 '速度(MB/s)' 不存在，请检查CSV文件。")
        # 如果不存在则不排序
        sorted_csv = combined_csv
# 输出最终合并后的CSV文件
output_file = os.path.join(csv_dir, 'combined_sorted.csv')
sorted_csv.to_csv(output_file, index=False, encoding=csv_encoding)
print(f'CSV文件合并和排序已经完成。文件保存为：{output_file}')
