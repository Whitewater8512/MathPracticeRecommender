import networkx as nx
import chromadb
from sentence_transformers import SentenceTransformer

class MathGraphRAG:
    def __init__(self):
        # 1. 初始化轻量级知识图谱
        self.kg = nx.DiGraph()
        self._build_math_kg()
        
        # 2. 初始化向量库 (复用你原有的 Chroma 逻辑)
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        # 这里假设已经连上了你原有的 collection
        
    def _build_math_kg(self):
        """构建高数知识点的前驱后继关系"""
        edges = [
            ("函数极限", "连续、间断与导数", "前提"),
            ("数列极限", "函数极限", "相关"),
            ("连续、间断与导数", "导数应用", "前置"),
            ("连续、间断与导数", "中值定理", "前置"),
            ("导数应用", "积分", "基础"),
        ]
        for u, v, rel in edges:
            self.kg.add_edge(u, v, relation=rel)

    def retrieve_with_graph(self, current_kp, top_k=2):
        """Graph-RAG 核心逻辑：获取当前节点 + 邻居节点的信息"""
        # 1. 在图谱中寻找关联知识点 (例如找它的前置知识点)
        related_kps = [current_kp]
        if current_kp in self.kg:
            # 获取前驱节点（基础）和后继节点（进阶）
            predecessors = list(self.kg.predecessors(current_kp))
            successors = list(self.kg.successors(current_kp))
            related_kps.extend(predecessors + successors)
            
        print(f"Graph-RAG 扩展检索路径: {' -> '.join(related_kps)}")
        
        # 2. 将扩展后的知识点一起送入向量库进行混合检索
        # (此处省略具体的 Chroma query 代码，将 related_kps 拼接成 query_texts 即可)
        return related_kps # 返回给 LLM 作为上下文提示