#!/usr/bin/env python3
import json, os, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
import requests

BASE=os.getenv('BITWIKI_BASE_URL','https://bitwiki.org').rstrip('/')
ARCHIVE=Path('archive-v1')
OUT=Path('v1-fidelity-audit.json')
UA='BITwiki-V1-Fidelity-Audit/1.0 (+https://github.com/bitwikiorg/wiki-content)'


def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def normalize_rows(v):
    if isinstance(v,list): return v
    if isinstance(v,dict): return list(v.values())
    return []


def slot_content(rev, role='main'):
    slot=(rev.get('slots') or {}).get(role) or {}
    if 'content' in slot: return slot.get('content') or ''
    if '*' in slot: return slot.get('*') or ''
    if role == 'main' and '*' in rev: return rev.get('*') or ''
    return None


def safe(s):
    return quote(s,safe='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 -_.()')


class API:
    def __init__(self):
        self.s=requests.Session(); self.s.headers.update({'User-Agent':UA}); self.calls=0; self.url=None
        for u in (BASE+'/w/api.php',BASE+'/api.php'):
            try:
                r=self.s.get(u,params={'action':'query','meta':'siteinfo','format':'json','formatversion':2},timeout=30)
                r.raise_for_status(); r.json(); self.url=u; break
            except Exception:
                pass
        if not self.url: raise RuntimeError('No public BITwiki Action API endpoint responded')

    def get(self,**params):
        self.calls += 1
        params.update(format='json',formatversion=2,utf8=1)
        for attempt in range(5):
            try:
                r=self.s.get(self.url,params=params,timeout=60)
                r.raise_for_status(); data=r.json()
                if 'error' in data: raise RuntimeError(data['error'])
                time.sleep(.01)
                return data
            except Exception:
                if attempt == 4: raise
                time.sleep(1+attempt)

    def continued(self,key,**params):
        out=[]; cont={}
        while True:
            data=self.get(**params,**cont)
            value=(data.get('query') or {}).get(key,[]) or []
            if not isinstance(value,list):
                raise TypeError(f'Expected query.{key} list, got {type(value).__name__}')
            out.extend(value)
            cont=data.get('continue') or {}
            if not cont: return out


def allpages(api, ns):
    return api.continued('allpages',action='query',list='allpages',apnamespace=ns,aplimit='max')


def revisions(api,title):
    out=[]; cont={}
    while True:
        data=api.get(
            action='query',prop='revisions',titles=title,
            rvprop='ids|timestamp|user|comment|flags|size|sha1|slotsize|slotsha1|contentmodel|roles|content|tags',
            rvslots='*',rvlimit='max',**cont)
        pages=normalize_rows((data.get('query') or {}).get('pages') or [])
        if not pages: raise RuntimeError('No live page returned for '+title)
        out.extend(pages[0].get('revisions') or [])
        cont=data.get('continue') or {}
        if not cont: return out


def relations(api,title):
    cats=set(); templates=set(); cont={}
    while True:
        data=api.get(action='query',prop='categories|templates',titles=title,cllimit='max',tllimit='max',**cont)
        pages=normalize_rows((data.get('query') or {}).get('pages') or [])
        if pages:
            cats.update(x['title'] for x in pages[0].get('categories') or [])
            templates.update(x['title'] for x in pages[0].get('templates') or [])
        cont=data.get('continue') or {}
        if not cont: return sorted(cats),sorted(templates)


def imageinfo(api,title):
    out=[]; cont={}
    while True:
        data=api.get(action='query',prop='imageinfo',titles=title,
                     iiprop='timestamp|user|comment|url|size|sha1|mime|mediatype|archivename',iilimit='max',**cont)
        pages=normalize_rows((data.get('query') or {}).get('pages') or [])
        if not pages: raise RuntimeError('No live file page returned for '+title)
        out.extend(pages[0].get('imageinfo') or [])
        cont=data.get('continue') or {}
        if not cont: return out


def querypage(api, name):
    out=[]; cont={}
    while True:
        data=api.get(action='query',list='querypage',qppage=name,qplimit='max',**cont)
        q=(data.get('query') or {}).get('querypage')
        rows=(q.get('results') or []) if isinstance(q,dict) else (q or [])
        if not isinstance(rows,list): raise TypeError('Unexpected querypage payload '+name)
        out.extend(rows)
        cont=data.get('continue') or {}
        if not cont: return out


def logevents(api, logtype):
    return api.continued('logevents',action='query',list='logevents',letype=logtype,lelimit='max',
                         leprop='ids|title|type|user|timestamp|comment|details')


def archived_revision_map(record):
    data=load(record['history_path'])
    return {int(r['revid']):r for r in data.get('revisions') or []}


def member_key(row):
    return (int(row.get('ns',0)),row.get('title'))


def main():
    started=now(); api=API()
    archive_audit=load(ARCHIVE/'audit.json')
    archive_index=load(ARCHIVE/'index.json')
    archive_records=archive_index.get('records') or []
    archive_by_key={(int(r['ns']),r['title']):r for r in archive_records}

    siteinfo=api.get(action='query',meta='siteinfo',siprop='general|namespaces|namespacealiases|statistics')
    nsraw=(siteinfo.get('query') or {}).get('namespaces') or {}
    namespaces=normalize_rows(nsraw)
    namespaces=sorted([n for n in namespaces if int(n['id'])>=0],key=lambda n:int(n['id']))

    live_pages=[]
    namespace_drift=[]
    archived_ns={int(x['id']):x for x in archive_index.get('namespace_summary') or []}
    for n in namespaces:
        ns=int(n['id']); local=n.get('name') or n.get('canonical') or ('Main' if ns==0 else f'NS-{ns}')
        local='Main' if ns==0 else local
        pages=allpages(api,ns)
        live_pages.extend(pages)
        old=archived_ns.get(ns)
        if old is None or old.get('archive_name') != local:
            namespace_drift.append({'id':ns,'live_name':local,'archived':old})

    live_by_key={(int(p['ns']),p['title']):p for p in live_pages}
    missing_pages=sorted([{'ns':k[0],'title':k[1]} for k in live_by_key.keys()-archive_by_key.keys()],key=lambda x:(x['ns'],x['title'].casefold()))
    stale_pages=sorted([{'ns':k[0],'title':k[1]} for k in archive_by_key.keys()-live_by_key.keys()],key=lambda x:(x['ns'],x['title'].casefold()))

    pageid_mismatches=[]; current_revision_mismatches=[]; revision_set_mismatches=[]; revision_body_mismatches=[]
    current_source_mismatches=[]; non_main_slots=[]; hidden_public_content=[]; revision_errors=[]
    live_revision_count=0; live_revision_bodies_checked=0; slot_roles=set()

    common=sorted(live_by_key.keys() & archive_by_key.keys(),key=lambda k:(k[0],k[1].casefold()))
    for i,key in enumerate(common,1):
        live=live_by_key[key]; arc=archive_by_key[key]
        if int(live.get('pageid',-1)) != int(arc.get('pageid',-2)):
            pageid_mismatches.append({'title':key[1],'ns':key[0],'live':live.get('pageid'),'archive':arc.get('pageid')})
        try:
            lr=revisions(api,key[1]); ar=archived_revision_map(arc)
        except Exception as e:
            revision_errors.append({'title':key[1],'error':repr(e)}); continue
        live_revision_count += len(lr)
        lm={int(r['revid']):r for r in lr}
        if set(lm)!=set(ar):
            revision_set_mismatches.append({'title':key[1],'live_only':sorted(set(lm)-set(ar)),'archive_only':sorted(set(ar)-set(lm))})
        if lr:
            newest=lr[0]
            if int(arc.get('current_revid',-1)) != int(newest.get('revid',-2)) or arc.get('sha1') != newest.get('sha1'):
                current_revision_mismatches.append({'title':key[1],'archive_revid':arc.get('current_revid'),'live_revid':newest.get('revid'),'archive_sha1':arc.get('sha1'),'live_sha1':newest.get('sha1')})
            live_main=slot_content(newest)
            if live_main is not None:
                archived_current=Path(arc['current_source_path']).read_text(encoding='utf-8')
                if archived_current != live_main:
                    current_source_mismatches.append({'title':key[1],'revid':newest.get('revid')})
        for revid in sorted(set(lm)&set(ar)):
            lrev=lm[revid]; arev=ar[revid]
            roles=lrev.get('roles') or list((lrev.get('slots') or {}).keys()) or ['main']
            for role in roles:
                slot_roles.add(role)
                if role != 'main': non_main_slots.append({'title':key[1],'revid':revid,'role':role})
            lmain=slot_content(lrev); amain=slot_content(arev)
            if lmain is None:
                if lrev.get('texthidden') or any((s or {}).get('texthidden') for s in (lrev.get('slots') or {}).values()):
                    hidden_public_content.append({'title':key[1],'revid':revid})
                continue
            live_revision_bodies_checked += 1
            if amain != lmain:
                revision_body_mismatches.append({'title':key[1],'revid':revid})
        if i%25==0 or i==len(common): print(f'pages {i}/{len(common)}')

    # Categories and complete membership graph.
    live_categories=api.continued('allcategories',action='query',list='allcategories',aclimit='max',acprop='size|hidden')
    live_cat_titles={'Category:'+x['category'] for x in live_categories}
    arc_cat_index=load(ARCHIVE/'categories'/'index.json')
    arc_cat_records={x['title']:x for x in arc_cat_index.get('records') or []}
    category_set_mismatch={
        'live_only':sorted(live_cat_titles-set(arc_cat_records),key=str.casefold),
        'archive_only':sorted(set(arc_cat_records)-live_cat_titles,key=str.casefold)
    }
    category_membership_mismatches=[]
    for title in sorted(live_cat_titles & set(arc_cat_records),key=str.casefold):
        live_members=api.continued('categorymembers',action='query',list='categorymembers',cmtitle=title,cmlimit='max',cmprop='ids|title|sortkey|sortkeyprefix|type|timestamp')
        archived=load(arc_cat_records[title]['members_path']).get('members') or []
        lk={member_key(x) for x in live_members}; ak={member_key(x) for x in archived}
        if lk != ak:
            category_membership_mismatches.append({'title':title,'live_only':sorted(list(lk-ak)),'archive_only':sorted(list(ak-lk))})

    # Template namespace and every transclusion caller.
    live_templates={p['title']:p for p in allpages(api,10)}
    arc_template_index=load(ARCHIVE/'templates'/'index.json')
    arc_templates={x['title']:x for x in arc_template_index.get('records') or []}
    template_set_mismatch={'live_only':sorted(set(live_templates)-set(arc_templates)), 'archive_only':sorted(set(arc_templates)-set(live_templates))}
    template_usage_mismatches=[]
    for title in sorted(set(live_templates)&set(arc_templates),key=str.casefold):
        live_callers=api.continued('embeddedin',action='query',list='embeddedin',eititle=title,eilimit='max')
        archived=load(arc_templates[title]['usage_path']).get('embedded_in') or []
        lk={member_key(x) for x in live_callers}; ak={member_key(x) for x in archived}
        if lk != ak:
            template_usage_mismatches.append({'title':title,'live_only':sorted(list(lk-ak)),'archive_only':sorted(list(ak-lk))})

    # File revision metadata. Binary availability is separately recorded in the archive.
    arc_files=load(ARCHIVE/'files'/'index.json')
    arc_file_records={x['title']:x for x in arc_files.get('records') or []}
    live_file_titles={p['title'] for p in allpages(api,6)}
    file_set_mismatch={'live_only':sorted(live_file_titles-set(arc_file_records)), 'archive_only':sorted(set(arc_file_records)-live_file_titles)}
    file_revision_mismatches=[]
    for title in sorted(live_file_titles & set(arc_file_records),key=str.casefold):
        live_infos=imageinfo(api,title); archived=arc_file_records[title].get('revisions') or []
        def ikey(x): return (x.get('timestamp'),x.get('sha1'),x.get('size'),x.get('mime'),x.get('mediatype'))
        if [ikey(x) for x in live_infos] != [ikey(x) for x in archived]:
            file_revision_mismatches.append({'title':title,'live':[ikey(x) for x in live_infos],'archive':[ikey(x) for x in archived]})

    required_reports=['Uncategorizedpages','Uncategorizedtemplates','Unusedtemplates','Wantedcategories','Wantedfiles','Wantedpages','Wantedtemplates','BrokenRedirects','DoubleRedirects']
    report_drift=[]
    archived_q=archive_audit.get('querypage_counts') or {}
    for name in required_reports:
        live_count=len(querypage(api,name))
        if archived_q.get(name) != live_count:
            report_drift.append({'querypage':name,'archive':archived_q.get(name),'live':live_count})

    # Public deletion log proves whether current-page enumeration can represent all historical wiki content.
    try:
        deletes=logevents(api,'delete')
    except Exception as e:
        deletes=[]; delete_log_error=repr(e)
    else:
        delete_log_error=None

    failures={
        'missing_live_pages_from_archive':missing_pages,
        'archived_pages_not_currently_live':stale_pages,
        'pageid_mismatches':pageid_mismatches,
        'current_revision_mismatches':current_revision_mismatches,
        'revision_set_mismatches':revision_set_mismatches,
        'revision_body_mismatches':revision_body_mismatches,
        'current_source_mismatches':current_source_mismatches,
        'revision_errors':revision_errors,
        'category_set_mismatch':category_set_mismatch if any(category_set_mismatch.values()) else {},
        'category_membership_mismatches':category_membership_mismatches,
        'template_set_mismatch':template_set_mismatch if any(template_set_mismatch.values()) else {},
        'template_usage_mismatches':template_usage_mismatches,
        'file_set_mismatch':file_set_mismatch if any(file_set_mismatch.values()) else {},
        'file_revision_mismatches':file_revision_mismatches,
        'namespace_drift':namespace_drift,
        'special_report_drift':report_drift,
        'non_main_revision_slots':non_main_slots,
    }
    hard_fail_keys=[k for k in failures if k not in {'special_report_drift','non_main_revision_slots'}]
    hard_fail=any(bool(failures[k]) for k in hard_fail_keys)
    slot_gap=bool(non_main_slots)

    report={
        'started_at':started,'completed_at':now(),'site':BASE,'api_endpoint':api.url,'api_calls':api.calls,
        'archive_snapshot':archive_audit.get('snapshot_completed'),
        'scope':'anonymous-readable current V1 pages + every public revision of those pages + category/template/file relationships',
        'live_namespace_count':len(namespaces),'live_page_count':len(live_pages),'archive_page_count':len(archive_records),
        'live_revision_count':live_revision_count,'archive_revision_count':archive_audit.get('revision_count'),
        'revision_bodies_compared':live_revision_bodies_checked,
        'slot_roles_seen':sorted(slot_roles),'non_main_slot_revision_count':len(non_main_slots),
        'public_hidden_revision_content_count':len(hidden_public_content),
        'category_count_live':len(live_cat_titles),'category_count_archive':len(arc_cat_records),
        'template_count_live':len(live_templates),'template_count_archive':len(arc_templates),
        'file_page_count_live':len(live_file_titles),'file_page_count_archive':len(arc_file_records),
        'public_delete_log_event_count':len(deletes),'public_delete_log_error':delete_log_error,
        'public_delete_log_events':deletes,
        'historical_boundary':{
            'current_existing_pages_fully_testable':True,
            'deleted_or_suppressed_page_bodies_recoverable_anonymously':False,
            'note':'A clean result proves fidelity for the anonymous-readable live V1 corpus and complete public histories of pages that currently exist. It cannot prove recovery of text deleted/suppressed before the archive snapshot without privileged XML/database/backups.'
        },
        'archive_main_slot_only_gap':slot_gap,
        'failures':failures,
        'content_fidelity_pass':not hard_fail and not slot_gap,
        'operational_drift_only':bool(report_drift) and not hard_fail and not slot_gap,
    }
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(0 if report['content_fidelity_pass'] else 1)


if __name__=='__main__':
    main()
