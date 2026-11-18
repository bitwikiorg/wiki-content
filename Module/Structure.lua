-- Module:Structure
-- Public/runtime wrapper for Template:Knowledge object.
-- Explicit metadata is optional; unregistered type/domain values are queued
-- for semantic vocabulary review, while invalid status assertions remain errors.

local Compiler = require("Module:BITwiki/Compiler")
local Core = require("Module:BITwiki/Core")
local Schema = mw.loadData("Module:BITwiki/Data/Schema")

local p = {}

function p.validateKnowledgeObject(frame)
    local result = Compiler.compileKnowledgeObject(frame.args)
    local errors = {}
    local has_warnings = false

    for _, diagnostic in ipairs(result.diagnostics) do
        if diagnostic.severity == "warning" then
            has_warnings = true
        else
            local field = Core.trim(diagnostic.field)
            local message = Core.trim(diagnostic.message)
            if field ~= "" then
                table.insert(errors, field .. ": " .. message)
            else
                table.insert(errors, message)
            end
        end
    end

    local output = {}
    if #errors > 0 then
        local rendered = Core.escapeDiagnostic(table.concat(errors, "; "))
        table.insert(output, '<span class="error bitwiki-semantic-validation-error">'
            .. 'BITwiki semantic identity error: ' .. rendered
            .. '</span>[[Category:BITwiki semantic validation errors]]')
    end
    if has_warnings then
        table.insert(output, "[[Category:BITwiki semantic vocabulary review]]")
    end

    return table.concat(output)
end

function p.renderDomains(frame)
    -- Emit separate semantic Text-property values, not one comma-containing
    -- annotation. Keep the printed terms visible in the infobox.
    local domains = Core.splitComma(frame.args.domain)
    local seen, rendered = {}, {}
    for _, domain in ipairs(domains) do
        if not seen[domain] then
            seen[domain] = true
            table.insert(rendered, "[[Domain::" .. Core.escapeDiagnostic(domain) .. "]]")
        end
    end
    return table.concat(rendered, ", ")
end

function p.renderStatus(frame)
    local status = Core.trim(frame.args.status)
    if status == "" then
        return ""
    end
    if not Schema.status[status] then
        -- Do not silently store invalid epistemic status as a semantic fact.
        return "''Unrecognized standing''"
    end
    return "[[Epistemic status::" .. Core.escapeDiagnostic(status) .. "]]"
end

return p
