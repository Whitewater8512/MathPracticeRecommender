class ConceptGraphKT:
    def __init__(self, nx_graph):
        self.graph = nx_graph
        
    def update_user_state(self, user_history_records):
        for node in self.graph.nodes:
            self.graph.nodes[node]['mastery'] = 0.15 
            
        gamma = 0.6
        for kp, is_correct in user_history_records:
            if kp not in self.graph: continue
            current_mastery = self.graph.nodes[kp]['mastery']
            
            if is_correct == 1:
                gain = (1.0 - current_mastery) * 0.35
                self.graph.nodes[kp]['mastery'] += gain
                for pre in self.graph.predecessors(kp):
                    w = self.graph[pre][kp].get('base_weight', 0.5)
                    self.graph.nodes[pre]['mastery'] += gain * w * gamma
            else:
                loss = current_mastery * 0.25
                self.graph.nodes[kp]['mastery'] -= loss
                for succ in self.graph.successors(kp):
                    w = self.graph[kp][succ].get('base_weight', 0.5)
                    self.graph.nodes[succ]['mastery'] -= loss * w * gamma
                    
            for node in self.graph.nodes:
                self.graph.nodes[node]['mastery'] = max(0.0, min(1.0, self.graph.nodes[node]['mastery']))
                
        return {node: self.graph.nodes[node]['mastery'] * 100 for node in self.graph.nodes}