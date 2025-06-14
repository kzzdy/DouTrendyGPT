import requests
import os

# 请将你的扣子API和OpenAI API密钥填入下方
KOUZI_API_KEY = os.getenv('KOUZI_API_KEY', 'your_kouzi_api_key')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

# 获取抖音热门内容（示例API，需替换为真实扣子API）
def fetch_douyin_hot():
    url = 'https://api.kouzi.com/douyin/hot'  # 示例URL
    headers = {'Authorization': f'Bearer {KOUZI_API_KEY}'}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get('data', [])

# 调用OpenAI GPT对内容进行改写
def rewrite_content_with_gpt(content):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': '你是一个内容创作助手，请将输入内容改写得更有趣、更有网感。'},
            {'role': 'user', 'content': content}
        ]
    }
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']

# 生成设计文档
def generate_md(contents):
    md = '# DouTrendyGPT 设计文档\n\n'
    for idx, item in enumerate(contents, 1):
        md += f'## 热门内容 {idx}\n原文：{item["origin"]}\n改写：{item["rewrite"]}\n\n'
    return md

def main():
    hot_list = fetch_douyin_hot()
    results = []
    for item in hot_list[:5]:  # 只处理前5条
        origin = item.get('desc', '')
        if not origin:
            continue
        rewrite = rewrite_content_with_gpt(origin)
        results.append({'origin': origin, 'rewrite': rewrite})
    md_content = generate_md(results)
    with open('DESIGN.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    print('设计文档已生成：DESIGN.md')

if __name__ == '__main__':
    main()
