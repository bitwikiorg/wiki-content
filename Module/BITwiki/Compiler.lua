-- Module:BITwiki/Compiler
-- Validate explicit identity assertions without treating incomplete editorial
-- metadata or a provisional classification as a reason to reject a subject.

local Core = require("Module:BITwiki/Core")
local Schema = mw.loadData("Module:BITwiki/Data/Schema")

local p = {}

local function validateControlled(field, value, vocabulary, diagnostics, severity)
    if value ~= "" and not vocabulary[value] then
        Core.appendDiagnostic(
            diagnostics,
            severity == "warning" and "vocabulary-review" or "unsupported-value",
            field,
            "unregistered " .. field .. " value '" .. value .. "'",
            severity or "error"
        )
    end
end

function p.compileKnowledgeObject(args)
    args = args or {}

    local domains = Core.splitComma(args.domain)
    local record = {
        entity_type = Core.trim(args.entity_type),
        domain = Core.trim(args.domain),
        domains = domains,
        status = Core.trim(args.status),
        provenance = Core.trim(args.provenance),
    }
    local diagnostics = {}

    -- The source-controlled vocabulary is a reviewed baseline, not an
    -- encyclopedia admission gate. Explicit novel types/domains are flagged
    -- for editorial normalization rather than silently replaced or rejected.
    validateControlled("entity_type", record.entity_type, Schema.entity_type, diagnostics, "warning")
    for _, domain in ipairs(domains) do
        validateControlled("domain", domain, Schema.domain, diagnostics, "warning")
    end

    -- Status is optional, but when asserted must retain its precise meaning.
    -- In particular, "Verified" and "Archived" are not evidentiary standings.
    validateControlled("status", record.status, Schema.status, diagnostics, "error")

    local has_errors = false
    for _, diagnostic in ipairs(diagnostics) do
        if diagnostic.severity == "error" then
            has_errors = true
            break
        end
    end

    return {
        ok = not has_errors,
        schema_version = Schema.schema_version,
        record = record,
        diagnostics = diagnostics,
    }
end

return p
