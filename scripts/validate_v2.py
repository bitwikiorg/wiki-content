#!/usr/bin/env python3
import json, re
from pathlib import Path

ROOTS=['Main','BITwiki','Portal','Template','Property','Category']
CATEGORY_RE=re.compile(r'\[\[\s*Category:([^\]|#]+)',re.I)
# Exactly two braces: do not mistake template parameters {{{name}}} for transclusions.
TEMPLATE_RE=re.compile(r'(?<!\{)\{\{(?!\{)\s*([^{}|\n]+)')
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

def title(s):
    return re.sub(r'\s+',' ',s.replace('_',' ').strip())

def files(root):
    p=Path(root)
    return sorted(p.rglob('*.mediawiki')) if p.exists() else []

def main():
    all_files=[p for r in ROOTS for p in files(r)]
    category_pages={title(p.relative_to('Category').as_posix()[:-10]) for p in files('Category')}
    template_pages={title(p.relative_to('Template').as_posix()[:-10]) for p in files('Template')}
    category_refs={}
    template_refs={}
    uncategorized=[]
    for p in all_files:
        text=p.read_text(encoding='utf-8')
        cats=sorted({title(x) for x in CATEGORY_RE.findall(text) if '{' not in x})
        for c in cats: category_refs.setdefault(c,[]).append(str(p))
        temps=[]
        for raw in TEMPLATE_RE.findall(text):
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

    missing_categories={k:v for k,v in category_refs.items() if k not in category_pages}
    missing_templates={k:v for k,v in template_refs.items() if k not in template_pages}
    required_domains=['Systems science','Science','Biology','Mathematics','Philosophy','Technology','Electronics','Energy','Engineering','Chemistry','Physics','Medicine']
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
    }
    report['valid']=not any([
      missing_categories,missing_templates,uncategorized,missing_domain_categories,missing_domain_portals,len(exemplars)!=12
    ])
    Path('v2-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
    raise SystemExit(0 if report['valid'] else 1)

if __name__=='__main__': main()
