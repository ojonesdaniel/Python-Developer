# Databricks notebook source
import requests
import re
import urllib.parse
from typing import List, Dict

# COMMAND ----------

# ===============================
# CONFIGURAÇÕES DA WIKI AZURE DEVOPS
# ===============================

ORGANIZATION = ""
PROJECT = ""
WIKI = ""


BASE_URL = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis/wiki/wikis/{WIKI}"
API_VERSION = "7.0"

PAT = ""  # COLOCAR SEU TOKEN

HEADERS = {
    "Authorization": f"Basic {PAT}",
    "Content-Type": "application/json"
}


# COMMAND ----------

def get_wiki_tree_root():
    url = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis/wiki/wikis/{WIKI}/pages"
    
    params = {
        "api-version": "5.0",
        "path": "/",
        "recursionLevel": "full",
        "includeContent": "false"
    }

    resp = requests.get(url, params=params, auth=("", PAT))
    resp.raise_for_status()
    return resp.json()

# COMMAND ----------

def flatten_pages(root_page):
    pages = []

    def dfs(page):
        pages.append(page)
        for child in page.get("subPages", []):
            dfs(child)

    dfs(root_page)
    return pages

# COMMAND ----------

root = get_wiki_tree_root()
pages = flatten_pages(root)

folder_root = "/Documentações/Tabelas"

subtree = [
    p for p in pages
    if p.get("path", "").startswith(folder_root)
]

leaf_pages = [
    p for p in subtree
    if not p.get("subPages")
]

print(f"Total de páginas finais: {len(leaf_pages)}")

# COMMAND ----------

def extract_from_path(path):
    parts = path.strip("/").split("/")
    
    return {
        "camada": parts[-3],
        "sistema": parts[-2],
        "tabela": parts[-1]
    }

# COMMAND ----------

def get_page_content(page_path):
    encoded_path = urllib.parse.quote(page_path)

    url = (
        f"{BASE_URL}/pages"
        f"?path={encoded_path}&includeContent=true&api-version=7.0"
    )

    response = requests.get(url, auth=("", PAT))

    if response.status_code != 200:
        print(f"Erro {response.status_code} ao acessar: {page_path}")
        return ""

    return response.json().get("content", "")

# COMMAND ----------

import re

def parse_flag_and_percentual(text):
    if not text:
        return None, None

    text_upper = text.upper()

    flag = None
    percentual = None

    # Detectar cor
    if "VERMELHO" in text_upper or "🔴" in text:
        flag = "Vermelho"
    elif "AMARELO" in text_upper or "🟡" in text:
        flag = "Amarelo"
    elif "VERDE" in text_upper or "🟢" in text:
        flag = "Verde"

    # Detectar percentual (ex: 100%)
    match = re.search(r'(\d{1,3})\s*%', text)
    if match:
        percentual = float(match.group(1))

    return flag, percentual


# COMMAND ----------

records = []

for p in leaf_pages:
    path_info = extract_from_path(p["path"])
    content = get_page_content(p["path"])
    flag, percentual = parse_flag_and_percentual(content)

    records.append({
        "camada": path_info["camada"],
        "sistema": path_info["sistema"],
        "tabela": path_info["tabela"],
        "flag": flag,
        "percentual": percentual
    })

df = pd.DataFrame(records)
df


# COMMAND ----------

spark_df = spark.createDataFrame(records)
spark_df.display()