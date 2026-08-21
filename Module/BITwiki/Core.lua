-- Module:BITwiki/Core
-- Shared deterministic helpers for BITwiki Scribunto modules.

local p = {}

function p.trim(value)
    if value == nil then
        return ""
    end
    value = tostring(value)
    return value:match("^%s*(.-)%s*$") or ""
end

function p.splitComma(value)
    local out = {}
    local text = p.trim(value)
    if text == "" then
        return out
    end

    for item in string.gmatch(text, "([^,]+)") do
        local normalized = p.trim(item)
        if normalized ~= "" then
            table.insert(out, normalized)
        end
    end
    return out
end

function p.appendDiagnostic(diagnostics, code, field, message, severity)
    table.insert(diagnostics, {
        code = code,
        field = field,
        message = message,
        severity = severity or "error",
    })
end

function p.escapeDiagnostic(value)
    return mw.text.nowiki(p.trim(value))
end

return p
