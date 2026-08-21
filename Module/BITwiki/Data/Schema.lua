-- Module:BITwiki/Data/Schema
-- Runtime projection of /bitwiki-runtime-schema.json.
-- Keep this file synchronized with the repository authority; CI validates drift.

return {
    schema_version = "0.1.0",
    entity_type = {
        ["Concept"] = true,
        ["Method"] = true,
        ["Protocol"] = true,
        ["Implementation"] = true,
        ["Project"] = true,
        ["Dataset"] = true,
        ["Person"] = true,
        ["Organization"] = true,
        ["Event"] = true,
        ["Publication"] = true,
        ["Location"] = true,
        ["Technology"] = true,
    },
    domain = {
        ["Systems science"] = true,
        ["Science"] = true,
        ["Biology"] = true,
        ["Computer science"] = true,
        ["Mathematics"] = true,
        ["Philosophy"] = true,
        ["Technology"] = true,
        ["Electronics"] = true,
        ["Energy"] = true,
        ["Engineering"] = true,
        ["Chemistry"] = true,
        ["Physics"] = true,
        ["Medicine"] = true,
    },
    status = {
        ["Hypothetical"] = true,
        ["Emerging"] = true,
        ["Supported"] = true,
        ["Well-supported"] = true,
        ["Established"] = true,
        ["Disputed"] = true,
    },
    relationships = {
        ["Related to"] = {
            inverse_display = "Related to",
            derive_inverse_assertion = false,
        },
        ["Implements"] = {
            inverse_display = "Implemented by",
            derive_inverse_assertion = false,
        },
        ["Part of"] = {
            inverse_display = "Has part",
            derive_inverse_assertion = false,
        },
        ["Depends on"] = {
            inverse_display = "Dependency of",
            derive_inverse_assertion = false,
        },
        ["Supports"] = {
            inverse_display = "Supported by",
            derive_inverse_assertion = false,
        },
        ["Contradicts"] = {
            inverse_display = "Contradicted by",
            derive_inverse_assertion = false,
        },
        ["Refines"] = {
            inverse_display = "Refined by",
            derive_inverse_assertion = false,
        },
        ["Derived from"] = {
            inverse_display = "Source of",
            derive_inverse_assertion = false,
        },
    },
}
