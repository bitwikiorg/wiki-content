-- Module:Structure
-- Public/runtime validation wrapper for Template:Knowledge object.
-- Delegates normalization and type checking to Module:BITwiki/Compiler.
-- V1 numeric-confidence tiers remain intentionally excluded.

local Compiler = require("Module:BITwiki/Compiler")
local Core = require("Module:BITwiki/Core")

local p = {}

function p.validateKnowledgeObject(frame)
    local result = Compiler.compileKnowledgeObject(frame.args)

    if result.ok then
        return ""
    end

    local messages = {}
    for _, diagnostic in ipairs(result.diagnostics) do
        local field = Core.trim(diagnostic.field)
        local message = Core.trim(diagnostic.message)
        if field ~= "" then
            table.insert(messages, field .. ": " .. message)
        else
            table.insert(messages, message)
        end
    end

    local rendered = Core.escapeDiagnostic(table.concat(messages, "; "))
    return '<span class="error bitwiki-semantic-validation-error">'
        .. 'BITwiki semantic identity error: ' .. rendered
        .. '</span>[[Category:BITwiki semantic validation errors]]'
end

return p
