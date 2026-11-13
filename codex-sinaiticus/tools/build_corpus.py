#!/usr/bin/env python3
"""Streaming Codex Sinaiticus XML transcription -> complete per-book static JSON."""
import hashlib, json, re, sys, xml.sax
from collections import defaultdict
from pathlib import Path

SOURCE='https://raw.githubusercontent.com/itsee-birmingham/codex-sinaiticus/main/sinaiticus_full_v195.xml'
NT='Matthew|Mark|Luke|John|Romans|1 Corinthians|2 Corinthians|Galatians|Ephesians|Philippians|Colossians|1 Thessalonians|2 Thessalonians|Hebrews|1 Timothy|2 Timothy|Titus|Philemon|Acts|James|1 Peter|2 Peter|1 John|2 John|3 John|Jude|Revelation|Barnabas|Shepherd of Hermas'.split('|')
ID='Matius|Markus|Lukas|Yohanes|Roma|1 Korintus|2 Korintus|Galatia|Efesus|Filipi|Kolose|1 Tesalonika|2 Tesalonika|Ibrani|1 Timotius|2 Timotius|Titus|Filemon|Kisah Para Rasul|Yakobus|1 Petrus|2 Petrus|1 Yohanes|2 Yohanes|3 Yohanes|Yudas|Wahyu|Surat Barnabas|Gembala Hermas'.split('|')
OT={1:('Genesis','Kejadian'),2:('Exodus','Keluaran'),3:('Leviticus','Imamat'),4:('Numbers','Bilangan'),5:('Deuteronomy','Ulangan'),6:('Joshua','Yosua'),7:('Judges','Hakim-hakim'),8:('Ruth','Rut'),9:('1 Kingdoms','1 Kerajaan'),10:('2 Kingdoms','2 Kerajaan'),11:('3 Kingdoms','3 Kerajaan'),12:('4 Kingdoms','4 Kerajaan'),13:('1 Chronicles','1 Tawarikh'),14:('2 Chronicles','2 Tawarikh'),26:('Psalms','Mazmur'),27:('Proverbs','Amsal'),32:('Job','Ayub')}
def label(b,title):
    n=int(b)
    if 33<=n<=61:return {'en':NT[n-33],'id':ID[n-33]}
    en,local=OT.get(n,(title or f'Book {b}',title or f'Kitab {b}'))
    return {'en':en,'id':local}
class Codex(xml.sax.ContentHandler):
    def __init__(self):
        self.books=defaultdict(list);self.titles={};self.book=None;self.div=[]
        self.current=None;self.ab=[];self.page=None;self.words=None;self.app=[];self.readings=[]
        self.skip=0;self.title=None
    def startElement(self,tag,a):
        tag=tag.split(':')[-1]
        if tag=='div':
            typ=a.get('type');self.div.append((typ,self.book))
            if typ=='book':
                m=re.search(r'\d+',a.get('n') or a.get('id') or '')
                self.book=m.group() if m else None
                if self.book and a.get('title'):self.titles.setdefault(self.book,a.get('title'))
        elif tag=='pb':
            m=re.match(r'^(?:Q|S-)(\d+)-(\d+)([rv])',a.get('id') or a.get('xml:id') or '',re.I)
            if not m:m=re.match(r'^(\d+)-(\d+)([rv])',a.get('n') or '',re.I)
            if m:
                self.page=f'{int(m[1])}-{int(m[2])}{m[3].lower()}'
                if self.current is not None and self.page not in self.current['pages']:
                    self.current['pages'].append(self.page)
        elif tag=='ab':
            vid=a.get('id') or a.get('xml:id') or ''
            m=re.match(r'^V-B(\d+)K(\d+)V(\d+)',vid) or re.match(r'^V-(\d+)-(\d+)-(\d+)',vid)
            self.ab.append(bool(m))
            if m:
                b,c,v=(str(int(x)) for x in m.groups())
                self.current={'b':b,'c':c,'v':v,'id':vid,'w':[],'pages':[self.page] if self.page else []}
        elif tag=='app':self.app.append({'count':0,'lemma':False})
        elif tag=='lem':
            if self.app:self.app[-1]['lemma']=True
        elif tag=='rdg':
            if self.app:
                st=self.app[-1];st['count']+=1
                self.readings.append(st['count']==1 and not st['lemma'])
            else:self.readings.append(True)
        elif tag in ('note','margin'):
            if tag=='note' and a.get('type')=='booktitle' and self.book:self.title=[]
            self.skip+=1
        elif tag=='w' and self.current is not None and self.skip==0 and all(self.readings):self.words=[]
    def characters(self,s):
        if self.words is not None and not self.skip:self.words.append(s)
        if self.title is not None:self.title.append(s)
    def endElement(self,tag):
        tag=tag.split(':')[-1]
        if tag=='w' and self.words is not None:
            value=re.sub(r'\s+',' ',''.join(self.words)).strip()
            if value and self.current is not None:self.current['w'].append(value)
            self.words=None
        elif tag=='rdg' and self.readings:self.readings.pop()
        elif tag=='app' and self.app:self.app.pop()
        elif tag in ('note','margin'):
            if tag=='note' and self.title is not None:
                title=re.sub(r'\s+',' ',''.join(self.title)).strip()
                if title and self.book:self.titles.setdefault(self.book,title)
                self.title=None
            self.skip=max(0,self.skip-1)
        elif tag=='ab':
            if self.ab and self.ab.pop() and self.current is not None:
                if self.current['w']:self.books[self.current['b']].append(self.current)
                self.current=None
        elif tag=='div' and self.div:_,self.book=self.div.pop()
def build(source,destination):
    source=Path(source);dest=Path(destination);(dest/'books').mkdir(parents=True,exist_ok=True)
    h=Codex();p=xml.sax.make_parser()
    for flag in ('http://xml.org/sax/features/external-general-entities','http://xml.org/sax/features/external-parameter-entities'):
        try:p.setFeature(flag,False)
        except xml.sax.SAXException:pass
    p.setContentHandler(h)
    with source.open('rb') as f:p.parse(f)
    total_verses=sum(len(v) for v in h.books.values())
    total_words=sum(len(v['w']) for vs in h.books.values() for v in vs)
    if len(h.books)<35 or total_verses<8500 or total_words<50000:
        raise ValueError(f'Incomplete XML: {len(h.books)} books, {total_verses} verses, {total_words} tokens')
    entries=[]
    for b,verses in sorted(h.books.items(),key=lambda row:int(row[0])):
        fn=f'books/b{b}.json'
        (dest/fn).write_text(json.dumps(verses,ensure_ascii=False,separators=(',',':')),encoding='utf8')
        entries.append({'book':b,'label':label(b,h.titles.get(b,'')),'titleGreek':h.titles.get(b,''),'count':len(verses),'chapters':sorted({int(v['c']) for v in verses}),'file':fn})
    digest=hashlib.sha256()
    with source.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
    meta={'title':'Codex Sinaiticus — preserved transcription','source':'Codex Sinaiticus Project / ITSEE Birmingham','sourceUrl':SOURCE,'sourceSha256':digest.hexdigest(),'license':'CC BY-NC-SA 3.0','totals':{'verses':total_verses,'tokens':total_words},'books':entries,'notes':'First encoded correction reading; bilingual lexical annotations are separate and incomplete.'}
    (dest/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    (dest/'quality-report.json').write_text(json.dumps({'books':len(entries),'verses':total_verses,'tokens':total_words,'sourceSha256':digest.hexdigest(),'philologicalTranslationReview':'not performed'},indent=2),encoding='utf8')
    print(f'{len(entries)} books, {total_verses} preserved verses, {total_words} tokens')
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: python build_corpus.py SOURCE.xml OUTPUT_DIR')
    build(sys.argv[1],sys.argv[2])
