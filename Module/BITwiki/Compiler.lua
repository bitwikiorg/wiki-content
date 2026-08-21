-- Module:BITwiki/Compiler
-- Deterministic normalization/type-checking layer for BITwiki knowledge objects.

local Core = require("Module:BITwiki/Core")
local Schema = mw.loadData("Module:BITwiki/Data/Schema")

local p = {}
local REQUIRED = {"entity_type", "domain", "status", "provenance"}

local function validateRequired(record, diagnostics)
    for _, field in ipairs(REQUIRED) do
        if record[field] == "" then
            Core.appendDiagnostic(
                diagnostics,
                "required-field",
                field,
                field .. " is required",
                "error"
            )
        end
    end
end

local function validateControlled(field, value, vocabulary, diagnostics)
    if value ~= "" and not vocabulary[value] then
        Core.appendDiagnostic(
            diagnostics,
            "unsupported-value",
            field,
            "unsupported value '" .. value .. "'",
            "error"
        )
    end
end

local function validateDomains(domains, diagnostics)
    for _, domain in ipairs(domains) do
        validateControlled("domain", domain, Schema.domain, diagnostics)
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

    validateRequired(record, diagnostics)
    validateControlled("entity_type", record.entity_type, Schema.entity_type, diagnostics)
    validateDomains(domains, diagnostics)
    validateControlled("status", record.status, Schema.status, diagnostics)

    return {
        ok = #diagnostics == 0,
        schema_version = Schema.schema_version,
        record = record,
        diagnostics = diagnostics,
    }
end

return p
