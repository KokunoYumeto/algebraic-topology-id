#!/usr/bin/env python3
"""Append the D60 capstone PDF to the frozen Lab 4 PDF."""
from __future__ import annotations
import argparse, importlib.util, json, re
from hashlib import sha256
from pathlib import Path
from typing import Any
import pypdf
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
PRIOR_BYTES = 10_131_344
PRIOR_SHA = "337dcb8bf7ee3d5b5b58c0efc621e661db2542b49f52f1b12b786b55db4fa2fc"
PRIOR_PAGES = 558
PRIOR_OUTLINE = 487
PRIOR_NAMED = 3155
PYPDF_VERSION = "6.12.2"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

def digest(p: Path) -> str: return sha256(p.read_bytes()).hexdigest()
def require(ok: bool, msg: str) -> None:
    if not ok: raise RuntimeError(msg)

def helper():
    path=ROOT/'scripts/merge-cumulative-assessments-002-003.py'
    spec=importlib.util.spec_from_file_location('d60_pdf_helpers',path); require(spec and spec.loader,'helper load failed')
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def source_contract(path: Path):
    text=path.read_text(encoding='utf-8')
    headings=[(len(m.group(1)),m.group(2).strip(),m.group(3)) for m in re.finditer(r'(?m)^(#{1,2})\s+(.+?)\s+\{#(o012-d60-capstone(?:-[a-z0-9]+)*)\}\s*$',text)]
    ids=re.findall(r'#(o012-d60-capstone(?:-[a-z0-9]+)*)\b',text)
    require(len(ids)==len(set(ids))==34,'capstone stable-ID census drift')
    require(len(headings)==14 and headings[0][0]==1 and all(x[0]==2 for x in headings[1:]),'capstone heading hierarchy drift')
    require(set(x[2] for x in headings).issubset(set(ids)),'capstone heading ID missing')
    return headings,ids

def bookmark(title: str) -> str:
    require(title.count('$')%2==0,'unbalanced math in heading')
    value=title.replace('$','')
    require('\\' not in value and '{' not in value and '}' not in value,'unsupported TeX in heading')
    return value

def merge(prior:Path, appendix:Path, output:Path, source:Path, scratch:Path)->dict[str,Any]:
    require(pypdf.__version__==PYPDF_VERSION,f'pypdf {pypdf.__version__} != {PYPDF_VERSION}')
    require(prior.is_file() and appendix.is_file() and source.is_file(),'merge input missing')
    require(prior.stat().st_size==PRIOR_BYTES and digest(prior)==PRIOR_SHA,'frozen Lab4 PDF drift')
    require(output.parent==scratch and output.suffix.lower()=='.pdf','unsafe merge output')
    headings,ids=source_contract(source); h=helper(); base=PdfReader(str(prior)); app=PdfReader(str(appendix))
    prior_struct=h.page_structure_hashes(base,PRIOR_PAGES); prior_outline=h.outline_entries(base)
    app_outline=h.outline_entries(app)
    require(len(base.pages)==PRIOR_PAGES and len(prior_outline)==PRIOR_OUTLINE and len(base.named_destinations)==PRIOR_NAMED,'predecessor structure drift')
    require(len(app.pages)>0 and len(app_outline)==len(headings),'appendix outline drift')
    require([bookmark(x[1]) for x in headings]==[x[0] for x in app_outline],'source/PDF heading mismatch')
    app_named={name:app.get_destination_page_number(dest) for name,dest in app.named_destinations.items()}
    require(all(x in app_named and app_named[x] is not None for x in ids),'appendix named destinations incomplete')
    prior_named={name:base.get_destination_page_number(dest) for name,dest in base.named_destinations.items()}
    require(set(ids).isdisjoint(prior_named),'capstone ID collision')
    external=[x for x in h.link_targets(app,0) if x not in ids and x not in prior_named]
    require(not external,f'unresolved appendix targets: {sorted(set(external))[:5]}')
    writer=PdfWriter(); writer.append(str(prior),import_outline=True); app._named_destinations_cache={}; writer.append(app,import_outline=False)
    for ident in ids: writer.add_named_destination(ident,PRIOR_PAGES+int(app_named[ident]))
    parent=None
    for (level,title,_),(_,local) in zip(headings,app_outline,strict=True):
        page=PRIOR_PAGES+int(local)
        if level==1: parent=writer.add_outline_item(bookmark(title),page,is_open=True)
        else: require(parent is not None,'level-2 heading without parent'); writer.add_outline_item(bookmark(title),page,parent=parent)
    writer.add_metadata({'/Title':'Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1–3, Laboratorium Komputasi 1–4, dan Capstone D60','/Author':'David Michael Roberts; Yeheli Fomberg; edisi Bahasa Indonesia dengan pendamping penguasaan','/Subject':'Edisi komposit D60 dengan capstone rekonstruksi bukti dan sintesis lintas-invarian','/Creator':f'{MODEL}; atas arahan pengguna','/Producer':'pypdf deterministic append','/CreationDate':"D:20260829000000+02'00'",'/ModDate':"D:20260829000000+02'00'"})
    writer.page_mode='/UseOutlines'; writer._ID=None
    with output.open('wb') as stream: writer.write(stream)
    merged=PdfReader(str(output)); merged_struct=h.page_structure_hashes(merged,PRIOR_PAGES); outline=h.outline_entries(merged); named={n:merged.get_destination_page_number(d) for n,d in merged.named_destinations.items()}
    require(len(merged.pages)==PRIOR_PAGES+len(app.pages),'merged page count drift'); require(merged_struct==prior_struct,'predecessor page structure changed'); require(outline[:PRIOR_OUTLINE]==prior_outline and len(outline)==PRIOR_OUTLINE+len(headings),'outline prefix drift'); require(len(named)==PRIOR_NAMED+len(ids),'named destination count drift'); require(all(named.get(n)==p for n,p in prior_named.items()),'prior named destinations changed'); require(all(named.get(n)==PRIOR_PAGES+int(app_named[n]) for n in ids),'capstone destination drift')
    return {'status':'PASS','bytes':output.stat().st_size,'sha256':digest(output),'pages':len(merged.pages),'appendix_pages':len(app.pages),'pypdf':pypdf.__version__,'outline_entries':len(outline),'named_destinations':len(named),'stable_id_destinations_added':len(ids),'outline_entries_added':len(headings),'predecessor_page_structure_aggregate_sha256':h.aggregate_hash(prior_struct),'predecessor_page_structure_sha256':prior_struct,'predecessor_outline_exact_prefix':True,'predecessor_named_destinations_preserved':True}

if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('--prior',required=True); ap.add_argument('--append',required=True); ap.add_argument('--output',required=True); ap.add_argument('--source',required=True); ap.add_argument('--scratch-root',required=True); a=ap.parse_args(); print(json.dumps(merge(*(Path(x).resolve() for x in (a.prior,a.append,a.output,a.source,a.scratch_root))),sort_keys=True))
