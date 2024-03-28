import os
import requests
import zipfile

# 设置代理信息
proxy_host = "127.0.0.1"
proxy_port = 7897
proxies = {
    'http': f'socks5://{proxy_host}:{proxy_port}',
    'https': f'socks5://{proxy_host}:{proxy_port}'
}

# 获取当前工作目录
current_dir = os.getcwd()

# 下载文件
url = "https://zip.baipiao.eu.org/"
response = requests.get(url, proxies=proxies, verify=True)  # 设置verify=True进行SSL证书验证
with open(os.path.join(current_dir, "txt.zip"), "wb") as file:
    file.write(response.content)

# 检查文件是否为ZIP文件
if not zipfile.is_zipfile(os.path.join(current_dir, "txt.zip")):
    print("下载的文件不是一个有效的ZIP文件。")
else:
    # 解压文件到txt文件夹
    with zipfile.ZipFile(os.path.join(current_dir, "txt.zip"), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(current_dir, "txt"))

    # 删除原始压缩文件
    os.remove(os.path.join(current_dir, "txt.zip"))

    print("文件下载并解压完成。")

# 删除txt.zip文件
if os.path.exists(os.path.join(current_dir, "txt.zip")):
    os.remove(os.path.join(current_dir, "txt.zip"))
    print("已删除txt.zip文件。")
