import logging
import azure.functions as func
import json
from azure.cosmos import CosmosClient

import os

def main(blob: func.InputStream):
    logging.info(f"Processing blob: {blob.name}, Size: {blob.length} bytes")
    
    # 1. CSV 내용 가져오기
    contents = blob.read().decode('utf-8').splitlines()

    # 2. 헤더 분리
    header = contents[0].split(',')
    rows = contents[1:]

    # 3. Cosmos DB 연결
    endpoint = os.environ["COSMOS_DB_ENDPOINT"]
    key = os.environ["COSMOS_DB_KEY"]
    client = CosmosClient(endpoint, key)
    database = client.get_database_client("babblee")
    container = database.get_container_client("steps")

    # 4. 행마다 문서로 저장
    for line in rows:
        values = line.split(',')
        doc = {header[i]: values[i] for i in range(len(header))}
        container.upsert_item(doc)

    logging.info("✅ CSV 파일이 Cosmos DB에 저장되었습니다.")


        


    
