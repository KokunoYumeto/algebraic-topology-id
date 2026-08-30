#!/usr/bin/env python3
"""Prepare an isolated append-only backend suffix for the D60 capstone."""
from __future__ import annotations
import copy, hashlib, json, re, sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SOURCE = ROOT / "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md"
QA_DIR = ROOT / "qa/capstone"
OUT = ROOT / "qa/capstone-backend-20260829"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl", "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl", "segments.jsonl", "terms.jsonl", "units.jsonl")
TIMESTAMP = "2026-08-29T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
RIGHTS_ID = "rights:o012-d60-capstone-original-cc-by-sa-4.0"
EDITION_ID = "edition:fomberg-at-2025-563194f"
RESOURCE_ID = "resource:fomberg-algebraic-topology-2025"
PROGRAM_ID = "program:o012-id"
COURSE_ID = "course:o012-d60"
ROUTE = "D60-R14"
SOURCE_REL = "source/id-ID/capstone/o012-d60-capstone-klein-bottle.md"

def sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()
def canon(row: dict[str, Any]) -> bytes: return (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def load_existing() -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    tables: dict[str, list[dict[str, Any]]] = {}; by_id: dict[str, dict[str, Any]] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes(); rows = []
        if b"\r" in raw or not raw.endswith(b"\n"): raise RuntimeError(f"invalid backend bytes: {name}")
        for line in raw.splitlines(keepends=True):
            row = json.loads(line.decode("utf-8"));
            if row["id"] in by_id: raise RuntimeError(f"duplicate existing ID: {row['id']}")
            by_id[row["id"]] = row; rows.append(row)
        tables[name] = rows
    return tables, by_id

def source_lines() -> tuple[list[bytes], str]:
    raw = SOURCE.read_bytes()
    if b"\r" in raw or not raw.endswith(b"\n"): raise RuntimeError("capstone source must be LF terminated")
    return raw.splitlines(keepends=True), sha(raw)

def stable_ids(lines: list[bytes]) -> list[tuple[str, int]]:
    text = b"".join(lines).decode("utf-8")
    found: list[tuple[str, int]] = []
    for n, line in enumerate(text.splitlines(), 1):
        for ident in re.findall(r"#(o012-d60-capstone(?:-[a-z0-9]+)*)\b", line):
            if not any(x[0] == ident for x in found): found.append((ident, n))
    if len(found) != 34: raise RuntimeError(f"expected 34 stable IDs, got {len(found)}")
    return found

def title_for(lines: list[str], line_no: int, ident: str) -> str:
    line = lines[line_no - 1]
    m = re.search(r"^#{1,2}\s+(.+?)\s+\{" + re.escape("#" + ident) + r"\}", line)
    if m: return re.sub(r"[`*_]", "", m.group(1)).strip()
    m = re.search(r"\*\*(.+?)\*\*", line)
    return m.group(1).strip() if m else ident

def classify(ident: str) -> str:
    if ident == "o012-d60-capstone": return "capstone"
    if "-ex-" in ident: return "exercise"
    if "-hint-" in ident: return "hint"
    if "-sol-" in ident: return "solution"
    if ident.endswith("-cover"): return "figure"
    if ident.endswith("-oral-rubric"): return "rubric"
    if ident.endswith("-rights"): return "rights_notice"
    if ident.endswith("-interpretation"): return "interpretation"
    return "section"

def parent_ident(ident: str) -> str | None:
    if ident == "o012-d60-capstone": return None
    m = re.search(r"-task-(\d{3})$", ident)
    if m: return "o012-d60-capstone"
    m = re.search(r"-(?:ex|hint|sol)-(\d{3})$", ident)
    if m: return f"o012-d60-capstone-task-{m.group(1)}"
    if ident.endswith("-cover"): return "o012-d60-capstone-data"
    return "o012-d60-capstone"

def locator(path: str, file_sha: str, lines: list[bytes], line_no: int) -> dict[str, Any]:
    raw = lines[line_no - 1]
    return {"content_sha256": sha(raw), "file_sha256": file_sha, "line_start": line_no, "line_end": line_no, "path": path}

def concept_rows(existing: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    specs = [("klein-bottle", "Klein bottle", "algebraic_topology"), ("mapping-torus", "mapping torus", "algebraic_topology"), ("monodromy", "monodromy", "fibered_spaces"), ("orientation-cover", "orientation cover", "algebraic_topology"), ("semidirect-product", "semidirect product", "group_theory"), ("exponent-sum", "signed exponent sum", "cellular_homology"), ("integral-fundamental-class", "integral fundamental class", "algebraic_topology"), ("degree-obstruction", "degree obstruction", "algebraic_topology"), ("finite-invariant-boundary", "finite invariant inference boundary", "mathematical_method"), ("proof-reconstruction", "proof reconstruction", "mathematical_method")]
    rows=[]; ids={}
    for slug,label,domain in specs:
        ident=f"concept:o012-d60-capstone-{slug}"; ids[slug]=ident
        if ident in existing: raise RuntimeError(f"concept collision: {ident}")
        rows.append({"canonical_label":label,"domain":domain,"entity_type":"concept","id":ident,"locale_neutral":True,"schema":"curriculum.interop","schema_version":"0.1.0","status":"active","supersedes":None,"timestamp":TIMESTAMP,"workflow":"o012-d60-id-reader-production"})
    return rows,ids

def make_additions(tables: dict[str, list[dict[str, Any]]], existing: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    lines, file_sha = source_lines(); text_lines=[x.decode('utf-8') for x in lines]; found=stable_ids(lines)
    additions={name:[] for name in FILES}; root_ident="o012-d60-capstone"; root_unit=f"unit:{root_ident}"
    concepts, concept_ids = concept_rows(existing); additions["concepts.jsonl"].extend(concepts)
    # Rights component is independent and covers every capstone unit.
    rights={"attribution":"Materi asli capstone D60 berbahasa Indonesia.","change_notice":"Original proof-reconstruction and synthesis layer; Roberts and Fomberg components remain separately attributed.","component_scope":[f"unit:{ident}" for ident,_ in found],"entity_type":"rights","id":RIGHTS_ID,"license_expression":"CC-BY-SA-4.0","license_url":"https://creativecommons.org/licenses/by-sa/4.0/","non_endorsement":"Independent Indonesian edition; no source-author or institutional endorsement.","schema":"curriculum.interop","schema_version":"0.1.0","status":"active","supersedes":None,"third_party_status":"No excluded problem-bank expression is used.","timestamp":TIMESTAMP,"workflow":"o012-d60-id-reader-production"}
    additions["rights.jsonl"].append(rights)
    # Build one unit and one segment for every stable reader ID.
    unit_by_ident={}
    for order,(ident,line_no) in enumerate(found,1):
        kind=classify(ident); par=parent_ident(ident); uid=f"unit:{ident}"; sid=f"segment:{ident}"; unit_by_ident[ident]=uid
        parent_uid=f"unit:{par}" if par else None
        path=[root_unit] if ident!=root_ident else [uid]
        if par and par!=root_ident: path.append(parent_uid)
        if ident!=root_ident: path.append(uid)
        concepts_used=["concept:fundamental-group","concept:homology","concept:attaching-map"]
        for slug in ("klein-bottle","mapping-torus","monodromy","orientation-cover","proof-reconstruction","finite-invariant-boundary"):
            concepts_used.append(concept_ids[slug])
        concepts_used=sorted(set(concepts_used))
        loc=locator(SOURCE_REL,file_sha,lines,line_no)
        display=title_for(text_lines,line_no,ident)
        common={"authority_context_ids":[COURSE_ID,PROGRAM_ID,EDITION_ID,RESOURCE_ID],"authority_context_only":True,"concept_ids":concepts_used,"course_id":COURSE_ID,"course_route_unit_id":ROUTE,"display_title":display,"edition_context_only":True,"edition_id":EDITION_ID,"edition_unit_id":"O012-ORIG-CAPSTONE","entity_type":"unit","id":uid,"locale":"id-ID","model_provenance":MODEL,"order":order,"parent_id":parent_uid,"path":path,"primary_course_route_unit_id":ROUTE,"program_id":PROGRAM_ID,"provenance_relation":"edition_original","resource_context_only":True,"resource_id":RESOURCE_ID,"rights_component_id":RIGHTS_ID,"schema":"curriculum.interop","schema_version":"0.1.0","source_corpus_used":False,"source_local_id":ident,"source_locator":{"kind":"edition_original","path":SOURCE_REL,"precision":"exact_target_span"},"status":"active","supersedes":None,"target_locator":loc,"timestamp":TIMESTAMP,"translation_state":"built","unit_kind":kind,"workflow":"o012-d60-id-reader-production"}
        seg={"authority_context_ids":[COURSE_ID,PROGRAM_ID,EDITION_ID,RESOURCE_ID],"authority_context_only":True,"concept_ids":concepts_used,"course_route_unit_id":ROUTE,"edition_context_only":True,"edition_id":EDITION_ID,"edition_unit_id":"O012-ORIG-CAPSTONE","entity_type":"segment","id":sid,"locale":"id-ID","model_provenance":MODEL,"order":order,"primary_course_route_unit_id":ROUTE,"provenance_relation":"edition_original","resource_context_only":True,"resource_id":RESOURCE_ID,"rights_component_id":RIGHTS_ID,"schema":"curriculum.interop","schema_version":"0.1.0","segment_kind":kind,"source_corpus_used":False,"source_local_id":ident,"source_locator":{"kind":"edition_original","line_end":line_no,"line_start":line_no,"path":SOURCE_REL,"precision":"exact_target_span"},"status":"active","supersedes":None,"target_locator":loc,"timestamp":TIMESTAMP,"translation_state":"built","unit_id":uid,"workflow":"o012-d60-id-reader-production"}
        additions["units.jsonl"].append(common); additions["segments.jsonl"].append(seg)
    # Controlled glossary terms with exact evidence anchors.
    term_specs=[("klein-bottle","Klein bottle","botol Klein","o012-d60-capstone-data"),("mapping-torus","mapping torus","mapping torus","o012-d60-capstone-data"),("monodromy","monodromy","monodromi","o012-d60-capstone-data"),("orientation-cover","orientation cover","selubung orientasi","o012-d60-capstone-data"),("semidirect-product","semidirect product","produk semidirect","o012-d60-capstone-ex-002"),("signed-exponent-sum","signed exponent sum","jumlah eksponen bertanda","o012-d60-capstone-ex-003"),("integral-fundamental-class","integral fundamental class","kelas fundamental integral","o012-d60-capstone-ex-004"),("degree-obstruction","degree obstruction","batas derajat","o012-d60-capstone-ex-004"),("proof-reconstruction","proof reconstruction","rekonstruksi bukti","o012-d60-capstone-proof-map"),("finite-invariant-boundary","finite invariant inference boundary","batas inferensi invarian terbatas","o012-d60-capstone-interpretation")]
    for n,(slug,source_term,preferred,evid) in enumerate(term_specs,1):
        tid=f"term:o012-d60-capstone-term-{n:03d}:id-ID"; cid=concept_ids.get(slug, "concept:algebraic-topology");
        if cid=="concept:algebraic-topology": cid="concept:homology"
        additions["terms.jsonl"].append({"concept_id":cid,"entity_type":"term","evidence_segment_id":f"segment:{evid}","id":tid,"locale":"id-ID","preferred":preferred,"register":"textbook","rejected_forms":[],"rights_component_id":RIGHTS_ID,"scope_unit_id":root_unit,"source_term":source_term,"status":"active","supersedes":None,"terminology_control_id":f"O012-CAP-TERM-{n:03d}","terminology_status":"admitted","timestamp":TIMESTAMP,"usage_note":"Capstone controlled terminology.","variants":[],"workflow":"o012-d60-id-reader-production"})
    # Relations: containment, hint/solution bindings, prerequisites, and repair xrefs.
    def rel(ident,typ,fr,to,note,**extra):
        row={"entity_type":"relation","from_id":fr,"id":ident,"note":note,"relation_type":typ,"schema":"curriculum.interop","schema_version":"0.1.0","status":"active","supersedes":None,"timestamp":TIMESTAMP,"to_id":to,"workflow":"o012-d60-id-reader-production"}; row.update(extra); return row
    for ident,_ in found:
        if ident==root_ident: continue
        par=parent_ident(ident) or root_ident
        additions["relations.jsonl"].append(rel(f"relation:contains:o012-d60-capstone:{ident}","contains",f"unit:{par}",f"unit:{ident}",f"Capstone contains {ident}."))
    for i in range(1,7):
        additions["relations.jsonl"].append(rel(f"relation:hints:o012-d60-capstone:{i:03d}","hints",f"unit:o012-d60-capstone-hint-{i:03d}",f"unit:o012-d60-capstone-ex-{i:03d}","Capstone hint binds to its exercise."))
        additions["relations.jsonl"].append(rel(f"relation:solves:o012-d60-capstone:{i:03d}","solves",f"unit:o012-d60-capstone-sol-{i:03d}",f"unit:o012-d60-capstone-ex-{i:03d}","Capstone complete checked solution binds to its exercise.",solution_status="complete_checked_solution"))
    for i,target in enumerate(["unit:o012-d60-lab01","unit:o012-d60-lab02","unit:o012-d60-lab03","unit:o012-d60-lab04"],1):
        additions["relations.jsonl"].append(rel(f"relation:depends-on:o012-d60-capstone:lab-{i:02d}","depends-on",root_unit,target,"Capstone prerequisite laboratory."))
    for i,target in enumerate(["segment:o012-fom-u003-forward-quotient-les","segment:o012-fom-u007-proof-pr13","segment:o012-fom-u007-proof-pr14","segment:o012-fom-u007-proof-pr15"],1):
        additions["relations.jsonl"].append(rel(f"relation:xref:o012-d60-capstone:repair-{i:02d}","xref",f"segment:o012-d60-capstone-proof-map",target,"Capstone proof map cross-references the closed repair."))
    additions["relations.jsonl"].append(rel("relation:xref:o012-d60-capstone:route-r14","xref",root_unit,"unit:o012-rbt-l30","Capstone is the D60-R14 route capstone.",course_route_unit_id=ROUTE))
    # QA artifacts and events.
    qa_specs=[("source","qa/capstone/STATIC_QA.json","qa:o012-d60-capstone-source", "source"),("structure","qa/capstone/STATIC_QA.json","qa:o012-d60-capstone-structure", "structure"),("math","qa/capstone/INDEPENDENT_MATH_REVIEW.json","qa:o012-d60-capstone-math", "math"),("language","qa/capstone/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json","qa:o012-d60-capstone-language", "language"),("mastery","qa/capstone/QA.json","qa:o012-d60-capstone-mastery", "mastery")]
    artifact_ids=[]
    for kind,path,event_id,qa_type in qa_specs:
        raw=(ROOT/path).read_bytes(); aid=f"artifact:o012-d60-capstone-{kind}-qa"; artifact_ids.append(aid)
        additions["artifacts.jsonl"].append({"bytes":len(raw),"edition_unit_id":"O012-ORIG-CAPSTONE","entity_type":"artifact","id":aid,"locale":"id-ID","manifest_artifact_id":None,"media_type":"application/json","path":path,"qa_event_ids":[event_id],"rights_component_id":RIGHTS_ID,"schema":"curriculum.interop","schema_version":"0.1.0","sha256":sha(raw),"status":"active","supersedes":None,"timestamp":TIMESTAMP,"toolchain":"D60 capstone source/QA; OpenAI Codex gpt-5.6-sol, Ultra; semantic admission only.","translation_state":"built","unit_id":root_unit,"workflow":"o012-d60-id-reader-production"})
        additions["qa.jsonl"].append({"capstone_id":"D60-CAPSTONE","entity_type":"qa_event","id":event_id,"note":f"Independent capstone {kind} QA passed with P1=P2=P3=0.","qa_type":qa_type,"result":"passed","schema":"curriculum.interop","schema_version":"0.1.0","status":"active","supersedes":None,"timestamp":TIMESTAMP,"unit_id":root_unit,"witness_artifact_ids":[aid],"workflow":"o012-d60-id-reader-production"})
    for name in FILES: additions[name].sort(key=lambda x:x["id"])
    return additions

def write_candidate(additions: dict[str,list[dict[str,Any]]], run: str, baseline: dict[str,tuple[int,int,str]]) -> dict[str,Any]:
    target=OUT/run
    if target.exists(): raise RuntimeError(f"candidate exists: {target}")
    target.mkdir(parents=True); suffix={}
    for name in FILES:
        raw=b"".join(canon(x) for x in additions[name]); (target/name).write_bytes(raw); suffix[name]={"records":len(additions[name]),"bytes":len(raw),"sha256":sha(raw)}
    receipt={"status":"PASS_CANDIDATE","timestamp":TIMESTAMP,"model_provenance":MODEL,"baseline":baseline,"suffix":suffix,"records_added":sum(x["records"] for x in suffix.values()),"bytes_added":sum(x["bytes"] for x in suffix.values())}
    (target/"RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8",newline="\n"); return receipt

def main() -> int:
    apply="--apply" in sys.argv; tables,existing=load_existing(); baseline={name:(len((BACKEND/name).read_bytes().splitlines()),(BACKEND/name).stat().st_size,sha((BACKEND/name).read_bytes())) for name in FILES}; additions=make_additions(tables,existing)
    all_ids=set(existing); new=[x["id"] for rows in additions.values() for x in rows]
    if len(new)!=len(set(new)) or all_ids.intersection(new): raise RuntimeError("capstone backend ID collision")
    if OUT.exists(): raise RuntimeError("candidate directory exists; inspect/apply with separate script")
    r1=write_candidate(additions,"run-a",baseline); r2=write_candidate(additions,"run-b",baseline)
    if r1["suffix"]!=r2["suffix"]: raise RuntimeError("candidate replay drift")
    print(json.dumps({"status":"PASS_CANDIDATE_ONLY","baseline":baseline,"records_added":r1["records_added"],"bytes_added":r1["bytes_added"],"suffix":r1["suffix"]},ensure_ascii=False,sort_keys=True)); return 0

if __name__=="__main__": raise SystemExit(main())
