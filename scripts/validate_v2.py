#!/usr/bin/env python3
"""Validate deployable BITwiki V2 wikitext by MediaWiki role."""
from __future__ import annotations
import json,re
from pathlib import Path
WIKITEXT_ROOTS=['Main','BITwiki','Portal','Template','Property','Category','Concept','SMWSchema','MediaWiki','Help']
CATEGORY_REQUIRED_ROOTS={'Main','BITwiki','Portal'}; IDENTITY_SCAN_ROOTS={'Main','BITwiki','Portal','Category','Concept','Help'}
CATEGORY_RE=re.compile(r'\[\[\s*Category:([^\]|#]+)',re.I); TEMPLATE_RE=re.compile(r'(?<!\{)\{\{(?!\{)\s*([^{}|\n]+)'); REDIRECT_RE=re.compile(r'^\s*#redirect\s*\[\[',re.I|re.M); LITERAL_BLOCK_RE=re.compile(r'<!--.*?-->|<(pre|nowiki|syntaxhighlight|source)\b[^>]*>.*?</\1\s*>',re.I|re.S)
MAGIC_WORDS={'PAGENAME','PAGENAMEE','FULLPAGENAME','FULLPAGENAMEE','BASEPAGENAME','BASEPAGENAMEE','SUBPAGENAME','SUBPAGENAMEE','ROOTPAGENAME','ROOTPAGENAMEE','NAMESPACE','NAMESPACEE','NAMESPACENUMBER','TALKSPACE','TALKSPACEE','SUBJECTSPACE','SUBJECTSPACEE','ARTICLESPACE','ARTICLESPACEE','TALKPAGENAME','TALKPAGENAMEE','SUBJECTPAGENAME','SUBJECTPAGENAMEE','ARTICLEPAGENAME','ARTICLEPAGENAMEE','REVISIONID','REVISIONDAY','REVISIONDAY2','REVISIONMONTH','REVISIONMONTH1','REVISIONYEAR','REVISIONTIMESTAMP','REVISIONUSER','CURRENTYEAR','CURRENTMONTH','CURRENTMONTH1','CURRENTMONTHNAME','CURRENTMONTHABBREV','CURRENTDAY','CURRENTDAY2','CURRENTDOW','CURRENTDAYNAME','CURRENTTIME','CURRENTHOUR','CURRENTWEEK','CURRENTTIMESTAMP','LOCALYEAR','LOCALMONTH','LOCALMONTH1','LOCALMONTHNAME','LOCALMONTHABBREV','LOCALDAY','LOCALDAY2','LOCALDOW','LOCALDAYNAME','LOCALTIME','LOCALHOUR','LOCALWEEK','LOCALTIMESTAMP','NUMBEROFPAGES','NUMBEROFARTICLES','NUMBEROFFILES','NUMBEROFEDITS','NUMBEROFVIEWS','NUMBEROFUSERS','NUMBEROFADMINS','NUMBEROFACTIVEUSERS','NUMBERINGROUP','NUMBERINGROUPE','CONTENTLANG','CONTENTLANGUAGE','DIRECTIONMARK','DIRMARK','SITENAME','SERVER','SERVERNAME','SCRIPTPATH','STYLEPATH','CURRENTVERSION','PROTECTIONLEVEL','PROTECTIONEXPIRY','DISPLAYTITLE','DEFAULTSORT'}
ALLOWED_ENTITY_TYPES={'Concept','Method','Protocol','Implementation','Project','Dataset','Person','Organization','Event','Publication','Location','Technology'}
ALLOWED_DOMAINS={'Systems science','Science','Biology','Computer science','Mathematics','Philosophy','Technology','Electronics','Energy','Engineering','Chemistry','Physics','Medicine'}
ALLOWED_EPISTEMIC_STATUSES={'Hypothetical','Emerging','Supported','Well-supported','Established','Disputed'}; REQUIRED_KNOWLEDGE_FIELDS=('entity_type','domain','status','provenance')
def title(v): return re.sub(r'\s+',' ',v.replace('_',' ').strip())
def files(root):
 p=Path(root); return sorted(p.rglob('*.mediawiki')) if p.exists() else []
def executable_text(text): return LITERAL_BLOCK_RE.sub('',text)
def template_params(text,name):
 match=re.search(r'{{\s*'+re.escape(name)+r'\b(.*?)}}',text,re.I|re.S)
 if not match: return None
 params={}
 for part in match.group(1).split('|')[1:]:
  if '=' not in part: continue
  key,value=part.split('=',1); key=title(key).casefold().replace(' ','_'); value=title(value)
  if key: params[key]=value
 return params
def split_domains(text): return [title(x) for x in text.split(',') if title(x)]
def main():
 all_files=[p for root in WIKITEXT_ROOTS for p in files(root)]; category_pages={title(p.relative_to('Category').as_posix()[:-10]) for p in files('Category')}; template_pages={title(p.relative_to('Template').as_posix()[:-10]) for p in files('Template')}; category_refs={}; template_refs={}; uncategorized=[]; knowledge_objects=[]; missing_fields=[]; invalid_types=[]; invalid_domains=[]; invalid_statuses=[]; exemplar_domains=set()
 for p in all_files:
  parsed=executable_text(p.read_text(encoding='utf-8')); root=p.parts[0]; cats=sorted({title(x) for x in CATEGORY_RE.findall(parsed) if '{' not in x})
  for c in cats: category_refs.setdefault(c,[]).append(str(p))
  temps=[]
  for raw in TEMPLATE_RE.findall(parsed):
   t=title(raw); low=t.casefold()
   if not t or t.startswith(('#',':','!')) or '{' in t or low.startswith(('subst:','safesubst:')): continue
   if t.upper() in MAGIC_WORDS: continue
   if ':' in t and t.split(':',1)[0].casefold() in {'int','msg','msgnw'}: continue
   temps.append(t)
  for t in sorted(set(temps)): template_refs.setdefault(t,[]).append(str(p))
  if root in CATEGORY_REQUIRED_ROOTS and not cats: uncategorized.append(str(p))
  if root in IDENTITY_SCAN_ROOTS and not REDIRECT_RE.search(parsed):
   ko=template_params(parsed,'Knowledge object')
   if ko is not None:
    knowledge_objects.append(str(p)); missing=[f for f in REQUIRED_KNOWLEDGE_FIELDS if not ko.get(f)]
    if missing: missing_fields.append({'path':str(p),'missing':missing})
    et=ko.get('entity_type')
    if et and et not in ALLOWED_ENTITY_TYPES: invalid_types.append({'path':str(p),'value':et})
    dt=ko.get('domain')
    if dt:
     domains=split_domains(dt)
     for d in domains:
      if d not in ALLOWED_DOMAINS: invalid_domains.append({'path':str(p),'value':d})
     if 'Domain exemplars' in cats: exemplar_domains.update(domains)
    st=ko.get('status')
    if st and st not in ALLOWED_EPISTEMIC_STATUSES: invalid_statuses.append({'path':str(p),'value':st})
 missing_categories={k:v for k,v in category_refs.items() if k not in category_pages}; missing_templates={k:v for k,v in template_refs.items() if k not in template_pages}; required=sorted(ALLOWED_DOMAINS); missing_domain_categories=[d for d in required if d not in category_pages]; missing_domain_portals=[d for d in required if not Path('Portal',d+'.mediawiki').exists()]; exemplars=[p for p in files('Main') if '[[Category:Domain exemplars]]' in p.read_text(encoding='utf-8')]; missing_exemplars=[d for d in required if d not in exemplar_domains]
 report={'deployable_wikitext_files':len(all_files),'wikitext_roots':WIKITEXT_ROOTS,'category_required_roots':sorted(CATEGORY_REQUIRED_ROOTS),'category_pages':len(category_pages),'template_pages':len(template_pages),'distinct_category_references':len(category_refs),'distinct_template_references':len(template_refs),'missing_category_pages':missing_categories,'missing_template_pages':missing_templates,'uncategorized_content_or_navigation_pages':uncategorized,'required_domain_count':len(required),'required_domain_categories_missing':missing_domain_categories,'required_domain_portal_title_projections_missing':missing_domain_portals,'domain_exemplar_count':len(exemplars),'domain_exemplar_domains':sorted(exemplar_domains),'domain_exemplar_domains_missing':missing_exemplars,'domain_exemplars':[str(p) for p in exemplars],'knowledge_object_count':len(knowledge_objects),'knowledge_object_pages':knowledge_objects,'knowledge_object_required_fields_missing':missing_fields,'invalid_entity_type_values':invalid_types,'invalid_domain_values':invalid_domains,'invalid_epistemic_status_values':invalid_statuses,'controlled_vocabularies':{'entity_types':sorted(ALLOWED_ENTITY_TYPES),'domains':sorted(ALLOWED_DOMAINS),'epistemic_statuses':sorted(ALLOWED_EPISTEMIC_STATUSES)},'notes':['Portal/ is validated as a title projection, not asserted to be a configured namespace.','Template/ compatibility/runtime pages are not required to join a category merely to satisfy CI.','Module/Lua and runtime configuration are audited by scripts/audit_substrate.py rather than parsed as ordinary wikitext.']}
 report['valid']=not any([missing_categories,missing_templates,uncategorized,missing_domain_categories,missing_domain_portals,missing_exemplars,missing_fields,invalid_types,invalid_domains,invalid_statuses]); Path('v2-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(json.dumps(report,indent=2,ensure_ascii=False)); raise SystemExit(0 if report['valid'] else 1)
if __name__=='__main__': main()
