#!/usr/bin/env python3
"""
シンプルHTML生成スクリプト

Generated with Claude Code
Date: 2025-06-20
Purpose: エラーのないHTMLを生成
"""

import re
from datetime import datetime

def create_simple_html():
    """シンプルで確実に動作するHTML生成"""
    
    # PROJECT_SUMMARY.mdを読み込み
    with open('/mnt/c/Desktop/Research/PROJECT_SUMMARY.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 現在の日時
    current_date = datetime.now().strftime('%Y年%m月%d日 %H:%M')
    
    # HTMLテンプレート（エスケープ問題回避）
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究プロジェクトまとめ</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #333;
            text-align: center;
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }}
        
        h2 {{
            color: #555;
            margin-top: 30px;
            border-left: 5px solid #667eea;
            padding-left: 15px;
        }}
        
        h3 {{
            color: #666;
            margin-top: 20px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #667eea;
            color: white;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        ul {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        .metric {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 15px;
            margin: 10px;
            border-radius: 5px;
            text-align: center;
        }}
        
        .header-info {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            border-top: 2px solid #667eea;
            color: #666;
        }}
        
        strong {{
            color: #333;
            font-weight: bold;
        }}
        
        @media print {{
            body {{
                background: white;
                font-size: 12pt;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-info">
            <h1>📋 研究プロジェクトまとめ</h1>
            <p><strong>WordNetベースの意味カテゴリ分析を用いた特化型画像分類システム</strong></p>
            <p>生成日時: {current_date}</p>
        </div>"""
    
    # Markdownを手動でHTMLに変換
    lines = md_content.split('\n')
    in_table = False
    in_list = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if in_list:
                html_content += "\n        </ul>"
                in_list = False
            if in_table:
                html_content += "\n        </table>"
                in_table = False
            html_content += "\n"
            continue
        
        # ヘッダー処理
        if line.startswith('# '):
            if line != '# 📋 研究プロジェクトまとめ':  # タイトルは既に表示済み
                html_content += f"\n        <h1>{line[2:]}</h1>"
        elif line.startswith('## '):
            if in_list:
                html_content += "\n        </ul>"
                in_list = False
            html_content += f"\n        <h2>{line[3:]}</h2>"
        elif line.startswith('### '):
            if in_list:
                html_content += "\n        </ul>"
                in_list = False
            html_content += f"\n        <h3>{line[4:]}</h3>"
        
        # テーブル処理
        elif '|' in line and not line.startswith('```'):
            if not in_table:
                html_content += "\n        <table>"
                in_table = True
                is_header = True
            
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            
            # ヘッダー区切り行をスキップ
            if all(set(cell.strip()) <= {'-', ' ', ':'} for cell in cells):
                continue
            
            # 行を追加
            if len(cells) > 0:
                html_content += "\n            <tr>"
                tag = "th" if 'カテゴリ' in cells[0] or 'カテゴリ' in line else "td"
                for cell in cells:
                    # 太字処理
                    cell = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', cell)
                    html_content += f"\n                <{tag}>{cell}</{tag}>"
                html_content += "\n            </tr>"
        
        # リスト処理
        elif line.startswith('- '):
            if in_table:
                html_content += "\n        </table>"
                in_table = False
            if not in_list:
                html_content += "\n        <ul>"
                in_list = True
            
            # 太字処理
            content = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', line[2:])
            html_content += f"\n            <li>{content}</li>"
        
        # 通常のテキスト
        else:
            if in_table:
                html_content += "\n        </table>"
                in_table = False
            if in_list:
                html_content += "\n        </ul>"
                in_list = False
            
            # 太字処理
            content = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', line)
            
            if content and not content.startswith('#'):
                html_content += f"\n        <p>{content}</p>"
    
    # 未閉じのタグを閉じる
    if in_list:
        html_content += "\n        </ul>"
    if in_table:
        html_content += "\n        </table>"
    
    # フッター追加
    html_content += f"""
        
        <div class="footer">
            <p>🤖 Generated with Claude Code - AI支援研究開発プロジェクト</p>
            <p>© 2025 Research Project</p>
        </div>
    </div>
</body>
</html>"""
    
    # HTMLファイルとして保存
    html_file = '/mnt/c/Desktop/Research/PROJECT_SUMMARY_SIMPLE.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"シンプルHTMLファイルを生成しました: {html_file}")
    print("\\n使用方法:")
    print("1. エクスプローラーでファイルをダブルクリック")
    print("2. またはブラウザにファイルをドラッグ&ドロップ")
    print("3. ブラウザで開いたら Ctrl+P でPDF保存")
    
    return html_file

if __name__ == "__main__":
    create_simple_html()