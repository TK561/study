#!/usr/bin/env python3
"""
WordNet階層可視化システム - 完全実装版
WordNetの階層構造を可視化し、インタラクティブに探索できるシステム
"""

import json
import os
from datetime import datetime
from pathlib import Path
import re
from collections import defaultdict, deque

class WordNetHierarchyVisualizer:
    def __init__(self):
        self.name = "WordNet階層可視化システム"
        self.version = "2.0.0"
        self.data_dir = Path("data/wordnet")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = Path("output/visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # WordNet階層データ（簡略版）
        self.wordnet_hierarchy = self._initialize_wordnet_data()
        
    def _initialize_wordnet_data(self):
        """WordNet階層データの初期化（実際のWordNetデータ構造を模倣）"""
        return {
            "entity": {
                "definition": "that which is perceived or known or inferred",
                "children": {
                    "physical_entity": {
                        "definition": "an entity that has physical existence",
                        "children": {
                            "object": {
                                "definition": "a tangible and visible entity",
                                "children": {
                                    "whole": {
                                        "definition": "an assemblage of parts",
                                        "children": {
                                            "artifact": {
                                                "definition": "a man-made object",
                                                "children": {
                                                    "instrumentality": {"definition": "an artifact designed to be used"},
                                                    "structure": {"definition": "a thing constructed"},
                                                    "commodity": {"definition": "articles of commerce"}
                                                }
                                            },
                                            "living_thing": {
                                                "definition": "a living organism",
                                                "children": {
                                                    "organism": {"definition": "a living thing that has the ability to act"},
                                                    "plant": {"definition": "a living organism lacking the power of locomotion"},
                                                    "animal": {"definition": "a living organism characterized by voluntary movement"}
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "substance": {
                                "definition": "the real physical matter",
                                "children": {
                                    "matter": {"definition": "that which has mass and occupies space"},
                                    "food": {"definition": "any substance that can be metabolized"}
                                }
                            }
                        }
                    },
                    "abstraction": {
                        "definition": "a general concept formed by extracting common features",
                        "children": {
                            "attribute": {"definition": "an abstraction belonging to or characteristic of an entity"},
                            "measure": {"definition": "a basis for comparison"},
                            "relation": {"definition": "an abstraction belonging to or characteristic of two entities"}
                        }
                    }
                }
            }
        }
    
    def find_path_to_concept(self, target_concept):
        """特定の概念までのパスを探索"""
        def search_recursive(node, path, target):
            if target.lower() in path[-1].lower():
                return path
            
            if isinstance(node, dict) and 'children' in node:
                for child_name, child_data in node['children'].items():
                    result = search_recursive(child_data, path + [child_name], target)
                    if result:
                        return result
            return None
        
        for root_name, root_data in self.wordnet_hierarchy.items():
            result = search_recursive(root_data, [root_name], target_concept)
            if result:
                return result
        return None
    
    def get_hierarchy_depth(self, node=None, depth=0):
        """階層の深さを計算"""
        if node is None:
            node = self.wordnet_hierarchy
        
        max_depth = depth
        for key, value in node.items():
            if isinstance(value, dict):
                if 'children' in value:
                    child_depth = self.get_hierarchy_depth(value['children'], depth + 1)
                    max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def extract_all_concepts(self, node=None, concepts=None):
        """すべての概念を抽出"""
        if concepts is None:
            concepts = []
        if node is None:
            node = self.wordnet_hierarchy
        
        for key, value in node.items():
            concepts.append({
                'name': key,
                'definition': value.get('definition', '') if isinstance(value, dict) else ''
            })
            if isinstance(value, dict) and 'children' in value:
                self.extract_all_concepts(value['children'], concepts)
        
        return concepts
    
    def generate_hierarchy_html(self):
        """インタラクティブなHTML可視化を生成"""
        html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WordNet階層可視化システム</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .controls {
            margin: 20px 0;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        input[type="text"] {
            padding: 8px;
            width: 300px;
            margin-right: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 8px 15px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
        .hierarchy {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        .node {
            margin: 5px 0;
            padding: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .node:hover {
            background: #e3f2fd;
            border-radius: 4px;
        }
        .node.expanded::before {
            content: "▼ ";
        }
        .node.collapsed::before {
            content: "▶ ";
        }
        .children {
            margin-left: 20px;
            display: none;
        }
        .children.show {
            display: block;
        }
        .definition {
            font-size: 0.9em;
            color: #666;
            font-style: italic;
            margin-left: 20px;
        }
        .path {
            background: #fffbdd;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
            border: 1px solid #ffd700;
        }
        .stats {
            background: #f0f0f0;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <h1>WordNet階層可視化システム</h1>
    
    <div class="controls">
        <h3>概念検索</h3>
        <input type="text" id="searchInput" placeholder="検索する概念を入力（例: animal, artifact）">
        <button onclick="searchConcept()">検索</button>
        <button onclick="expandAll()">すべて展開</button>
        <button onclick="collapseAll()">すべて折りたたむ</button>
    </div>
    
    <div id="searchResult"></div>
    
    <div class="stats">
        <h3>階層統計情報</h3>
        <p>総概念数: <span id="totalConcepts">0</span></p>
        <p>最大階層深度: <span id="maxDepth">0</span></p>
    </div>
    
    <div class="hierarchy" id="hierarchyContainer">
        <h3>WordNet階層構造</h3>
        <div id="hierarchyTree"></div>
    </div>
    
    <script>
        const wordnetData = """ + json.dumps(self.wordnet_hierarchy) + """;
        
        function renderHierarchy(data, container, level = 0) {
            for (const [key, value] of Object.entries(data)) {
                const nodeDiv = document.createElement('div');
                nodeDiv.className = 'node collapsed';
                nodeDiv.style.marginLeft = level * 20 + 'px';
                
                const hasChildren = value.children && Object.keys(value.children).length > 0;
                
                let nodeContent = key.replace(/_/g, ' ');
                if (value.definition) {
                    nodeContent += '<div class="definition">' + value.definition + '</div>';
                }
                
                nodeDiv.innerHTML = nodeContent;
                
                if (hasChildren) {
                    nodeDiv.onclick = function(e) {
                        e.stopPropagation();
                        toggleNode(this);
                    };
                    
                    const childrenDiv = document.createElement('div');
                    childrenDiv.className = 'children';
                    renderHierarchy(value.children, childrenDiv, level + 1);
                    
                    container.appendChild(nodeDiv);
                    container.appendChild(childrenDiv);
                } else {
                    nodeDiv.style.marginLeft = (level * 20 + 20) + 'px';
                    nodeDiv.className = 'node';
                    container.appendChild(nodeDiv);
                }
            }
        }
        
        function toggleNode(node) {
            node.classList.toggle('expanded');
            node.classList.toggle('collapsed');
            const children = node.nextElementSibling;
            if (children && children.classList.contains('children')) {
                children.classList.toggle('show');
            }
        }
        
        function expandAll() {
            document.querySelectorAll('.node.collapsed').forEach(node => {
                node.classList.remove('collapsed');
                node.classList.add('expanded');
            });
            document.querySelectorAll('.children').forEach(children => {
                children.classList.add('show');
            });
        }
        
        function collapseAll() {
            document.querySelectorAll('.node.expanded').forEach(node => {
                node.classList.remove('expanded');
                node.classList.add('collapsed');
            });
            document.querySelectorAll('.children').forEach(children => {
                children.classList.remove('show');
            });
        }
        
        function searchConcept() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const resultDiv = document.getElementById('searchResult');
            
            if (!searchTerm) {
                resultDiv.innerHTML = '';
                return;
            }
            
            const path = findPath(wordnetData, searchTerm);
            if (path) {
                resultDiv.innerHTML = '<div class="path"><strong>パス:</strong> ' + 
                    path.join(' → ') + '</div>';
            } else {
                resultDiv.innerHTML = '<div class="path">概念が見つかりませんでした</div>';
            }
        }
        
        function findPath(data, target, currentPath = []) {
            for (const [key, value] of Object.entries(data)) {
                const newPath = [...currentPath, key];
                if (key.toLowerCase().includes(target)) {
                    return newPath;
                }
                if (value.children) {
                    const result = findPath(value.children, target, newPath);
                    if (result) return result;
                }
            }
            return null;
        }
        
        function countConcepts(data) {
            let count = 0;
            for (const [key, value] of Object.entries(data)) {
                count++;
                if (value.children) {
                    count += countConcepts(value.children);
                }
            }
            return count;
        }
        
        function getMaxDepth(data, depth = 0) {
            let maxDepth = depth;
            for (const [key, value] of Object.entries(data)) {
                if (value.children) {
                    const childDepth = getMaxDepth(value.children, depth + 1);
                    maxDepth = Math.max(maxDepth, childDepth);
                }
            }
            return maxDepth;
        }
        
        // 初期化
        renderHierarchy(wordnetData, document.getElementById('hierarchyTree'));
        document.getElementById('totalConcepts').textContent = countConcepts(wordnetData);
        document.getElementById('maxDepth').textContent = getMaxDepth(wordnetData);
    </script>
</body>
</html>"""
        
        output_path = self.output_dir / "wordnet_hierarchy.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def analyze_concept_relationships(self, concept1, concept2):
        """2つの概念間の関係を分析"""
        path1 = self.find_path_to_concept(concept1)
        path2 = self.find_path_to_concept(concept2)
        
        if not path1 or not path2:
            return {
                "error": "一方または両方の概念が見つかりませんでした",
                "concept1": concept1,
                "concept2": concept2
            }
        
        # 共通の祖先を見つける
        common_ancestor = None
        for i in range(min(len(path1), len(path2))):
            if path1[i] == path2[i]:
                common_ancestor = path1[i]
            else:
                break
        
        return {
            "concept1": {
                "name": concept1,
                "path": path1,
                "depth": len(path1)
            },
            "concept2": {
                "name": concept2,
                "path": path2,
                "depth": len(path2)
            },
            "common_ancestor": common_ancestor,
            "semantic_distance": len(path1) + len(path2) - 2 * path1.index(common_ancestor) if common_ancestor else -1
        }
    
    def export_to_json(self):
        """階層データをJSON形式でエクスポート"""
        export_data = {
            "metadata": {
                "system": self.name,
                "version": self.version,
                "export_date": datetime.now().isoformat(),
                "total_concepts": len(self.extract_all_concepts()),
                "max_depth": self.get_hierarchy_depth()
            },
            "hierarchy": self.wordnet_hierarchy,
            "concepts": self.extract_all_concepts()
        }
        
        output_path = self.output_dir / f"wordnet_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return str(output_path)

def main():
    """実行例"""
    print("🌳 WordNet階層可視化システム 起動")
    print("=" * 50)
    
    visualizer = WordNetHierarchyVisualizer()
    
    # HTML可視化生成
    html_path = visualizer.generate_hierarchy_html()
    print(f"✅ インタラクティブ可視化生成: {html_path}")
    
    # 概念分析例
    print("\n📊 概念関係分析:")
    relationship = visualizer.analyze_concept_relationships("animal", "artifact")
    print(json.dumps(relationship, ensure_ascii=False, indent=2))
    
    # JSONエクスポート
    json_path = visualizer.export_to_json()
    print(f"\n💾 データエクスポート完了: {json_path}")
    
    # 統計情報
    all_concepts = visualizer.extract_all_concepts()
    print(f"\n📈 統計情報:")
    print(f"  総概念数: {len(all_concepts)}")
    print(f"  最大階層深度: {visualizer.get_hierarchy_depth()}")
    
    print("\n✨ システム準備完了")
    print(f"🌐 ブラウザで開く: file://{Path(html_path).absolute()}")

if __name__ == "__main__":
    main()