import os
os.environ["CHROMA_TELEMETRY"] = "false"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

import json
import tqdm
import pickle
import sqlite3
import numpy as np
import networkx as nx
from typing import Dict, Tuple
from streamlit_agraph import agraph, Node, Edge, Config
import rag

class GraphRAG:
    def __init__(self, db_path='mpr.db', kg_json_path='knowledge_graph_model.json'):
        self.kg = nx.DiGraph()
        self.db_path = db_path
        self.kg_json_path = kg_json_path
        self._build_kg_from_db()
        self._build_embeddings()

    def _build_embeddings(self):
        self.node_embeddings = {}
        default_dim = 1536 
        nodes = list(self.kg.nodes)
        
        if not nodes:
            return

        cache_file = "node_embeddings_cache.pkl"
        if os.path.exists(cache_file):
            print(f"⏳ [系统启动] 检测到缓存，正在加载 {len(nodes)} 个节点向量...")
            with open(cache_file, "rb") as f:
                self.node_embeddings = pickle.load(f)
            return

        print(f"⏳ [首次构建] 正在批量计算 {len(nodes)} 个知识节点的全局向量表征，这可能需要一小段时间...")
        
        try:
            results = rag.collection.query(
                query_texts=nodes, 
                n_results=3, 
                include=["embeddings"]
            )
            
            for i, node in tqdm.tqdm(enumerate(nodes), total=len(nodes), desc="计算节点向量ing"):
                if results['embeddings'] and results['embeddings'][i]:
                    # 取相关文本块向量的平均值
                    node_vec = np.mean(results['embeddings'][i], axis=0)
                    self.node_embeddings[node] = node_vec
                else:
                    self.node_embeddings[node] = np.random.rand(default_dim)
            
            with open(cache_file, "wb") as f:
                pickle.dump(self.node_embeddings, f)
            print("✅ [构建完成] 节点向量已全部算完并写入本地缓存！")

        except Exception as e:
            print(f"❌ 批量提取节点向量失败，使用随机值兜底: {e}")
            for node in nodes:
                self.node_embeddings[node] = np.random.rand(default_dim)

    def _build_kg_from_db(self):
        # 1. 构建图谱节点（基于本地 SQLite 的知识点）
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT DISTINCT knowledge_point FROM questions")
        kps = [row[0] for row in c.fetchall() if row[0] != "未分类"]
        conn.close()

        for kp in kps: 
            self.kg.add_node(kp)
            
        # 2. 动态注入大模型抽取的知识图谱边
        if os.path.exists(self.kg_json_path):
            try:
                with open(self.kg_json_path, "r", encoding="utf-8") as f:
                    kg_data = json.load(f)
                    
                added_edges = 0
                for edge in kg_data:
                    u = edge.get("source")
                    v = edge.get("target")
                    weight = edge.get("weight", 0.5)
                    
                    # 根据视觉理解大模型抽取的细粒度图谱，动态扩充节点库
                    if u not in self.kg.nodes:
                        self.kg.add_node(u)
                    if v not in self.kg.nodes:
                        self.kg.add_node(v)
                        
                    self.kg.add_edge(u, v, base_weight=weight)
                    added_edges += 1
                print(f"✅ 成功从 {self.kg_json_path} 加载并关联了 {added_edges} 条有效依赖边。")
            except Exception as e:
                print(f"❌ 读取图谱 JSON 文件失败，退回无连接节点模式: {e}")
        else:
            print(f"⚠️ 未找到 {self.kg_json_path}，当前图谱无前置连边。请运行 data_pipeline.py。")

    def _cosine_sim(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def dynamic_attention_routing(self, target_kp: str, user_bkt_scores: Dict[str, float]) -> Tuple[str, list]:
        if target_kp not in self.kg:
            return target_kp, []

        target_emb = self.node_embeddings.get(target_kp, np.zeros(1536))
        best_candidate = target_kp
        highest_score = -float('inf')
        path_logs = []

        # BFS 队列结构：(当前节点, 深度, 累积衰减率)
        queue = [(target_kp, 0, 1.0)]
        visited = set([target_kp])
        
        # 算法超参
        MAX_DEPTH = 3   # 往前追溯的最大跳数
        GAMMA = 0.7     # 距离衰减因子 (每多一跳，相关性打7折)
        
        # 兜底：如果没有 PageRank 属性，防止报错
        if not hasattr(self, 'pagerank'):
            self.pagerank = {node: 1.0 for node in self.kg.nodes}

        while queue:
            current_node, depth, current_decay = queue.pop(0)

            # 达到最大深度则停止深入
            if depth >= MAX_DEPTH: continue

            # 获取所有前置节点 (DiGraph 中 predecessor 是前置条件)
            predecessors = list(self.kg.predecessors(current_node))

            for pre in predecessors:
                if pre in visited: continue
                visited.add(pre)

                pre_emb = self.node_embeddings.get(pre, np.zeros(1536))
                sim = self._cosine_sim(target_emb, pre_emb)
                base_w = self.kg[pre][current_node].get('base_weight', 0.5)
                
                # 1. 语义与结构相关性 (受距离衰减影响)
                relevance = sim * base_w * current_decay
                
                # 2. 节点图谱影响力 (基石权重)
                pr_weight = self.pagerank.get(pre, 0.0)
                
                # 3. 用户能力画像 (惩罚项：已经掌握的不再推荐)
                bkt_score = user_bkt_scores.get(pre, 0.0) / 100.0

                attention_score = (relevance * 1.0) + (pr_weight * 3.0) - (bkt_score * 1.5)

                path_logs.append({
                    "source": pre, 
                    "target": current_node, 
                    "depth": depth + 1,
                    "score": round(attention_score, 3), 
                    "bkt": round(bkt_score*100, 1),
                    "pr": round(pr_weight, 4)
                })

                if attention_score > highest_score:
                    highest_score = attention_score
                    best_candidate = pre

                queue.append((pre, depth + 1, current_decay * GAMMA))

        path_logs = sorted(path_logs, key=lambda x: x['score'], reverse=True)[:8]
        return best_candidate, path_logs

    def render_routing_visualization(self, target_kp: str, recommended_kp: str, path_logs: list):
        nodes, edges = [], []
        added_nodes = set()
        
        # 目标节点
        nodes.append(Node(id=target_kp, label=f"当前弱项:\n{target_kp}", size=35, color="#FF6B6B", symbolType="diamond"))
        added_nodes.add(target_kp)

        for log in path_logs:
            pre_node = log["source"]
            target_node = log["target"]
            score = log["score"]
            bkt = log["bkt"]
            depth = log.get("depth", 1) 

            if pre_node not in added_nodes:
                if pre_node == recommended_kp:
                    nodes.append(Node(id=pre_node, label=f"★最优降维★\n{pre_node}\n掌握度:{bkt}%", size=45, color="#FFE66D", symbolType="star"))
                else:
                    nodes.append(Node(id=pre_node, label=f"{pre_node}\n跳数:{depth}\n掌握:{bkt}%", size=30, color="#A9B0B0"))
                added_nodes.add(pre_node)
            
            edge_color = "#FFE66D" if pre_node == recommended_kp else "#E0E0E0"
            edge_width = 4 if pre_node == recommended_kp else 1
            edges.append(Edge(source=pre_node, target=target_node, label=f"Attn: {score}", color=edge_color, width=edge_width))

        config = Config(
            width="100%",        
            height=450,
            directed=True,
            physics=True,
            hierarchical=False,  
            nodeHighlightBehavior=True,
            highlightColor="#F7A7A6",
            collapsible=False
        )
        agraph(nodes=nodes, edges=edges, config=config)

    def render_local_map(self, target_kp: str, user_bkt_scores: dict, max_nodes: int = 3):
            """
            当未触发降维时，展示当前知识点的局部微观拓扑图（前置 + 当前 + 后继）及掌握情况
            :param max_nodes: 控制前置和后继节点最多展示的数量，防止图谱过载
            """
            if target_kp not in self.kg:
                return

            nodes, edges = [], []
            added_nodes = set()

            # 1. 定义一个闭包函数，用来根据 BKT 分数动态决定节点颜色和大小
            def get_node_style(node_name):
                score = user_bkt_scores.get(node_name, 15.0)  # 没做过的默认 15 分
                if node_name == target_kp:
                    return "#FF6B6B", 38, "diamond"  # 当前核心练习点：大菱形
                elif score >= 70:
                    return "#00CC96", 28, "circle"   # 已熟练掌握的节点：绿色
                elif score >= 40:
                    return "#FFAA00", 28, "circle"   # 正在提升中的节点：黄色
                else:
                    return "#FF4B4B", 28, "circle"   # 同样薄弱的前置/后继：红色

            # 2. 添加当前目标节点
            color, size, shape = get_node_style(target_kp)
            t_bkt = round(user_bkt_scores.get(target_kp, 0.0), 1)
            nodes.append(Node(id=target_kp, label=f"当前目标:\n{target_kp}\n(掌握:{t_bkt}%)", size=size, color=color, symbolType=shape))
            added_nodes.add(target_kp)

            # 3. 寻找并添加所有直接前置节点（先修条件）
            predecessors = list(self.kg.predecessors(target_kp))[:max_nodes]
            for pre in predecessors:
                p_bkt = round(user_bkt_scores.get(pre, 0.0), 1)
                if p_bkt > 0:
                    if pre not in added_nodes:
                        p_color, p_size, p_shape = get_node_style(pre)
                        p_bkt = round(user_bkt_scores.get(pre, 0.0), 1)
                        nodes.append(Node(id=pre, label=f"前置基础:\n{pre}\n(掌握:{p_bkt}%)", size=p_size, color=p_color, symbolType=p_shape))
                        added_nodes.add(pre)
                    edges.append(Edge(source=pre, target=target_kp, color="#E0E0E0", width=2, label="先修依赖"))

            # 4. 寻找并添加所有直接后继节点（后续延伸）
            successors = list(self.kg.successors(target_kp))[:max_nodes]
            for succ in successors:
                s_bkt = round(user_bkt_scores.get(succ, 0.0), 1)
                if s_bkt > 0:
                    if succ not in added_nodes:
                        s_color, s_size, s_shape = get_node_style(succ)
                        s_bkt = round(user_bkt_scores.get(succ, 0.0), 1)
                        nodes.append(Node(id=succ, label=f"后续延伸:\n{succ}\n(掌握:{s_bkt}%)", size=s_size, color=s_color, symbolType=s_shape))
                        added_nodes.add(succ)
                    edges.append(Edge(source=target_kp, target=succ, color="#A9B0B0", width=1, dashed=True, label="后续解锁"))

            # 5. 配置图谱并渲染
            config = Config(
                width="100%",        
                height=400,
                directed=True,
                physics=True,
                hierarchical={
                    "enabled": True,
                    "direction": "LR",
                    "sortMethod": "directed"
                },
                nodeHighlightBehavior=True,
                highlightColor="#F7A7A6",
                collapsible=False
            )
            agraph(nodes=nodes, edges=edges, config=config)