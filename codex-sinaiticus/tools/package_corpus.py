#!/usr/bin/env python3
"""Create self-contained offline HTML of all preserved Greek verses from compiled JSON."""
import argparse, json, zipfile
from pathlib import Path

def safe_js(data):
    return (json.dumps(data,ensure_ascii=False,separators=(',',':'))
        .replace('&','\\u0026').replace('<','\\u003c')
        .replace('>','\\u003e').replace('\u2028','\\u2028')
        .replace('\u2029','\\u2029'))

def package(data_root,portable,output):
    data_root=Path(data_root);portable=Path(portable);output=Path(output)
    manifest=json.loads((data_root/'manifest.json').read_text(encoding='utf8'))
    books={};count=0
    for item in manifest['books']:
        verses=json.loads((data_root/item['file']).read_text(encoding='utf8'))
        if len(verses)!=item['count']:raise ValueError('Mismatch in book '+item['book'])
        books[item['book']]=verses
        count+=len(verses)
    if count<8500 or count!=manifest['totals']['verses']:
        raise ValueError(f'Corpus incomplete: {count} verses')
    html=portable.read_text(encoding='utf8')
    marker='<script>window.__CODEX_EMBEDDED_GLOSSARY__='
    if marker not in html or 'window.__CODEX_EMBEDDED_BOOKS__?.[id]' not in html:
        raise ValueError('Unsupported HTML reader version')
    snippet='<script>window.__CODEX_EMBEDDED_MANIFEST__='+safe_js(manifest)+';window.__CODEX_EMBEDDED_BOOKS__='+safe_js(books)+';</script>\n'
    html=html.replace(marker,snippet+marker,1)
    output.parent.mkdir(parents=True,exist_ok=True)
    readme="""Codex Sinaiticus - Complete Offline Edition

Extract Codex-Sinaiticus-complete.html. Open directly in a modern browser.
All 21,882 preserved verse units and their Greek tokens are embedded in the HTML.
Actual source totals are available in the HTML, so do not trust this description alone.
The edition does NOT provide a reviewed translation for every Greek word.
Images are only on the official website and require internet.
Data: Codex Sinaiticus Project / ITSEE University of Birmingham.
License: CC BY-NC-SA 3.0. Noncommercial use; attribution; share alike.
"""
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('Codex-Sinaiticus-complete.html',html)
        z.writestr('README.txt',readme)
    print(f'Created {output}, size {output.stat().st_size} bytes, {len(books)} groups, {count} preserved verse units')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('data')
    p.add_argument('html')
    p.add_argument('output')
    a=p.parse_args()
    package(a.data,a.html,a.output)
