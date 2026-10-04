"""Chuyển spec/proposal HTML thành markdown tách theo mục cho AI agent đọc.
Dùng: python3 scripts/docs/html_to_md.py docs/technical-spec-build-plan.html docs/spec "Technical spec & kế hoạch build"
Cần: pip install beautifulsoup4 markdownify
"""
import re, sys, unicodedata
from bs4 import BeautifulSoup
from markdownify import markdownify as md

if hasattr(sys.stdout, "reconfigure"):  # Windows console cp1252 không in được tiếng Việt → UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def slug(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if unicodedata.category(c)!='Mn').replace('đ','d').replace('Đ','D')
    return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')[:40]

def convert(src,outdir,prefix_title):
    soup=BeautifulSoup(open(src,encoding='utf-8').read(),'html.parser')
    for s in soup(['script','style','button']): s.decompose()
    idx=[]
    for sec in soup.find_all('section'):
        sid=sec.get('id') or ''
        if not sid or 'partdiv' in (sec.get('class') or []): 
            # part dividers → index only
            if sid:
                t=sec.find(class_='title'); n=sec.find(class_='num')
                idx.append(('part', (n.get_text(strip=True) if n else '')+' — '+(t.get_text(strip=True) if t else ''), None))
            continue
        # diagrams & pre → code fences
        codes=[]
        for d in sec.find_all(['pre']) + sec.find_all(class_='diagram'):
            txt=d.get_text()
            lang='python' if re.search(r'^\s*(def |class |import |from |async def )',txt,re.M) else ('yaml' if re.search(r'^\s*[\w-]+:\s',txt,re.M) and 'def ' not in txt else 'text')
            codes.append('```'+lang+'\n'+txt.strip('\n')+'\n```')
            d.replace_with(soup.new_string(f'\n\nCODEBLOCK{len(codes)-1}X\n\n'))
        num=sec.find(class_='num'); title=sec.find(class_='title')
        numt=num.get_text(' ',strip=True) if num else sid
        tt=title.get_text(' ',strip=True) if title else ''
        if num: num.decompose()
        if title: title.decompose()
        body=md(str(sec),heading_style='ATX',bullets='-',strip=['section','div','span'])
        body=re.sub(r'\n{3,}','\n\n',body).strip()
        body=body.replace('\\_','_').replace('\\*','*')
        for i,c in enumerate(codes): body=body.replace(f'CODEBLOCK{i}X',c)
        m=re.match(r'(\d+(?:\.\d+)?)',numt)
        n=m.group(1) if m else ''
        fname=(f'{int(float(n)):02d}' if n and '.' not in n else (n.replace('.','_') if n else 'x'))+'-'+sid+'.md'
        if not n: fname=sid+'.md'
        head=f'# {numt} — {tt}\n\n> Trích từ {prefix_title}. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.\n\n'
        open(f'{outdir}/{fname}','w',encoding='utf-8').write(head+body+'\n')
        idx.append(('sec',f'{numt} — {tt}',fname))
    return idx

idx=convert(sys.argv[1],sys.argv[2],sys.argv[3])
lines=[f'# Mục lục — {sys.argv[3]}\n']
for k,t,f in idx:
    lines.append(f'\n## {t}\n' if k=='part' else f'- [{t}]({f})')
open(f'{sys.argv[2]}/README.md','w',encoding='utf-8').write('\n'.join(lines)+'\n')
print(len([i for i in idx if i[0]=='sec']))
