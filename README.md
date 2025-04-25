# Nexus 文件管理 API 使用说明

该 Python 环境 API 用于对 Nexus 仓库进行文件操作，提供以下功能：

1. **上传文件**
   - 将本地文件上传至 Nexus 仓库
2. **复制文件**
   - 将文件从一个 Nexus 仓库复制到另一个 Nexus 仓库
3. **下载文件**
   - 将文件从 Nexus 仓库下载到本地

---

## 前置准备

### 1. 配置环境变量

在.env文件中将NEXUS_URL，NEXUS_USER，NEXUS_PASSWORD，REPO_NAME改掉，REPO_NAME就是下载和上传的默认仓库

- **示例**

REPO_NAME=release-repo-hosted

NEXUS_URL=http://10.86.9.179:8081
NEXUS_USER=admin
NEXUS_PASSWORD=siouxnexusadminpw0106



### 2. 安装依赖并启动服务

在终端中运行以下命令，请确保你已经配置好 Python 和 pip：

```bash
pip install -r ./requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000  # 将 host 替换为你的内网IP或者云服务器Ip
```
---

## API调用说明及示例

---

### 1. 上传文件接口

**接口说明：**

- **URL:** /upload-to-nexus  
- **方法:** POST  
- **参数（query方式）：**
  - file_path: 本地文件路径  
  - project: 项目名称  
  - version: 文件版本号  

**调用示例：**

```bash
curl -X POST "http://<服务器IP>:8000/upload-to-nexus?file_path=C:/Users/xxxx/testfiles/app.jar&project=my-project&version=1.0.0"
```
-**Notes:** `这会将本地文件路径的文件上传到该nexus仓库的/project/version路径中`

### 2. 复制文件接口

**接口说明：**

- **URL:** `/copy-between-repos`  
- **方法:** `POST`  
- **参数（query方式）：**
  - `src_repo`: 源仓库名称  
  - `src_path`: 源文件在仓库中的路径  
  - `dest_repo`: 目标仓库名称  
  - `dest_path`: 目标文件在仓库中的路径  

**调用示例：**
```bash
curl -X POST "http://<服务器IP>:8000/copy-between-repos?src_repo=review-repo-hosted&src_path=my-project/1.0.0/install.jar&dest_repo=release-repo-hosted&dest_path=my-project/1.0.0/install.jar"
```
-**Notes:** 这会将review-repo-hosted的my-project/1.0.0/install.jar文件上传到release-repo-hosted的my-project/1.0.0/install.jar路径中

### 3. 下载文件接口

**接口说明：**

- **URL:** /download-from-nexus
- **方法:** GET  
- **参数（query方式）：**
  - project: 项目名称  
  - version: 文件版本号  
  - file_name: 项目名称  
  - local_dest: 本地文件保存路径  


**调用示例：**

```bash
curl -X GET "http://<服务器IP>:8000/download-from-nexus?project=my-project&version=1.0.0&file_name=install.jar&local_dest=C:/Users/xxxx/testfiles/testinstall.jar"
```
-**Notes:** `这会将nexus仓库里/my-project/1.0.0的install.jar文件上传到本地C:/Users/xxxx/testfiles路径，并且作为testinstall.jar保存
