# nexus_utils.py
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

NEXUS_URL = os.getenv('NEXUS_URL')         # Nexus 服务器 URL
NEXUS_USER = os.getenv('NEXUS_USER')       # Nexus 用户名
NEXUS_PASSWORD = os.getenv('NEXUS_PASSWORD')  # Nexus 密码
REPO_NAME = os.getenv('REPO_NAME')

def upload_to_nexus(file_path: str, project: str, version: str):
    """
    上传文件到 Nexus 存储库。

    :param file_path: 本地文件路径
    :param project: project 名称 (相当于仓库名 or repo)
    :param version: 文件版本
    例: url = {NEXUS_URL}/repository/{project}/{version}/{file_name}
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"文件未找到: {file_path}")

    file_name = path.name
    url = f"{NEXUS_URL}/repository/{REPO_NAME}/{project}/{version}/{file_name}"

    headers = {
        'Content-Type': 'application/octet-stream',
    }

    with open(file_path, 'rb') as file:
        response = requests.put(
            url,
            headers=headers,
            data=file,
            auth=HTTPBasicAuth(NEXUS_USER, NEXUS_PASSWORD)
        )

    if response.status_code in [200, 201, 204]:
        print(f"文件 {file_name} 上传成功！ -> {url}")
    else:
        print(f"上传文件失败: {response.status_code} - {response.text}")
        raise Exception(f"上传文件失败: {response.status_code} - {response.text}")


def copy_between_repos(src_repo: str, src_path: str, dest_repo: str, dest_path: str):
    """
    Copy a file between Nexus repositories using streaming.
    """
    src_url = f"{NEXUS_URL}/repository/{src_repo}/{src_path}"
    dest_url = f"{NEXUS_URL}/repository/{dest_repo}/{dest_path}"
    headers = {'Content-Type': 'application/octet-stream'}

    print(f"源文件 URL: {src_url}")
    print(f"目标文件 URL: {dest_url}")

    try:
        with requests.get(src_url, auth=HTTPBasicAuth(NEXUS_USER, NEXUS_PASSWORD), stream=True) as get_resp:
            if get_resp.status_code != 200:
                raise Exception(f"无法从 Nexus 源仓库下载: {get_resp.status_code} - {get_resp.text}")

            print(f"成功从 {src_repo} 下载文件，开始上传到目标仓库...")
            with requests.put(
                dest_url,
                headers=headers,
                data=get_resp.iter_content(chunk_size=8192),
                auth=HTTPBasicAuth(NEXUS_USER, NEXUS_PASSWORD)
            ) as put_resp:
                if put_resp.status_code not in [200, 201, 204]:
                    raise Exception(f"无法上传到目标仓库: {put_resp.status_code} - {put_resp.text}")

    except Exception as e:
        print(f"复制操作失败: {e}")
        raise
    else:
        path = Path(dest_path)
        file_name = path.name
        print(f"文件 {file_name} 已成功从 {src_repo} 复制到 {dest_repo}！")

def download_from_nexus(project: str, version: str, file_name: str, local_dest: str) -> str:
    """
    从 Nexus 仓库中下载指定文件并保存到本地路径。
    1. 构造 Nexus 上文件的 URL
    2. 使用 requests 进行下载（stream 流式下载）
    3. 保存到指定的 local_dest
    4. 返回下载结果
    """

    remote_url = f"{NEXUS_URL}/repository/{REPO_NAME}/{project}/{version}/{file_name}"

    print(f"即将下载: {remote_url}")
    resp = requests.get(remote_url, auth=HTTPBasicAuth(NEXUS_USER, NEXUS_PASSWORD), stream=True)
    if resp.status_code != 200:
        raise Exception(f"无法下载文件: {resp.status_code} - {resp.text}")

    # 将下载内容以二进制写入 local_dest
    with open(local_dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return f"文件已成功下载到 {local_dest}"