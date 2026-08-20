-- Module:Structure
-- BITwiki V2 runtime structure/identity validation.
-- V1 lineage: Lua Module Specifications + Template Validation Lua Module.
-- This module intentionally does not implement V1 numeric confidence tiers.

local p = {}

local VALID = {
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
}

local function trim(value)
    if value == nil then
        return ""
    end
    value = tostring(value)
    return value:match("^%s*(.-)%s*$") or ""
end

local function validate_required(args, errors)
    for _, field in ipairs({"entity_type", "domain", "status", "provenance"}) do
        if trim(args[field]) == "" then
            table.insert(errors, field .. " is required")
        end
    end
end

local function validate_vocab_value(field, value, errors)
    if value ~= "" and not VALID[field][value] then
        table.insert(errors, field .. " has unsupported value '" .. value .. "'")
    end
end

local function validate_domain(value, errors)
    for item in string.gmatch(value, "([^,]+)") do
        validate_vocab_value("domain", trim(item), errors)
    end
end

local function validate_vocab(args, errors)
    validate_vocab_value("entity_type", trim(args.entity_type), errors)
    validate_domain(trim(args.domain), errors)
    validate_vocab_value("status", trim(args.status), errors)
end

function p.validateKnowledgeObject(frame)
    local args = frame.args
    local errors = {}

    validate_required(args, errors)
    validate_vocab(args, errors)

    if #errors == 0 then
        return ""
    end

    local message = mw.text.nowiki(table.concat(errors, "; "))
    return '<span class="error bitwiki-semantic-validation-error">'
        .. 'BITwiki semantic identity error: ' .. message
        .. '</span>[[Category:BITwiki semantic validation errors]]'
end

return p
