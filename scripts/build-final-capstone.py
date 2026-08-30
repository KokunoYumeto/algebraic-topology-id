#!/usr/bin/env python3
"""Deterministically append the original D60 capstone to the Lab 4 reader."""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
PRIOR_SLUG='roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03-lab04'
SLUG=PRIOR_SLUG+'-capstone'
PRIOR_HTML=ROOT/f'output/html/{PRIOR_SLUG}/index.html'; PRIOR_PDF=ROOT/f'output/pdf/topologi-aljabar-{PRIOR_SLUG}-id.pdf'
SOURCE=ROOT/'source/id-ID/capstone/o012-d60-capstone-klein-bottle.md'
STATIC=ROOT/'qa/capstone/STATIC_QA.json'; MATH=ROOT/'qa/capstone/INDEPENDENT_MATH_REVIEW.json'; LANG=ROOT/'qa/capstone/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json'; QA=ROOT/'qa/capstone/QA.json'; CENSUS=ROOT/'qa/PROOF_REPAIR_CENSUS.json'
HTML_OUT=ROOT/f'output/html/{SLUG}/index.html'; PDF_OUT=ROOT/f'output/pdf/topologi-aljabar-{SLUG}-id.pdf'; MANIFEST_OUT=ROOT/f'output/ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE.csv'; DRAFT=ROOT/'qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_LAB01_LAB02_LAB03_LAB04_CAPSTONE_BUILD_DRAFT.json'
SCRATCH=ROOT/f'tmp/pdfs/{SLUG}-build'; MODEL='OpenAI Codex gpt-5.6-sol, Ultra'
PRIOR_HTML_ID=(15974648,'a76e31fc92e1554a6b14ffaccc1ad1001ee5c2838a3e36d1441b98519b39d4f8'); PRIOR_PDF_ID=(10131344,'337dcb8bf7ee3d5b5b58c0efc621e661db2542b49f52f1b12b786b55db4fa2fc'); PRIOR_PAGES=558; PRIOR_OUTLINE=487; PRIOR_NAMED=3155

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def digest(p:Path)->str:return sha(p.read_bytes())
def req(ok:bool,msg:str)->None:
    if not ok: raise RuntimeError(msg)
def ident(p:Path)->dict[str,Any]:
    b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'lf_lines':b.count(b'\n'),'sha256':sha(b)}
def command(args:list[str],cwd:Path=ROOT)->subprocess.CompletedProcess[bytes]:
    r=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,timeout=900,env={**os.environ,'SOURCE_DATE_EPOCH':'1787961600','FORCE_SOURCE_DATE':'1'})
    if r.returncode: raise RuntimeError(f'command failed {args!r}: {(r.stderr or b'').decode(errors="replace")[:2000]}')
    return r
def tool(n:str)->str:
    p=shutil.which(n); req(p is not None,f'missing tool {n}'); return p
def canonical_write(dst:Path,src:Path)->None:
    dst.parent.mkdir(parents=True,exist_ok=True); tmp=dst.parent/f'.{dst.name}.capstone.pending'; req(not tmp.exists(),'temporary collision'); shutil.copyfile(src,tmp); req(digest(tmp)==digest(src),'pending copy mismatch'); os.replace(tmp,dst); req(digest(dst)==digest(src),'promoted artifact mismatch')
def replace_once(text:str,old:str,new:str,label:str)->str:
    req(text.count(old)==1,f'{label} occurrence drift'); return text.replace(old,new,1)
def expand_html_fragment(pandoc:str)->str:
    outa=SCRATCH/'capstone-a.html'; outb=SCRATCH/'capstone-b.html'; src=SCRATCH/'capstone-source.md'; src.write_bytes(SOURCE.read_bytes())
    args=[pandoc,str(src),'--from=markdown+fenced_divs+tex_math_dollars','--to=html5','--mathml','--section-divs','--strip-comments','--fail-if-warnings']
    command([*args,f'--output={outa}']); command([*args,f'--output={outb}']); req(digest(outa)==digest(outb),'capstone HTML fragment builds differ')
    text=outa.read_text(encoding='utf-8'); req('<html' not in text and '<body' not in text,'fragment has shell');
    ids=sorted(set(re.findall(r'\bid="(cb[0-9]+(?:-[0-9]+)?)"',text)),key=len,reverse=True)
    for i in ids: text=text.replace(f'id="{i}"',f'id="capstone-{i}"').replace(f'href="#{i}"',f'href="#capstone-{i}"')
    stable=re.findall(r'\bid="(o012-d60-capstone(?:-[a-z0-9]+)*)"',text); req(len(stable)==len(set(stable))==34,'capstone HTML stable-ID drift'); req(text.count('class="exercise')==6 and text.count('class="hint')==6 and text.count('class="solution')==6,'capstone HTML exercise census drift'); req('<math' in text and '$' not in text,'capstone HTML math conversion failed'); return text
def pdf_source()->Path:
    raw=SOURCE.read_text(encoding='utf-8'); body=re.sub(r'\A---\n.*?\n---\n','',raw,count=1,flags=re.S)
    # Convert all fenced stable IDs to explicit PDF destinations, then headings.
    fence=re.compile(r'(?m)^(:::\s*\{[^\n]*?)\s+#(o012-d60-capstone(?:-[a-z0-9]+)*)\b([^\n]*\})\s*$')
    count=len(fence.findall(body)); req(count==20,'capstone fenced destination census drift')
    body=fence.sub(lambda m:m.group(1)+m.group(3)+'\n\n```{=latex}\n\\hypertarget{'+m.group(2)+'}{}\n```',body)
    heading=re.compile(r'(?m)^(#{1,2})\s+(.+?)\s+\{#(o012-d60-capstone(?:-[a-z0-9]+)*)\}\s*$'); req(len(heading.findall(body))==14,'capstone heading destination census drift')
    body=heading.sub(r'\1 \2\n\n```{=latex}\n\\hypertarget{\3}{}\n```',body)
    path=SCRATCH/'capstone-layout.md'; path.write_text(body,encoding='utf-8',newline='\n'); return path
def build_pdf_appendix(pandoc:str)->tuple[Path,dict[str,Any]]:
    src=pdf_source(); header=SCRATCH/'capstone-header.tex'; header.write_text('\\AddToHook{begindocument/end}{\\pdftrailerid{}}\n\\usepackage{listings}\n\\lstset{breaklines=true,breakatwhitespace=false,basicstyle=\\ttfamily\\scriptsize,columns=fullflexible,keepspaces=true,showstringspaces=false,upquote=true}\n',encoding='utf-8',newline='\n')
    a=SCRATCH/'append-a.pdf'; b=SCRATCH/'append-b.pdf'; args=[pandoc,str(src),'--from=markdown+fenced_divs+tex_math_dollars','--standalone','--number-sections','--strip-comments','--listings','--metadata=lang:id-ID','--metadata=pagetitle:Capstone D60','--metadata=date:29 Agustus 2026','--pdf-engine=pdflatex',f'--include-in-header={header}','--variable=papersize:a4','--variable=geometry:margin=21mm','--variable=fontsize:11pt','--variable=colorlinks:true','--variable=linkcolor:blue','--variable=pdf-trailer-id:']
    command([*args,f'--output={a}']); command([*args,f'--output={b}']); req(digest(a)==digest(b),'capstone appendix PDF builds differ')
    info=command(['pdfinfo',str(a)]).stdout.decode(errors='replace'); req(re.search(r'(?m)^Page size:.*\(A4\)\s*$',info) is not None,'appendix not A4'); m=re.search(r'(?m)^Pages:\s+(\d+)\s*$',info); req(m is not None and int(m.group(1))>0,'appendix page count missing'); trailer=command(['mutool','show',str(a),'trailer']).stdout.decode(errors='replace'); req(re.search(r'(?m)^\s*/ID\s',trailer) is None,'appendix trailer ID present'); return a,{'pages':int(m.group(1)),'bytes':a.stat().st_size,'sha256':digest(a)}
def main()->int:
    for p in (SOURCE,STATIC,MATH,LANG,QA,CENSUS,PRIOR_HTML,PRIOR_PDF): req(p.is_file(),f'missing input {p}')
    req(ident(PRIOR_HTML)['bytes']==PRIOR_HTML_ID[0] and digest(PRIOR_HTML)==PRIOR_HTML_ID[1],'prior HTML drift'); req(ident(PRIOR_PDF)['bytes']==PRIOR_PDF_ID[0] and digest(PRIOR_PDF)==PRIOR_PDF_ID[1],'prior PDF drift')
    census=json.loads(CENSUS.read_text(encoding='utf-8')); req(census.get('status')=='PASS' and len(census.get('summary',{}).get('proof_repairs_closed',[]))==4,'proof census not PASS'); static=json.loads(STATIC.read_text(encoding='utf-8')); req(static.get('status')=='PASS' and static.get('structure',{}).get('stable_ids')==34,'capstone static QA failed')
    q=json.loads(QA.read_text(encoding='utf-8')); req(q.get('status')=='PASS' and q.get('human_review_claimed') is False,'capstone combined QA failed')
    SCRATCH.mkdir(parents=True); req(SCRATCH.parent==(ROOT/'tmp/pdfs').resolve(),'unsafe scratch')
    try:
        pandoc=tool('pandoc'); mutool=tool('mutool'); pdfinfo=tool('pdfinfo'); pdffonts=tool('pdffonts'); pdftotext=tool('pdftotext'); python=sys.executable
        req(command([pandoc,'--version']).stdout.decode().splitlines()[0]=='pandoc 3.9.0.2','unexpected Pandoc version'); frag=expand_html_fragment(pandoc)
        prior=PRIOR_HTML.read_bytes().decode('utf-8'); nl='\r\n' if '\r\n' in prior else '\n';
        old_title='<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1–3, dan Laboratorium Komputasi 1–4</title>'; new_title='<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1–3, Laboratorium Komputasi 1–4, dan Capstone D60</title>'
        old_heading='<h1 class="title">Topologi Aljabar — Roberts 30/30, Fomberg'+nl+'1.1–1.13, Asesmen Kumulatif 1–3, dan Laboratorium Komputasi 1–4</h1>'; new_heading='<h1 class="title">Topologi Aljabar — Roberts 30/30, Fomberg'+nl+'1.1–1.13, Asesmen Kumulatif 1–3, Laboratorium Komputasi 1–4, dan Capstone D60</h1>'
        old_sub='<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui'+nl+'homologi seluler; 108 soal bersolusi; Laboratorium Komputasi 1–4 lengkap dan dapat dijalankan luring; checkpoint komposit parsial</p>'; new_sub='<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui'+nl+'homologi seluler; 108 soal bersolusi; Laboratorium Komputasi 1–4 dan capstone D60 lengkap serta dapat dijalankan luring; edisi komposit ditutup</p>'
        combined=replace_once(prior,old_title,new_title,'title'); combined=replace_once(combined,old_heading,new_heading,'heading'); combined=replace_once(combined,old_sub,new_sub,'subtitle')
        nav='\n</ul>\n</nav>' if nl=='\n' else nl+'</ul>'+nl+'</nav>'; pos=combined.rfind(nav); req(pos>0,'ToC close missing'); toc=nl+'<li><a href="#o012-d60-capstone" id="toc-o012-d60-capstone">Capstone D60 — Rekonstruksi Bukti dan Sintesis Lintas-Invarian</a></li>'; combined=combined[:pos]+toc+combined[pos:]
        old_status='Laboratorium Komputasi 1–4 kini lengkap. Jalur komposit masih parsial'+nl+'karena penutupan metadata bukti dan capstone belum selesai; kursor sumber'+nl+'berikutnya tetap pada baris 4186.'; new_status='Laboratorium Komputasi 1–4, metadata bukti, dan capstone kini lengkap. Seluruh'+nl+'jalur D60 yang dipilih telah ditutup; kursor sumber tetap pada baris 4186.'; combined=replace_once(combined,old_status,new_status,'status')
        body='\n</body>' if nl=='\n' else nl+'</body>'; bpos=combined.rfind(body); req(bpos>0,'body close missing'); insert=nl+frag.rstrip('\r\n').replace('\n',nl); combined=combined[:bpos]+insert+combined[bpos:]
        # exact predecessor reconstruction
        rev=combined; rev=rev[:rev.rfind(insert)]+rev[rev.rfind(insert)+len(insert):]; rev=rev.replace(toc,'',1); rev=replace_once(rev,new_status,old_status,'reverse status'); rev=replace_once(rev,new_sub,old_sub,'reverse subtitle'); rev=replace_once(rev,new_heading,old_heading,'reverse heading'); rev=replace_once(rev,new_title,old_title,'reverse title'); req(rev.encode()==PRIOR_HTML.read_bytes(),'HTML predecessor reconstruction failed')
        html_a=SCRATCH/'combined-a.html'; html_b=SCRATCH/'combined-b.html'; html_a.write_text(combined,encoding='utf-8',newline=''); html_b.write_text(combined,encoding='utf-8',newline=''); req(digest(html_a)==digest(html_b),'HTML write nondeterminism')
        all_ids=re.findall(r'(?<=\s)id="([^"]+)"',combined); req(len(all_ids)==len(set(all_ids)),'duplicate HTML IDs'); links=re.findall(r'\bhref="#([^"]+)"',combined); req(not(set(links)-set(all_ids)),'unresolved HTML fragments'); req('id="o012-d60-capstone"' in combined and 'id="toc-o012-d60-capstone"' in combined,'capstone HTML insertion missing'); req('max-width: 58rem;' in combined and 'margin: 0 auto;' in combined and '@media (max-width: 700px)' in combined,'reflow CSS drift'); req(not re.search(r'\bsrc="(?:https?:)?//',combined),'external HTML runtime asset'); req(not any(x in combined for x in ('C:\\Users\\','github_pat_','ghp_','access_token','BEGIN PRIVATE KEY')),'private marker in HTML')
        appendix,app_info=build_pdf_appendix(pandoc)
        merged_a=SCRATCH/'merged-a.pdf'; merged_b=SCRATCH/'merged-b.pdf'; merge_args=[python,'-B',str(ROOT/'scripts/merge-capstone.py'),'--prior',str(PRIOR_PDF),'--append',str(appendix),'--source',str(SOURCE),'--scratch-root',str(SCRATCH)]; ma=json.loads(command([*merge_args,'--output',str(merged_a)]).stdout); mb=json.loads(command([*merge_args,'--output',str(merged_b)]).stdout); req(digest(merged_a)==digest(merged_b),'merged PDFs differ'); req(ma.get('status')=='PASS','PDF merge failed'); req(ma.get('pages')==PRIOR_PAGES+app_info['pages'] and ma.get('outline_entries')==PRIOR_OUTLINE+14 and ma.get('named_destinations')==PRIOR_NAMED+34,'PDF census drift')
        prior_text=SCRATCH/'prior.txt'; merged_prefix=SCRATCH/'merged-prefix.txt'; merged_text=SCRATCH/'merged.txt'; command([pdftotext,'-enc','UTF-8','-f','1','-l',str(PRIOR_PAGES),str(PRIOR_PDF),str(prior_text)]); command([pdftotext,'-enc','UTF-8','-f','1','-l',str(PRIOR_PAGES),str(merged_a),str(merged_prefix)]); req(digest(prior_text)==digest(merged_prefix),'PDF predecessor text changed'); command([pdftotext,'-enc','UTF-8',str(merged_a),str(merged_text)]); ptxt=merged_text.read_text(encoding='utf-8',errors='replace'); req(all(x in ptxt for x in ('Capstone D60','botol Klein','FOM-PR-13','H_1','degree')),'required capstone PDF text missing'); req(not any(x in ptxt for x in ('C:\\Users\\','github_pat_','BEGIN PRIVATE KEY')),'private marker in PDF')
        fonts=[x for x in command([pdffonts,str(merged_a)]).stdout.decode(errors='replace').splitlines()[2:] if x.strip()]; req(fonts and all(re.search(r'\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',x) and re.search(r'\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',x).groups()==('yes','yes','yes') for x in fonts),'font embedding gate failed')
        manifest=SCRATCH/'manifest.csv'; manifest.write_text('path,bytes,sha256\n'+f'{HTML_OUT.relative_to(ROOT).as_posix()},{html_a.stat().st_size},{digest(html_a)}\n'+f'{PDF_OUT.relative_to(ROOT).as_posix()},{merged_a.stat().st_size},{digest(merged_a)}\n',encoding='utf-8',newline='\n')
        receipt={'status':'PASS_DETERMINISTIC_BUILD_PENDING_VISUAL_BROWSER_QA','source_date_epoch':1787961600,'model_provenance':MODEL,'pandoc':command([pandoc,'--version']).stdout.decode().splitlines()[0],'pypdf':'6.12.2','frozen_predecessor':{'html':{'bytes':PRIOR_HTML_ID[0],'sha256':PRIOR_HTML_ID[1]},'pdf':{'bytes':PRIOR_PDF_ID[0],'sha256':PRIOR_PDF_ID[1],'pages':PRIOR_PAGES},'html_exact_reconstruction':True,'pdf_extracted_text_prefix_identical':True},'source':ident(SOURCE),'qa_inputs':[ident(x) for x in (STATIC,MATH,LANG,QA,CENSUS)],'html':{'path':HTML_OUT.relative_to(ROOT).as_posix(),'bytes':html_a.stat().st_size,'sha256':digest(html_a),'stable_ids_added':34,'headings_added':14,'exercises_added':6,'hints_added':6,'solutions_added':6,'centered_reflowing_self_contained':True,'native_mathml':True},'pdf':{'path':PDF_OUT.relative_to(ROOT).as_posix(),'bytes':merged_a.stat().st_size,'sha256':digest(merged_a),'pages':ma['pages'],'appendix_pages':app_info['pages'],'stable_id_destinations_added':34,'outline_entries_added':14,'named_destinations':ma['named_destinations'],'fonts':len(fonts),'all_fonts_embedded_subset_tounicode':True,'trailer_id_suppressed':True},'manifest':{'path':MANIFEST_OUT.relative_to(ROOT).as_posix(),'bytes':manifest.stat().st_size,'sha256':digest(manifest)},'proof_census':{'path':CENSUS.relative_to(ROOT).as_posix(),'bytes':CENSUS.stat().st_size,'sha256':digest(CENSUS)},'toolchain_inputs':{'builder':ident(Path(__file__).resolve()),'merger':ident(ROOT/'scripts/merge-capstone.py')}}
        draft=SCRATCH/'draft.json'; draft.write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n'); canonical_write(HTML_OUT,html_a); canonical_write(PDF_OUT,merged_a); canonical_write(MANIFEST_OUT,manifest); canonical_write(DRAFT,draft); print(json.dumps(receipt,ensure_ascii=False,sort_keys=True)); return 0
    finally:
        if SCRATCH.exists(): shutil.rmtree(SCRATCH)

if __name__=='__main__': raise SystemExit(main())
