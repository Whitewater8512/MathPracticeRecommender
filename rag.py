import os
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# os.environ["TRANSFORMERS_OFFLINE"] = "1"
# os.environ["HF_HUB_OFFLINE"] = "1"

import torch
import chromadb
from chromadb.utils import embedding_functions
from typing import List

GOLD_DATA_FOLDER = "datas/gold"
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "math_textbooks"

DEVICE = "cuda" if __name__ == "__main__" and torch.cuda.is_available() else "cpu"

client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

class SafeEmbeddingFunction:
    def __init__(self, device: str):
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(
            "./Alibaba-NLP/gte-Qwen2-1.5B-instruct",
            device=device,
            model_kwargs={"torch_dtype": torch.float16},
        )
        self._device = device

    def _encode_safe(self, texts: List[str], device: str) -> list:
        self._model.to(device)
        with torch.no_grad():
            embeddings = self._model.encode(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=True,
                batch_size=4
            )
        return embeddings.tolist()

    def __call__(self, input: List[str]):
        with torch.no_grad():                          # 禁止梯度累积
            embeddings = self._model.encode(
                input,
                convert_to_numpy=True,
                normalize_embeddings=True,
                batch_size=4                           # 模型内部分批，防单次爆显存
            )
        if self._device == "cuda":
            torch.cuda.empty_cache()                   # 每次 encode 后立即释放碎片
        return embeddings.tolist()

    def embed_query(self, input: List[str]):
        return self.__call__(input)
    
    def embed_documents(self, input: List[str]):
        return self.__call__(input)

def get_embedding_function():
    return SafeEmbeddingFunction(device=DEVICE)

embedding_func = get_embedding_function()
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_func,
    metadata={"description": "高数语义向量库"}
)

def load_gold_chunks_to_vector_db():
    if not os.path.exists(GOLD_DATA_FOLDER):
        print(f"⚠️ 数据目录 {GOLD_DATA_FOLDER} 不存在，请先运行 data_pipeline.py")
        return

    gold_files = [f for f in os.listdir(GOLD_DATA_FOLDER) if f.endswith(".md")]
    if not gold_files: return

    try:
        existing_data = collection.get(include=["metadatas"])
        processed_files = {
            meta["source_chunk"] for meta in existing_data.get("metadatas", [])
            if meta and "source_chunk" in meta
        }
    except Exception:
        processed_files = set()

    pending_files = [f for f in gold_files if f not in processed_files]
    if not pending_files:
        print("✅ 所有切片已入库，无需重复处理。")
        return

    print(f"📥 待处理切片: {len(pending_files)} 个")
    documents, metadatas, ids = [], [], []

    for i, chunk_file in enumerate(pending_files):
        chunk_path = os.path.join(GOLD_DATA_FOLDER, chunk_file)
        try:
            with open(chunk_path, "r", encoding="utf-8") as f:
                content = f.read()
            if not content.strip():
                continue

            documents.append(content)
            original_doc = chunk_file.split("_chunk_")[0] + ".md"
            metadatas.append({"source": original_doc, "source_chunk": chunk_file})
            ids.append(chunk_file)

            # ✅ 批大小改为 8，写入后立即清空列表和显存
            if len(documents) >= 8:
                collection.add(documents=documents, metadatas=metadatas, ids=ids)
                documents, metadatas, ids = [], [], []
                if DEVICE == "cuda":
                    torch.cuda.empty_cache()
                print(f"   ✅ 已处理 {i+1}/{len(pending_files)} 个切片")

        except Exception as e:
            print(f"❌ 读取切片失败 {chunk_file}: {e}")
            documents, metadatas, ids = [], [], []   # 出错也要清空，防止脏数据混入
            if DEVICE == "cuda":
                torch.cuda.empty_cache()

    if documents:
        collection.add(documents=documents, metadatas=metadatas, ids=ids)

    print("🎉 全部切片入库完成！")

def retrieve_relevant_context(query: str, top_k: int = 2) -> str:
    if collection.count() == 0:
        return ""
    results = collection.query(query_texts=[query], n_results=top_k)
    context_list = results['documents'][0] if results['documents'] else []
    return "\n---\n".join(context_list)

def get_knowledge_base_stats() -> dict:
    if collection is None:
        return {"total_chunks": 0, "total_files": 0, "files": []}
    try:
        total_chunks = collection.count()
        if total_chunks == 0:
            return {"total_chunks": 0, "total_files": 0, "files": []}
        existing_data = collection.get(include=["metadatas"])
        metadatas = existing_data.get("metadatas", [])
        unique_files = {meta.get("source", "Unknown") for meta in metadatas if meta}
        return {"total_chunks": total_chunks, "total_files": len(unique_files), "files": sorted(list(unique_files))}
    except Exception as e:
        print(f"统计数据获取失败: {e}")
        return {"total_chunks": 0, "total_files": 0, "files": []}

if __name__ == "__main__":
    print("🔍 正在检查并加载 Gold 切片到向量数据库...")
    load_gold_chunks_to_vector_db()
else:
    stats = get_knowledge_base_stats()
    print(f"📊 当前知识库状态: {stats['total_chunks']} chunks from {stats['total_files']} files.")
