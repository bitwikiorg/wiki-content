#!/usr/bin/env python3
"""Audit actual use of BITwiki's MediaWiki/SMW runtime substrate."""
from __future__ import annotations
import json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'manifest.json'; SITEINFO=ROOT/'archive-v1'/'siteinfo.json'; LIVE_TEMPLATES=ROOT/'archive-v1'/'templates'/'index.json'; OUTPUT=ROOT/'v2-substrate-audit.json'
SOURCE_ROOTS=('Main','BITwiki','Portal','Template','Property','Category','Concept','Module','SMWSchema','MediaWiki','Help')
SOURCE_SUFFIXES={'.mediawiki','.lua','.css','.js','.json'}
PATTERNS={
'smw_ask':re.compile(r'\{\{\s*#ask\s*:',re.I),'smw_concept':re.compile(r'\{\{\s*#concept\s*:',re.I),'smw_subobject':re.compile(r'\{\{\s*#subobject\s*:',re.I),'scribunto_invoke':re.compile(r'\{\{\s*#invoke\s*:',re.I),'cargo_declare':re.compile(r'\{\{\s*#cargo_declare\s*:',re.I),'cargo_store':re.compile(r'\{\{\s*#cargo_store\s*:',re.I),'cargo_query':re.compile(r'\{\{\s*#cargo_query\s*:',re.I),'includeonly':re.compile(r'<includeonly>',re.I),'onlyinclude':re.compile(r'<onlyinclude>',re.I),'noinclude':re.compile(r'<noinclude>',re.I),'main_namespace_transclusion':re.compile(r'\{\{\s*:[^{}|\n]+',re.I)}
SEMANTIC_ANNOTATION=re.compile(r'\[\[([^\[\]|:]+)::',re.I)
INTENTIONALLY_NOT_DEPLOYED={'Talk','User','User talk','BITwiki talk','File','File talk','MediaWiki talk','Template talk','Help talk','Category talk','Property talk','Concept talk','smw/schema talk','Module talk'}
def read_json(p): return json.loads(p.read_text(encoding='utf-8'))
def relative(p): return p.relative_to(ROOT).as_posix()
def source_files():
 out=[]
 for name in SOURCE_ROOTS:
  root=ROOT/name
  if root.exists(): out.extend(p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in SOURCE_SUFFIXES)
 return sorted(out)
def ns_name(item): return 'Main' if item.get('id')==0 else item.get('name','')
def main():
 manifest=read_json(MANIFEST); siteinfo=read_json(SITEINFO); template_index=read_json(LIVE_TEMPLATES); files=source_files(); primitive=Counter(); primitive_files={k:[] for k in PATTERNS}; props=Counter(); surfaces=Counter()
 for p in files:
  rel=relative(p); surfaces[p.relative_to(ROOT).parts[0]]+=1
  try: text=p.read_text(encoding='utf-8')
  except UnicodeDecodeError: continue
  for name,pattern in PATTERNS.items():
   matches=pattern.findall(text)
   if matches: primitive[name]+=len(matches); primitive_files[name].append(rel)
  for prop in SEMANTIC_ANNOTATION.findall(text): props[prop.strip()]+=1
 records=[i for i in siteinfo['query']['namespaces'].values() if i.get('id',-1)>=0]; configured=sorted({ns_name(i) for i in records if ns_name(i)},key=str.casefold); extensions=sorted({i.get('name','') for i in siteinfo['query'].get('extensions',[]) if i.get('name')},key=str.casefold)
 mappings=manifest.get('mediawiki_substrate',{}).get('source_control_mappings',{}); mapped={s['path'] for s in mappings.values() if s.get('path')}; missing_roots=sorted(path for path in mapped if not (ROOT/path.rstrip('/')).exists()); configured_unmapped=sorted(ns for ns in configured if ns not in mappings and ns not in INTENTIONALLY_NOT_DEPLOYED)
 projections=sorted(ns for ns,spec in mappings.items() if spec.get('kind')=='title projection'); projection_namespaces=sorted(set(projections)&set(configured))
 live=sorted(i['title'] for i in template_index.get('templates',[])); controlled=sorted(f'Template:{p.stem}' for p in (ROOT/'Template').glob('*.mediawiki')); missing_templates=sorted(set(live)-set(controlled))
 dirs=[p for p in ROOT.rglob('*') if p.is_dir() and '.git' not in p.parts and '__pycache__' not in p.parts]; missing_readmes=sorted(relative(p) for p in dirs if not (p/'README.md').exists())
 warnings=[]
 if primitive['cargo_declare']==0: warnings.append('Cargo is installed but no source-controlled Cargo table declaration was found; keep this at zero until a repeated-data workflow justifies a table.')
 if primitive['cargo_store']==0: warnings.append('No source-controlled Cargo storage call was found.')
 if primitive['smw_subobject']==0: warnings.append('No SMW subobject usage was found; introduce subobjects only for qualified/nested facts.')
 critical=[]
 if missing_roots: critical.append('Mapped source roots missing: '+', '.join(missing_roots))
 if missing_templates: critical.append('Current live templates absent from Template/: '+', '.join(missing_templates))
 if missing_readmes: critical.append('Directories without README.md: '+', '.join(missing_readmes))
 if configured_unmapped: critical.append('Configured content/runtime namespaces without repository mapping: '+', '.join(configured_unmapped))
 report={'status':'ok' if not critical else 'error','purpose':'Measure actual use of MediaWiki, Semantic MediaWiki, Scribunto, Cargo and transclusion primitives instead of inferring architecture from prose.','siteinfo_snapshot':str(SITEINFO.relative_to(ROOT)),'configured_namespaces':configured,'installed_extensions':extensions,'source_control_mappings':mappings,'configured_but_unmapped':configured_unmapped,'title_projections':projections,'title_projections_also_configured_as_namespaces':projection_namespaces,'source_files_scanned':len(files),'source_surface_file_counts':dict(sorted(surfaces.items())),'primitive_counts':{name:primitive.get(name,0) for name in PATTERNS},'primitive_files':{name:sorted(paths) for name,paths in primitive_files.items() if paths},'semantic_property_assertion_counts':dict(sorted(props.items(),key=lambda x:(-x[1],x[0].casefold()))),'live_template_titles':live,'source_controlled_template_titles':controlled,'missing_live_templates':missing_templates,'missing_mapped_roots':missing_roots,'missing_readmes':missing_readmes,'warnings':warnings,'critical':critical}
 OUTPUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(json.dumps(report,indent=2,ensure_ascii=False)); return 0 if not critical else 1
if __name__=='__main__': raise SystemExit(main())
