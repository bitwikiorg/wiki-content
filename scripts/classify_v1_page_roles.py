#!/usr/bin/env python3
"""Classify every archived V1 Main page by migration role before ontology.

The roles in this file are migration-analysis roles, not BITwiki entity types. They answer
what job a historical page artifact performs during V1 -> V2 maturation so that only
actual subject-knowledge objects directly pressure the V2 ontology.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

INPUT = Path('v1-classification-usage.json')
OUTPUT = Path('v1-page-role-matrix.json')
EXPECTED_V1_MAIN_PAGES = 162

ROLES = {
    'canonical_subject_candidate',
    'architecture_system_source',
    'book_matter_reusable',
    'navigation_interface',
    'maintenance_validation_test',
    'unresolved',
}

DIRECT_SUBJECT_PAGES = {
    'Bioluminescent Organisms',
    'Fluorescent Coral Reefs',
}

NAVIGATION_EXACT = {
    'BITwiki How to Navigate',
    'BITwiki Master Navigation',
    'BITwiki Ontology Index',
    'BITwiki Start Here',
    'Category List',
    'Component List',
    'Concept Catalog',
    'Constitutional index',
    'Evidence epistemics index',
    'Governance index',
    'INDEX',
    'MASTER INDEX',
    'Main Page',
    'Main Page styled',
    'Ontology index',
    'Portal List',
    'Property Definitions Index',
    'Research Synthesis Index',
    'Schema matter index',
    'Site notice',
    'Template List',
}

MAINTENANCE_EXACT = {
    'PHASE3 DEPLOYMENT AUDIT',
    'Template Improvement Recommendations',
    'Template Validation Implementation',
    'Template Validation Lua Module',
    'Template Validation Report',
    'Test Page',
}

BOOK_MATTER_CATEGORIES = {
    'Definition Fragments',
    'Evidence Summary Fragments',
    'Main Page Sections',
    'Methodology Fragments',
    'Protocol Fragments',
    'Topic Sections',
    'Transcludable Content',
}

BOOK_MATTER_EXACT = {
    'Component Implementation section',
    'Component Knowledge graph section',
    'Component Portals section',
    'Component Semantic section',
    'Component Transclusion section',
    'Component:Implementation section',
    'Component:Knowledge graph section',
    'Component:Portals section',
    'Component:Semantic section',
    'Component:Transclusion section',
}

SYSTEM_INFOBOX_TYPES = {
    'architecture-overview', 'constitutional', 'deployment-guide', 'documentation',
    'evidence-epistemics', 'front-matter', 'glossary', 'governance',
    'governance specification', 'guide', 'integration-guide', 'master-index',
    'migration-guide', 'ontology', 'processual', 'quality-framework',
    'quality-standards', 'reference', 'research-synthesis', 'schema-matter',
    'specification', 'steward-handbook', 'technical specification',
    'technical-guide', 'technical-reference', 'technical-specification', 'template',
    'template-system', 'user-guide', 'validation-framework',
}

SYSTEM_TITLE_PREFIXES = (
    'BITwiki ', 'BITCORE ', 'CATEGORY ARCHITECTURE', 'Charter',
    'Citation Pattern Integration Guide', 'Dependency Schema', 'Doc', 'EPV Framework',
    'Epistemic Audit Framework', 'Epistemic Framework Synthesis', 'Epistemic Properties',
    'Epistemics', 'Event Types', 'Governance Integration', 'Infobox ',
    'Knowledge Engine Patterns', 'Knowledge Graph Visualization', 'Lua Module Specifications',
    'Ontology Alignment', 'Ontology', 'PHILOSOPHICAL FRAMEWORK SUMMARY',
    'Portal Architecture Specification', 'Property Types', 'Provenance Model',
    'Quality Validation Framework', 'Query Patterns', 'README', 'REVISION SUMMARY',
    'SMW ', 'System Architecture', 'Template Catalog', 'Template System Validation Framework',
    'Validation rules', 'Wiki Organization Guidelines',
)

HISTORICAL_VARIANT_PATTERNS = (
    re.compile(r'\.REVISED$', re.I),
    re.compile(r'\bRevised$', re.I),
    re.compile(r'\bstyled$', re.I),
    re.compile(r'^Component:', re.I),
    re.compile(r'Coraline', re.I),
    re.compile(r'^REVISION SUMMARY$', re.I),
)


def role_for(page: dict) -> tuple[str, str, list[str]]:
    title = page['title']
    categories = set(page.get('api_recorded_categories') or [])
    infobox_type = (page.get('infobox_type_source_parameter') or '').casefold()
    signals: list[str] = []

    if title in DIRECT_SUBJECT_PAGES:
        signals.append('explicit_first_class_real_world_subject_or_project')
        return (
            'canonical_subject_candidate',
            'Coherent first-class subject/project page with its own composed content; review for V2 canonicalization.',
            signals,
        )

    if page.get('is_subpage'):
        signals.append('historical_main_namespace_subpage')
        return (
            'book_matter_reusable',
            'Historical subpage composed into a parent knowledge page; migrate as composition/Book Matter evidence before ontology.',
            signals,
        )

    matched_book_categories = sorted(categories & BOOK_MATTER_CATEGORIES)
    if matched_book_categories or title in BOOK_MATTER_EXACT or title.endswith(' section'):
        if matched_book_categories:
            signals.extend(f'category:{c}' for c in matched_book_categories)
        if title in BOOK_MATTER_EXACT or title.endswith(' section'):
            signals.append('section_or_component_title')
        return (
            'book_matter_reusable',
            'Fragment, section, or transcludable content artifact; its subject signal may seed a canonical page but the artifact itself is composition machinery.',
            signals,
        )

    if title in NAVIGATION_EXACT or re.search(r'(^| )index$', title, re.I) or title.endswith(' List'):
        signals.append('index_list_main_or_navigation_surface')
        return (
            'navigation_interface',
            'Human/agent orientation, index, list, landing, or interface surface rather than a subject ontology object.',
            signals,
        )

    if title in MAINTENANCE_EXACT:
        signals.append('explicit_audit_test_or_validation_implementation')
        return (
            'maintenance_validation_test',
            'Operational audit/test/validation artifact; preserve as implementation history or maintenance evidence, not subject knowledge.',
            signals,
        )

    if infobox_type in SYSTEM_INFOBOX_TYPES:
        signals.append(f'infobox_page_role:{infobox_type}')
    if title.startswith(SYSTEM_TITLE_PREFIXES):
        signals.append('system_or_meta_title')
    if signals:
        return (
            'architecture_system_source',
            'BITwiki/BITCORE architecture, ontology, schema, epistemics, governance, constitutional, documentation, or system-design source.',
            signals,
        )

    return (
        'unresolved',
        'No high-confidence migration-role rule matched; requires direct revision/content review.',
        [],
    )


def lifecycle_flags(page: dict) -> list[str]:
    title = page['title']
    flags = []
    if any(pattern.search(title) for pattern in HISTORICAL_VARIANT_PATTERNS):
        flags.append('historical_variant_or_parallel_branch')
    if title.startswith('Component:'):
        flags.append('parallel_component_naming_surface')
    if title == 'Main Page styled':
        flags.append('alternate_presentation_surface')
    if page.get('revision_count', 0) and page['revision_count'] > 1:
        flags.append('has_preserved_revision_history')
    return flags


def composition_signal(page: dict) -> str | None:
    categories = set(page.get('api_recorded_categories') or [])
    if 'Definition Fragments' in categories:
        return 'concept_definition_fragment'
    if 'Methodology Fragments' in categories:
        return 'method_fragment'
    if 'Protocol Fragments' in categories:
        return 'protocol_fragment'
    if 'Evidence Summary Fragments' in categories:
        return 'evidence_summary_fragment'
    if 'Topic Sections' in categories or 'Transcludable Content' in categories:
        return 'generic_topic_section'
    if 'Main Page Sections' in categories or page['title'].endswith(' section'):
        return 'navigation_or_landing_section'
    if page.get('is_subpage'):
        return 'parent_page_subpage'
    return None


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(f'Missing {INPUT}; run scripts/inventory_corpus.py first.')

    source = json.loads(INPUT.read_text(encoding='utf-8'))
    pages = []
    role_counts = Counter()
    lifecycle_counts = Counter()
    composition_counts = Counter()

    for page in source.get('pages', []):
        role, rationale, signals = role_for(page)
        assert role in ROLES
        flags = lifecycle_flags(page)
        comp = composition_signal(page)
        role_counts[role] += 1
        for flag in flags:
            lifecycle_counts[flag] += 1
        if comp:
            composition_counts[comp] += 1

        pages.append({
            'title': page['title'],
            'path': page['path'],
            'pageid': page.get('pageid'),
            'current_revid': page.get('current_revid'),
            'revision_count': page.get('revision_count'),
            'migration_role': role,
            'role_rationale': rationale,
            'role_evidence_signals': signals,
            'lifecycle_flags': flags,
            'composition_signal': comp,
            'api_recorded_categories': page.get('api_recorded_categories', []),
            'api_recorded_identity_categories': page.get('api_recorded_identity_categories', []),
            'infobox_type_source_parameter': page.get('infobox_type_source_parameter'),
            'classification_annotation_source_syntax': page.get('classification_annotation_source_syntax', []),
        })

    unresolved = [p['title'] for p in pages if p['migration_role'] == 'unresolved']
    subject_candidates = [p['title'] for p in pages if p['migration_role'] == 'canonical_subject_candidate']
    reusable_subject_signals = [
        {'title': p['title'], 'composition_signal': p['composition_signal']}
        for p in pages
        if p['migration_role'] == 'book_matter_reusable' and p['composition_signal'] in {
            'concept_definition_fragment', 'method_fragment', 'protocol_fragment', 'evidence_summary_fragment'
        }
    ]

    report = {
        'scope': 'all archived V1 Main pages',
        'interpretation': (
            'Migration roles classify historical page artifacts by operational/content job before ontology. '
            'They are not Entity type values and do not decide final V2 canonicalization by themselves.'
        ),
        'role_vocabulary': {
            'canonical_subject_candidate': 'First-class real-world subject/project object that may directly pressure V2 Entity type/Domain vocabulary.',
            'architecture_system_source': 'BITwiki/BITCORE architecture, schema, governance, constitutional, epistemic, or documentation source.',
            'book_matter_reusable': 'Reusable section, fragment, or subpage whose content may seed canonical knowledge but whose historical artifact role is compositional.',
            'navigation_interface': 'Index, list, landing, notice, or navigation/orientation surface.',
            'maintenance_validation_test': 'Operational audit, test, validation implementation, or maintenance artifact.',
            'unresolved': 'Insufficient evidence for a high-confidence role assignment.',
        },
        'summary': {
            'pages_classified': len(pages),
            'expected_v1_main_pages': EXPECTED_V1_MAIN_PAGES,
            'complete': len(pages) == EXPECTED_V1_MAIN_PAGES and not unresolved,
            'role_counts': dict(sorted(role_counts.items())),
            'lifecycle_flag_counts': dict(sorted(lifecycle_counts.items())),
            'composition_signal_counts': dict(sorted(composition_counts.items())),
            'canonical_subject_candidates': subject_candidates,
            'reusable_subject_signal_fragments': reusable_subject_signals,
            'unresolved_pages': unresolved,
        },
        'pages': pages,
    }

    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(report['summary'], indent=2, ensure_ascii=False))

    if len(pages) != EXPECTED_V1_MAIN_PAGES:
        raise SystemExit(f'Expected {EXPECTED_V1_MAIN_PAGES} V1 Main pages, got {len(pages)}')
    if unresolved:
        raise SystemExit(f'Unresolved V1 page roles: {unresolved}')


if __name__ == '__main__':
    main()
