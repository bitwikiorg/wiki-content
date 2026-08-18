#!/usr/bin/env python3
import hashlib, json, os, shutil, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
import requests

BASE=os.getenv('BITWIKI_BASE_URL','https://bitwiki.org').rstrip('/')
OUT=Path('archive-v1')
UA='BITwiki-V1-Archive/2.0 (+https://github.com/bitwikiorg/wiki-content)'
REPORTS={
'broken-redirects':'BrokenRedirects','dead-end-pages':'Deadendpages','double-redirects':'DoubleRedirects',
'long-pages':'Longpages','oldest-pages':'Ancientpages','fewest-revisions':'Fewestrevisions',
'pages-without-language-links':'Withoutinterwiki','short-pages':'Shortpages',
'uncategorized-categories':'Uncategorizedcategories','uncategorized-files':'Uncategorizedimages',
'uncategorized-pages':'Uncategorizedpages','uncategorized-templates':'Uncategorizedtemplates',
'unused-categories':'Unusedcategories','unused-files':'Unusedimages','unused-templates':'Unusedtemplates',
'wanted-categories':'Wantedcategories','wanted-files':'Wantedfiles','wanted-pages':'Wantedpages',
'wanted-templates':'Wantedtemplates','list-of-redirects':'Listredirects',
'most-linked-categories':'Mostlinkedcategories','most-linked-pages':'Mostlinked',
'most-transcluded-pages':'Mosttranscludedpages','pages-with-most-categories':'Mostcategories',
'pages-with-most-revisions':'Mostrevisions'}
REQUIRED={'Uncategorizedpages','Uncategorizedtemplates','Unusedtemplates','Wantedcategories','Unusedcategories','BrokenRedirects','DoubleRedirects'}

def iso(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def safe(s): return quote(s,safe='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 -_.()')
def dump(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def content(r):
    m=(r.get('slots') or {}).get('main') or {}
    return m.get('content',m.get('*',r.get('*',''))) or ''

class API:
    def __init__(self):
        self.s=requests.Session(); self.s.headers.update({'User-Agent':UA}); self.calls=0
        self.url=None
        for u in (BASE+'/w/api.php',BASE+'/api.php'):
            try:
                r=self.s.get(u,params={'action':'query','meta':'siteinfo','format':'json','formatversion':2},timeout=30); r.raise_for_status(); r.json(); self.url=u; break
            except Exception: pass
        if not self.url: raise RuntimeError('No BITwiki Action API endpoint responded')
    def get(self,**p):
        self.calls+=1; p.update(format='json',formatversion=2,utf8=1)
        for n in range(5):
            try:
                r=self.s.get(self.url,params=p,timeout=45); r.raise_for_status(); x=r.json()
                if 'error' in x: raise RuntimeError(x['error'])
                time.sleep(.02); return x
            except Exception:
                if n==4: raise
                time.sleep(1+n)
    def all(self,key,**p):
        out=[]; cont={}
        while True:
            x=self.get(**p,**cont); out += (x.get('query') or {}).get(key,[]) or []
            cont=x.get('continue') or {}
            if not cont:return out

def pages_of(a,ns): return a.all('allpages',action='query',list='allpages',apnamespace=ns,aplimit='max')
def history(a,title):
    out=[]; cont={}
    while True:
        x=a.get(action='query',prop='revisions',titles=title,rvprop='ids|timestamp|user|comment|flags|size|sha1|content',rvslots='main',rvlimit='max',**cont)
        ps=(x.get('query') or {}).get('pages') or []; ps=list(ps.values()) if isinstance(ps,dict) else ps
        if not ps: raise RuntimeError('No page: '+title)
        out += ps[0].get('revisions') or []; cont=x.get('continue') or {}
        if not cont:return out

def relations(a,title):
    cats=set(); tpls=set(); cont={}
    while True:
        x=a.get(action='query',prop='categories|templates',titles=title,cllimit='max',tllimit='max',**cont)
        ps=(x.get('query') or {}).get('pages') or []; ps=list(ps.values()) if isinstance(ps,dict) else ps
        if ps:
            cats|={r['title'] for r in ps[0].get('categories') or []}; tpls|={r['title'] for r in ps[0].get('templates') or []}
        cont=x.get('continue') or {}
        if not cont:return sorted(cats),sorted(tpls)

def main():
    started=iso(); a=API(); print('API',a.url)
    OUT.mkdir(exist_ok=True)
    for d in ('pages','history','namespaces','categories','templates','special'):
        if (OUT/d).exists(): shutil.rmtree(OUT/d)
    for f in ('manifest.json','raw-snapshots-1.md','raw-snapshots-2.md','wiki-surface-manifest.json','index.json','siteinfo.json','audit.json'):
        if (OUT/f).exists():(OUT/f).unlink()
    si=a.get(action='query',meta='siteinfo',siprop='general|namespaces|namespacealiases|specialpagealiases|statistics|extensions'); dump(OUT/'siteinfo.json',si)
    raw=si['query']['namespaces']; nss=list(raw.values()) if isinstance(raw,dict) else raw; nss=sorted([n for n in nss if int(n['id'])>=0],key=lambda n:int(n['id']))
    allp=[]; byns={}; nsum=[]
    for n in nss:
        i=int(n['id']); name=n.get('canonical') or n.get('name') or ('Main' if i==0 else f'NS-{i}'); name='Main' if i==0 else name
        ps=pages_of(a,i); byns[i]=ps; rec={'id':i,'name':n.get('name',''),'canonical':n.get('canonical',''),'archive_name':name,'count':len(ps),'pages':ps}; dump(OUT/'namespaces'/safe(name)/'index.json',rec)
        nsum.append({k:rec[k] for k in ('id','name','canonical','archive_name','count')}); print(i,name,len(ps))
        for p in ps:p['namespace_name']=name; allp.append(p)
    rel={}; revtotal=0
    for j,p in enumerate(allp,1):
        title=p['title']; ns=p['namespace_name']; fn=safe(title); hs=history(a,title)
        if not hs: raise RuntimeError('Zero revisions: '+title)
        revtotal+=len(hs); src=content(hs[0]); pp=OUT/'pages'/safe(ns)/(fn+'.mediawiki'); pp.parent.mkdir(parents=True,exist_ok=True); pp.write_text(src,encoding='utf-8')
        hp=OUT/'history'/safe(ns)/(fn+'.json'); dump(hp,{'title':title,'namespace':p.get('ns'),'pageid':p.get('pageid'),'revision_count':len(hs),'revisions':hs})
        cats,tpls=relations(a,title); rel[title]={'categories':cats,'templates':tpls}
        p.update(current_revid=hs[0].get('revid'),current_timestamp=hs[0].get('timestamp'),revision_count=len(hs),sha1=hs[0].get('sha1'),source_sha256=hashlib.sha256(src.encode()).hexdigest(),current_source_path=str(pp),history_path=str(hp),categories=cats,templates=tpls)
        if j%25==0 or j==len(allp):print('pages',j,'/',len(allp))
    used=a.all('allcategories',action='query',list='allcategories',aclimit='max',acprop='size|hidden'); usedmap={r['category']:r for r in used}; created={p['title'] for p in byns.get(14,[])}
    ctitles=created|{'Category:'+x for x in usedmap}; crecs=[]
    for t in sorted(ctitles,key=str.casefold):
        name=t.split(':',1)[1]; info=usedmap.get(name,{})
        mem=a.all('categorymembers',action='query',list='categorymembers',cmtitle=t,cmlimit='max',cmprop='ids|title|sortkey|sortkeyprefix|type|timestamp'); mp=OUT/'categories'/'members'/(safe(t)+'.json'); dump(mp,{'title':t,'count':len(mem),'members':mem})
        crecs.append({'title':t,'created_page':t in created,'used':bool(mem),'api_size':info.get('size',len(mem)),'pages':info.get('pages'),'subcats':info.get('subcats'),'files':info.get('files'),'member_count':len(mem),'members_path':str(mp)})
    dump(OUT/'categories'/'index.json',{'count':len(crecs),'used_count':sum(x['used'] for x in crecs),'created_page_count':sum(x['created_page'] for x in crecs),'wanted_page_count':sum(x['used'] and not x['created_page'] for x in crecs),'records':crecs})
    trecs=[]
    for p in byns.get(10,[]):
        t=p['title']; callers=a.all('embeddedin',action='query',list='embeddedin',eititle=t,eilimit='max'); up=OUT/'templates'/'usage'/(safe(t)+'.json'); dump(up,{'title':t,'transclusion_count':len(callers),'embedded_in':callers}); rr=rel.get(t,{})
        trecs.append({'title':t,'pageid':p.get('pageid'),'transclusion_count':len(callers),'unused':not callers,'categories':rr.get('categories',[]),'dependencies':rr.get('templates',[]),'usage_path':str(up)})
    dump(OUT/'templates'/'index.json',{'count':len(trecs),'unused_count':sum(x['unused'] for x in trecs),'uncategorized_count':sum(not x['categories'] for x in trecs),'records':sorted(trecs,key=lambda x:x['title'].casefold())})
    rix=[]; fails=[]
    for slug,qp in REPORTS.items():
        try:
            rows=a.all('querypage',action='query',list='querypage',qppage=qp,qplimit='max'); dump(OUT/'special'/(slug+'.json'),{'querypage':qp,'count':len(rows),'results':rows}); rix.append({'slug':slug,'querypage':qp,'count':len(rows),'status':'captured'})
        except Exception as e:
            dump(OUT/'special'/(slug+'.json'),{'querypage':qp,'status':'error','error':str(e)}); rix.append({'slug':slug,'querypage':qp,'status':'error','error':str(e)}); fails += [qp] if qp in REQUIRED else []
    dump(OUT/'special'/'index.json',{'reports':rix})
    if fails: raise RuntimeError('Required reports failed: '+','.join(fails))
    rc={r['querypage']:r.get('count') for r in rix if r['status']=='captured'}; un=sum(x['unused'] for x in trecs); uc=sum(not x['categories'] for x in trecs)
    audit={'snapshot_started':started,'snapshot_completed':iso(),'site':BASE,'api_endpoint':a.url,'api_calls':a.calls,'namespace_count':len(nss),'page_count':len(allp),'revision_count':revtotal,'namespace_counts_by_name':{x['archive_name']:x['count'] for x in nsum},'category_count_union':len(crecs),'used_category_count':sum(x['used'] for x in crecs),'created_category_page_count':sum(x['created_page'] for x in crecs),'wanted_category_page_count':sum(x['used'] and not x['created_page'] for x in crecs),'template_count':len(trecs),'unused_template_count_independent':un,'uncategorized_template_count_independent':uc,'querypage_counts':rc,'special_page_alias_count':len((si.get('query') or {}).get('specialpagealiases') or []),'continuation_policy':'Every list/revision/category/template/report request follows MediaWiki continuation until absent.','completeness':{'all_nonnegative_namespaces_enumerated':True,'all_current_page_sources_captured':True,'all_revision_bodies_captured':True,'all_used_and_created_categories_enumerated':True,'all_category_memberships_captured':True,'all_template_pages_enumerated':True,'all_template_transclusion_callers_captured':True,'required_maintenance_reports_captured':True}}
    audit['warnings']=[]
    if rc.get('Unusedtemplates')!=None and rc['Unusedtemplates']!=un:audit['warnings'].append(f"Unusedtemplates report={rc['Unusedtemplates']} vs embeddedin={un}")
    if rc.get('Uncategorizedtemplates')!=None and rc['Uncategorizedtemplates']!=uc:audit['warnings'].append(f"Uncategorizedtemplates report={rc['Uncategorizedtemplates']} vs category-tags={uc}")
    dump(OUT/'audit.json',audit); dump(OUT/'index.json',{'snapshot_completed':audit['snapshot_completed'],'site':BASE,'api_endpoint':a.url,'namespace_summary':nsum,'page_count':len(allp),'revision_count':revtotal,'records':sorted(allp,key=lambda x:(int(x.get('ns',0)),x['title'].casefold()))})
    (OUT/'README.md').write_text(f'''# archive-v1 — exhaustive public BITwiki V1 snapshot\n\n**Read-only provenance. Do not deploy this directory as V2 pages.**\n\nGenerated from the anonymous MediaWiki Action API with continuation followed until exhaustion.\n\n## Snapshot\n- Captured: **{audit["snapshot_completed"]}**\n- API: `{a.url}`\n- Namespaces enumerated: **{len(nss)}**\n- Pages: **{len(allp)}**\n- Revision bodies: **{revtotal}**\n- Templates: **{len(trecs)}**\n- Categories (used ∪ created): **{len(crecs)}**\n- Used categories: **{audit["used_category_count"]}**\n- Created Category: pages: **{audit["created_category_page_count"]}**\n- Used categories lacking Category: pages: **{audit["wanted_category_page_count"]}**\n\n## Files\n`siteinfo.json` site model; `index.json` every page; `namespaces/*` exhaustive title lists; `pages/*` current wikitext; `history/*` complete revision histories with bodies; `categories/*` complete category graph; `templates/*` every template and transclusion caller; `special/*` maintenance reports; `audit.json` completeness checks.\n\n## Migration\n```text\narchive exact V1 source + history + usage\n→ compare related versions\n→ preserve unique writing / citations / semantics / behavior\n→ separate durable ideas from obsolete implementation\n→ KEEP / REWRITE / MERGE / SPLIT / REDIRECT / RETIRE\n→ implement V2\n→ rerun maintenance reports\n```\n\nSpecial pages are generated reports, not deployable content pages. Similar titles are never sufficient evidence for a merge.\n''',encoding='utf-8')
    print(json.dumps(audit,indent=2))
if __name__=='__main__': main()
