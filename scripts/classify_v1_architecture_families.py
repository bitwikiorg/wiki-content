#!/usr/bin/env python3
"""Classify the 83 V1 architecture/system pages into maturation families.

This mapping is intentionally explicit. The V1 archive is fixed evidence and family
assignment is an auditable migration decision, not a fuzzy ontology classifier.
Architecture family is independent from lifecycle flags such as REVISED/parallel branch.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

INPUT = Path('v1-page-role-matrix.json')
OUTPUT = Path('v1-architecture-family-matrix.json')
EXPECTED_ARCHITECTURE_PAGES = 83

FAMILY_DESCRIPTIONS = {
    'foundational_constitutional_philosophy': 'Manifesto, Charter, Constitution, foundational worldview, and constitutional revision lineage.',
    'epistemics_evidence_provenance': 'Evidence, uncertainty, source hierarchy, provenance, claim validation, and epistemic frameworks.',
    'ontology_semantics_relationships': 'Entity/type systems, taxonomy, ontology alignment, semantic relations, and ontological experiments.',
    'composition_templates_transclusion': 'Templates, infoboxes, reusable composition, transclusion contracts, and template-system validation.',
    'semantic_schema_smw_queries_modules': 'Semantic MediaWiki property/schema machinery, query patterns, modules, dependencies, and technical schema references.',
    'navigation_portals_categories_visualization': 'Human/agent orientation architecture: categories, portals, glossary, graph visualization, and navigational views.',
    'quality_governance_stewardship': 'Governance, quality standards, stewardship, and operational review frameworks.',
    'deployment_integration_migration_operations': 'Deployment, integration, migration, user-facing operation, and performance constraints.',
    'research_synthesis_knowledge_systems': 'Research-synthesis patterns connecting external knowledge-system work back into BITwiki architecture.',
    'system_architecture_boundary': 'Top-level system architecture, organization, and BITwiki/BIThub/BITCORE boundary specifications.',
}

FAMILY_MEMBERS = {
    'foundational_constitutional_philosophy': {
        'BITCORE Manifesto', 'BITwiki Charter Revised', 'BITwiki Charter', 'BITwiki Constitution',
        'BITwiki Foundational Triad', 'Charter', 'PHILOSOPHICAL FRAMEWORK SUMMARY', 'REVISION SUMMARY',
    },
    'epistemics_evidence_provenance': {
        'BITwiki Claim Validation', 'BITwiki Epistemic Framework', 'BITwiki Epistemic Tiers',
        'BITwiki Epistemics Performative', 'BITwiki Evidence Evaluation', 'BITwiki Evidence Framework',
        'BITwiki Evidence Tiers', 'BITwiki Evidence and Epistemics', 'BITwiki Provenance Model',
        'BITwiki Source Hierarchy', 'BITwiki Source Types', 'BITwiki Uncertainty Markers',
        'Epistemic Audit Framework', 'Epistemic Framework Synthesis.REVISED', 'Epistemics', 'Provenance Model',
    },
    'ontology_semantics_relationships': {
        'BITwiki Entity Types.REVISED', 'BITwiki Entity Types', 'BITwiki Epistemic Status Taxonomy',
        'BITwiki Expanded Entity Types', 'BITwiki Ontology Alignment Matrix', 'BITwiki Ontology Performative',
        'BITwiki Relationship Pattern Catalog', 'BITwiki Relationship Types', 'BITwiki Semantic Patterns',
        'BITwiki Taxonomy Architecture', 'BITwiki Visual Diagram Specification', 'Ontology Alignment Matrix.REVISED',
        'Ontology Alignment Specification', 'Ontology', 'Validation rules', 'EPV Framework',
    },
    'composition_templates_transclusion': {
        'BITwiki Transclusion Rules', 'Doc', 'Infobox Concept', 'Infobox Idea', 'Infobox Implementation',
        'Infobox Project', 'SMW Template System', 'Template Catalog', 'Template Usage Guide',
        'Template System Validation Framework',
    },
    'semantic_schema_smw_queries_modules': {
        'BITwiki Page Types', 'BITwiki Property Dictionary', 'Citation Pattern Integration Guide',
        'Dependency Schema', 'Epistemic Properties', 'Event Types', 'Lua Module Specifications',
        'Property Types', 'Query Patterns', 'README', 'SMW Property Definitions', 'SMW Property Types Complete',
        'SMW Query Patterns Reference',
    },
    'navigation_portals_categories_visualization': {
        'BITwiki Glossary', 'CATEGORY ARCHITECTURE', 'Knowledge Graph Visualization', 'Portal Architecture Specification',
    },
    'quality_governance_stewardship': {
        'BITwiki Governance Framework', 'BITwiki Quality Bar', 'BITwiki Quality Standards',
        'BITwiki Steward Handbook', 'Governance Integration Coraline', 'Quality Validation Framework',
    },
    'deployment_integration_migration_operations': {
        'BITwiki Deployment Guide', 'BITwiki Integration Guide', 'BITwiki Performance Budgets',
        'BITwiki User Guide', 'Content Migration Guide',
    },
    'research_synthesis_knowledge_systems': {
        'Knowledge Engine Patterns',
    },
    'system_architecture_boundary': {
        'BITwiki Architecture Overview', 'BITwiki BITHUB Boundary Specification', 'System Architecture',
        'Wiki Organization Guidelines',
    },
}

TITLE_TO_FAMILY = {
    title: family
    for family, titles in FAMILY_MEMBERS.items()
    for title in titles
}


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(f'Missing {INPUT}; run scripts/classify_v1_page_roles.py first.')

    role_matrix = json.loads(INPUT.read_text(encoding='utf-8'))
    architecture_pages = [
        p for p in role_matrix.get('pages', [])
        if p.get('migration_role') == 'architecture_system_source'
    ]
    titles = {p['title'] for p in architecture_pages}
    mapped = set(TITLE_TO_FAMILY)
    missing = sorted(titles - mapped)
    stale = sorted(mapped - titles)

    if len(architecture_pages) != EXPECTED_ARCHITECTURE_PAGES:
        raise SystemExit(
            f'Expected {EXPECTED_ARCHITECTURE_PAGES} architecture/system pages, got {len(architecture_pages)}'
        )
    if missing or stale:
        raise SystemExit(f'Architecture family mapping mismatch. Missing={missing}; stale={stale}')

    rows = []
    counts = Counter()
    historical_variants = Counter()
    for page in architecture_pages:
        family = TITLE_TO_FAMILY[page['title']]
        counts[family] += 1
        if 'historical_variant_or_parallel_branch' in page.get('lifecycle_flags', []):
            historical_variants[family] += 1
        rows.append({
            'title': page['title'],
            'path': page['path'],
            'current_revid': page.get('current_revid'),
            'architecture_family': family,
            'family_description': FAMILY_DESCRIPTIONS[family],
            'lifecycle_flags': page.get('lifecycle_flags', []),
            'api_recorded_categories': page.get('api_recorded_categories', []),
            'infobox_type_source_parameter': page.get('infobox_type_source_parameter'),
        })

    rows.sort(key=lambda r: (r['architecture_family'], r['title'].casefold()))
    report = {
        'scope': 'V1 Main pages classified as architecture_system_source',
        'interpretation': (
            'Architecture families are maturation/research groupings, not V2 Entity types or namespaces. '
            'Lifecycle/branch state remains orthogonal and is preserved separately.'
        ),
        'family_vocabulary': FAMILY_DESCRIPTIONS,
        'summary': {
            'architecture_pages_classified': len(rows),
            'expected_architecture_pages': EXPECTED_ARCHITECTURE_PAGES,
            'complete': len(rows) == EXPECTED_ARCHITECTURE_PAGES and not missing and not stale,
            'family_counts': dict(sorted(counts.items())),
            'historical_variant_counts_by_family': dict(sorted(historical_variants.items())),
            'unmapped_pages': missing,
            'stale_mapping_titles': stale,
        },
        'pages': rows,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(report['summary'], indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
