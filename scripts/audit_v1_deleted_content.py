#!/usr/bin/env python3
import json, os, re, time
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE=os.getenv('BITWIKI_BASE_URL','https://bitwiki.org').rstrip('/')
INPUT=Path('v1-fidelity-audit.json')
ARCHIVE_INDEX=Path('archive-v1/index.json')
OUT=Path('v1-deleted-content-audit.json')
UA='BITwiki-V1-Deleted-Content-Audit/1.0 (+https://github.com/bitwikiorg/wiki-content)'


def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def rows(v): return v if isinstance(v,list) else list(v.values()) if isinstance(v,dict) else []


class API:
    def __init__(self):
        self.s=requests.Session(); self.s.headers.update({'User-Agent':UA}); self.calls=0; self.url=None
        for u in (BASE+'/w/api.php',BASE+'/api.php'):
            try:
                r=self.s.get(u,params={'action':'query','meta':'siteinfo','format':'json','formatversion':2},timeout=30)
                r.raise_for_status(); r.json(); self.url=u; break
            except Exception: pass
        if not self.url: raise RuntimeError('No API endpoint')
    def get(self,**p):
        self.calls+=1; p.update(format='json',formatversion=2,utf8=1)
        for n in range(5):
            try:
                r=self.s.get(self.url,params=p,timeout=60); r.raise_for_status(); data=r.json()
                time.sleep(.01); return data
            except Exception:
                if n==4: raise
                time.sleep(1+n)


def deleted_revisions(api,title):
    out=[]; cont={}; errors=[]
    while True:
        data=api.get(action='query',prop='deletedrevisions',titles=title,
                     drvprop='ids|timestamp|user|comment|flags|size|sha1|slotsize|slotsha1|contentmodel|roles|content|tags',
                     drvslots='*',drvlimit='max',**cont)
        if 'error' in data:
            errors.append(data['error']); return out,errors
        pages=rows((data.get('query') or {}).get('pages') or [])
        if pages: out.extend(pages[0].get('deletedrevisions') or [])
        cont=data.get('continue') or {}
        if not cont: return out,errors


def has_content(rev):
    for slot in (rev.get('slots') or {}).values():
        if 'content' in slot or '*' in slot: return True
    return '*' in rev


def normalized_candidates(title):
    vals={title}
    vals.add(re.sub(r'(?i)\s+final\s*$','',title).strip())
    vals.add(re.sub(r'(?i)\.final\s*$','',title).strip())
    vals.add(re.sub(r'(?i)^final\s+','',title).strip())
    vals.add(re.sub(r'(?i)\s+revised\s*$','',title).strip())
    return {v for v in vals if v}


def main():
    source=load(INPUT); archive=load(ARCHIVE_INDEX); api=API()
    live_titles={(int(r['ns']),r['title']) for r in archive.get('records') or []}
    events=source.get('public_delete_log_events') or []
    delete_events=[e for e in events if e.get('action')=='delete']
    restore_events=[e for e in events if e.get('action') in {'restore','undelete'}]
    other_events=[e for e in events if e.get('action') not in {'delete','restore','undelete'}]
    unique=[]; seen=set()
    for e in delete_events:
        key=(int(e.get('ns',0)),e.get('title'))
        if key not in seen: seen.add(key); unique.append(key)

    records=[]; total_deleted_revisions=0; readable_deleted_revisions=0; content_readable=0
    permission_errors=0; exact_recreated=0; normalized_survivor=0
    comments={}
    for e in delete_events:
        c=e.get('comment') or ''
        comments[c]=comments.get(c,0)+1

    for i,(ns,title) in enumerate(unique,1):
        revs,errors=deleted_revisions(api,title)
        total_deleted_revisions += len(revs)
        readable_deleted_revisions += len(revs)
        ccount=sum(1 for r in revs if has_content(r)); content_readable += ccount
        if errors: permission_errors += 1
        exact=(ns,title) in live_titles
        counterpart=None
        if not exact:
            for c in normalized_candidates(title):
                if c != title and (ns,c) in live_titles:
                    counterpart=c; break
        exact_recreated += int(exact); normalized_survivor += int(counterpart is not None)
        records.append({
            'ns':ns,'title':title,'delete_event_count':sum(1 for e in delete_events if int(e.get('ns',0))==ns and e.get('title')==title),
            'currently_exists_exact':exact,'obvious_normalized_survivor':counterpart,
            'deleted_revision_metadata_returned':len(revs),'deleted_revision_content_returned':ccount,
            'api_errors':errors,
            'deleted_revision_ids':[r.get('revid') for r in revs],
            'deleted_revision_sha1':[r.get('sha1') for r in revs],
        })
        if i%25==0 or i==len(unique): print(f'deleted titles {i}/{len(unique)}')

    report={
        'completed_at':now(),'site':BASE,'api_endpoint':api.url,'api_calls':api.calls,
        'public_delete_log_events_total':len(events),'delete_actions':len(delete_events),'restore_actions':len(restore_events),'other_delete_log_actions':len(other_events),
        'unique_deleted_titles':len(unique),'currently_recreated_exact_titles':exact_recreated,'obvious_normalized_survivors':normalized_survivor,
        'deleted_revision_records_returned_anonymously':readable_deleted_revisions,
        'deleted_revision_bodies_returned_anonymously':content_readable,
        'titles_with_deleted_revision_api_errors':permission_errors,
        'delete_comment_frequencies':sorted([{'comment':k,'count':v} for k,v in comments.items()],key=lambda x:(-x['count'],x['comment'])),
        'records':records,
        'historical_content_complete_from_public_sources': len(unique)==0 or content_readable>0 and all(r['deleted_revision_content_returned']==r['deleted_revision_metadata_returned'] and not r['api_errors'] for r in records),
        'conclusion_note':'Current live V1 fidelity is independently verified elsewhere. This report tests whether deleted pre-snapshot content can also be recovered anonymously. If deleted revision bodies are not returned, an admin XML export/database/backup is required to prove complete historical V1 recovery.'
    }
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
