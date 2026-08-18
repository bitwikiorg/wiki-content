#!/usr/bin/env python3
import json, re
from pathlib import Path

ROOTS=['Main','BITwiki','Portal','Template','Property','Category']
CATEGORY_RE=re.compile(r'\[\[\s*Category:([^\]|#]+)',re.I)
TEMPLATE_RE=re.compile(r'(?<!\{)\{\{(?!\{)\s*([^{}|\n]+)')
REDIRECT_RE=re.compile(r'^\s*#redirect\s*\[\[',re.I|re.M)
LITERAL_BLOCK_RE=re.compile(
    r'<!--.*?-->|<(pre|nowiki|syntaxhighlight|source)\b[^>]*>.*?</\1\s*>',
    re.I | re.S,
)
MAGIC_WORDS={
'PAGENAME','PAGENAMEE','FULLPAGENAME','FULLPAGENAMEE','BASEPAGENAME','BASEPAGENAMEE',
'SUBPAGENAME','SUBPAGENAMEE','ROOTPAGENAME','ROOTPAGENAMEE','NAMESPACE','NAMESPACEE',
'NAMESPACENUMBER','TALKSPACE','TALKSPACEE','SUBJECTSPACE','SUBJECTSPACEE','ARTICLESPACE',
'ARTICLESPACEE','TALKPAGENAME','TALKPAGENAMEE','SUBJECTPAGENAME','SUBJECTPAGENAMEE',
'ARTICLEPAGENAME','ARTICLEPAGENAMEE','REVISIONID','REVISIONDAY','REVISIONDAY2','REVISIONMONTH',
'REVISIONMONTH1','REVISIONYEAR','REVISIONTIMESTAMP','REVISIONUSER','CURRENTYEAR','CURRENTMONTH',
'CURRENTMONTH1','CURRENTMONTHNAME','CURRENTMONTHABBREV','CURRENTDAY','CURRENTDAY2','CURRENTDOW',
'CURRENTDAYNAME','CURRENTTIME','CURRENTHOUR','CURRENTWEEK','CURRENTTIMESTAMP','LOCALYEAR',
'LOCALMONTH','LOCALMONTH1','LOCALMONTHNAME','LOCALMONTHABBREV','LOCALDAY','LOCALDAY2','LOCALDOW',
'LOCALDAYNAME','LOCALTIME','LOCALHOUR','LOCALWEEK','LOCALTIMESTAMP','NUMBEROFPAGES',
'NUMBEROFARTICLES','NUMBEROFFILES','NUMBEROFEDITS','NUMBEROFVIEWS','NUMBEROFUSERS',
'NUMBEROFADMINS','NUMBEROFACTIVEUSERS','NUMBERINGROUP','NUMBERINGROUPE','CONTENTLANG',
'CONTENTLANGUAGE','DIRECTIONMARK','DIRMARK','SITENAME','SERVER','SERVERNAME','SCRIPTPATH',
'STYLEPATH','CURRENTVERSION','PROTECTIONLEVEL','PROTECTIONEXPIRY','DISPLAYTITLE','DEFAULTSORT'
}

ALLOWED_ENTITY_TYPES={
'Concept','Method','Protocol','Implementation','Project','Dataset','Person','Organization',
'Event','Publication','Location','Technology'
}
ALLOWED_DOMAINS={
'Systems science','Science','Biology','Mathematics','Philosophy','Technology','Electronics',
'Energy','Engineering','Chemistry','Physics','Medicine'
}
ALLOWED_EPISTEMIC_STATUSES={
'Hypothetical','Emerging','Supported','Well-supported','Established','Disputed'
}
REQUIRED_KNOWLEDGE_FIELDS=('entity_type','domain','status','provenance')


def title(s):
    return re.sub(r'\s+',' ',s.replace('_',' ').strip())


def files(root):
    p=Path(root)
    return sorted(p.rglob('*.mediawiki')) if p.exists() else []


def executable_text(text):
    return LITERAL_BLOCK_RE.sub('', text)


def template_params(text,name):
    """Parse current line-oriented V2 template calls; sufficient for identity validation."""
    match=re.search(r'{{\s*'+re.escape(name)+r'\b(.*?)}}',text,re.I|re.S)
    if not match:
        return None
    params={}
    for part in match.group(1).split('|')[1:]:
        if '=' not in part:
            continue
        key,value=part.split('=',1)
        key=title(key).casefold().replace(' ','_')
        value=title(value)
        if key:
            params[key]=value
    return params


def main():
    all_files=[p for r in ROOTS for p in files(r)]
    category_pages={title(p.relative_to('Category').as_posix()[:-10]) for p in files('Category')}
    template_pages={title(p.relative_to('Template').as_posix()[:-10]) for p in files('Template')}
    category_refs={}
    template_refs={}
    uncategorized=[]
    knowledge_objects=[]
    missing_knowledge_fields=[]
    invalid_entity_types=[]
    invalid_domains=[]
    invalid_epistemic_statuses=[]

    for p in all_files:
        text=p.read_text(encoding='utf-8')
        parsed=executable_text(text)
        cats=sorted({title(x) for x in CATEGORY_RE.findall(parsed) if '{' not in x})
        for c in cats: category_refs.setdefault(c,[]).append(str(p))

        temps=[]
        for raw in TEMPLATE_RE.findall(parsed):
            t=title(raw)
            low=t.casefold()
            if not t or t.startswith(('#',':','!')) or '{' in t or low.startswith(('subst:','safesubst:')):
                continue
            if t.upper() in MAGIC_WORDS:
                continue
            if ':' in t and t.split(':',1)[0].casefold() in {'int','msg','msgnw'}:
                continue
            temps.append(t)
        for t in sorted(set(temps)): template_refs.setdefault(t,[]).append(str(p))

        if p.parts[0] in {'Main','BITwiki','Portal','Template'} and not cats:
            uncategorized.append(str(p))

        # Identity validation applies to instantiated calls, not Template/Property documentation.
        if p.parts[0] not in {'Template','Property'} and not REDIRECT_RE.search(parsed):
            ko=template_params(parsed,'Knowledge object')
            if ko is not None:
                knowledge_objects.append(str(p))
                missing=[field for field in REQUIRED_KNOWLEDGE_FIELDS if not ko.get(field)]
                if missing:
                    missing_knowledge_fields.append({'path':str(p),'missing':missing})
                entity_type=ko.get('entity_type')
                if entity_type and entity_type not in ALLOWED_ENTITY_TYPES:
                    invalid_entity_types.append({'path':str(p),'value':entity_type})
                domain_text=ko.get('domain')
                if domain_text:
                    for domain in [title(x) for x in domain_text.split(',') if title(x)]:
                        if domain not in ALLOWED_DOMAINS:
                            invalid_domains.append({'path':str(p),'value':domain})
                status=ko.get('status')
                if status and status not in ALLOWED_EPISTEMIC_STATUSES:
                    invalid_epistemic_statuses.append({'path':str(p),'value':status})

    missing_categories={k:v for k,v in category_refs.items() if k not in category_pages}
    missing_templates={k:v for k,v in template_refs.items() if k not in template_pages}
    required_domains=sorted(ALLOWED_DOMAINS)
    missing_domain_categories=[x for x in required_domains if x not in category_pages]
    missing_domain_portals=[x for x in required_domains if not Path('Portal',x+'.mediawiki').exists()]
    exemplars=[p for p in files('Main') if '[[Category:Domain exemplars]]' in p.read_text(encoding='utf-8')]

    report={
      'deployable_mediawiki_files':len(all_files),
      'category_pages':len(category_pages),
      'template_pages':len(template_pages),
      'distinct_category_references':len(category_refs),
      'distinct_template_references':len(template_refs),
      'missing_category_pages':missing_categories,
      'missing_template_pages':missing_templates,
      'uncategorized_deployable_pages':uncategorized,
      'required_domain_categories_missing':missing_domain_categories,
      'required_domain_portals_missing':missing_domain_portals,
      'domain_exemplar_count':len(exemplars),
      'domain_exemplars':[str(p) for p in exemplars],
      'knowledge_object_count':len(knowledge_objects),
      'knowledge_object_pages':knowledge_objects,
      'knowledge_object_required_fields_missing':missing_knowledge_fields,
      'invalid_entity_type_values':invalid_entity_types,
      'invalid_domain_values':invalid_domains,
      'invalid_epistemic_status_values':invalid_epistemic_statuses,
      'controlled_vocabularies':{
        'entity_types':sorted(ALLOWED_ENTITY_TYPES),
        'domains':sorted(ALLOWED_DOMAINS),
        'epistemic_statuses':sorted(ALLOWED_EPISTEMIC_STATUSES),
      },
    }
    report['valid']=not any([
      missing_categories,missing_templates,uncategorized,missing_domain_categories,
      missing_domain_portals,len(exemplars)!=12,missing_knowledge_fields,invalid_entity_types,
      invalid_domains,invalid_epistemic_statuses
    ])
    Path('v2-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
    raise SystemExit(0 if report['valid'] else 1)

if __name__=='__main__': main()
