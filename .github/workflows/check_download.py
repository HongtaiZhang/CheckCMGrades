import os
import time
import requests
from pathlib import Path

def download_if_available(url, download_folder=None):
    if download_folder is None:
        # 获取系统默认的下载文件夹
        download_folder = str(Path.home() / "Downloads")
    
    # 从URL提取文件名
    filename = os.path.basename(url)
    save_path = os.path.join(download_folder, filename)
    
    try:
        # 发送HEAD请求检查文件是否可用
        response = requests.head(url, allow_redirects=True, timeout=10)
        
        if response.status_code == 200:
            # 如果可用，发送GET请求下载文件
            print(f"文件可用，开始下载: {url}")
            response = requests.get(url, allow_redirects=True, timeout=10)
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            print(f"文件已下载到: {save_path}")
            return True
        else:
            print(f"文件尚不可用 (HTTP状态码: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"检查/下载过程中出错: {e}")
        return False

def main():
    url = "https://www.comap-math.org/mcm/2025Certs/2528079.pdf"
    check_interval = 15 * 60  # 15分钟，以秒为单位
    
    print(f"开始监控URL: {url}")
    print(f"检查间隔: {check_interval/60}分钟")
    print(f"文件将下载到: {Path.home() / 'Downloads'}")
    print("按Ctrl+C停止监控...")
    
    while True:
        try:
            if download_if_available(url):
                print("下载成功！")
                break  # 下载成功后退出循环
                
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            print("\n监控已停止")
            break

if __name__ == "__main__":
    main()
