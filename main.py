from fastapi import FastAPI, HTTPException, Query
from nexus_utils import upload_to_nexus, copy_between_repos,download_from_nexus
# from pydantic import BaseModel


app = FastAPI()

@app.post("/upload-to-nexus")
def upload_file_to_nexus(
    file_path: str = Query(..., description="本地文件路径"),
    project: str = Query(..., description="项目名称"),
    version: str = Query(..., description="文件版本号")
):
    """
    接收三个参数：
    1. file_path: 本地文件的路径
    2. project: 项目名称
    3. version: 文件版本
    """

    try:
        result = upload_to_nexus(file_path, project, version)
        return {"message": "upload succeed"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/copy-between-repos")
def copy_between_repos_api(
    src_repo: str = Query(..., description="源仓库名称"),
    src_path: str = Query(..., description="源文件在仓库中的路径"),
    dest_repo: str = Query(..., description="目标仓库名称"),
    dest_path: str = Query(..., description="目标文件在仓库中的路径")
):
    """
    接口说明：
    将文件从一个 Nexus 仓库复制到另一个 Nexus 仓库，
    参数通过 query 方式传递，与 upload 接口方式保持一致。
    """
    try:
        copy_between_repos(src_repo, src_path, dest_repo, dest_path)
        return {"message": "copy succeed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download-from-nexus")
def download_file_from_nexus_api(
    project: str = Query(..., description="项目名称"),
    version: str = Query(..., description="文件版本号"),
    file_name: str = Query(..., description="文件名称"),
    local_dest: str = Query(..., description="本地文件保存路径")
):
    """
    从 Nexus 仓库下载指定文件并保存到本地。
    1. project: 项目名称
    2. version: 文件版本号
    3. file_name: 文件名称
    4. local_dest: 本地保存路径
    """
    try:
        result = download_from_nexus(project, version, file_name, local_dest)
        return {"message": "download succeed"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# 运行服务器：
#   uvicorn main:app --host 0.0.0.0 --port 8000
