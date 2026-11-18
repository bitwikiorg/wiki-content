-- Lua 5.1 regression tests for metadata optionality and separate domain values.
-- Runs with a minimal MediaWiki stub, not a live MediaWiki/SMW parser.

mw = {
    text = {
        nowiki = function(value) return tostring(value) end,
    },
    loadData = function(name)
        assert(name == "Module:BITwiki/Data/Schema")
        return dofile("Module/BITwiki/Data/Schema.lua")
    end,
}

package.preload["Module:BITwiki/Core"] = function()
    return dofile("Module/BITwiki/Core.lua")
end
package.preload["Module:BITwiki/Compiler"] = function()
    return dofile("Module/BITwiki/Compiler.lua")
end

local Compiler = require("Module:BITwiki/Compiler")
local Structure = dofile("Module/Structure.lua")
local count = 0

local function check(condition, message)
    assert(condition, message)
    count = count + 1
end

local empty = Compiler.compileKnowledgeObject({})
check(empty.ok == true, "missing metadata must not block a valid subject")
check(#empty.diagnostics == 0, "missing optional fields must not manufacture errors")

local known = Compiler.compileKnowledgeObject({
    entity_type = "Concept",
    domain = "Biology, Philosophy",
    status = "Supported",
    provenance = "Cited sources",
})
check(known.ok, "known explicit metadata must remain valid")
check(#known.record.domains == 2, "multi-domain values must be separately parsed")
check(#known.diagnostics == 0, "known values must not create warnings")

local new_values = Compiler.compileKnowledgeObject({
    entity_type = "Species",
    domain = "History, Literature",
})
check(new_values.ok == true, "provisional classifications must not reject the subject")
check(#new_values.diagnostics == 3, "each unknown type/domain is a review signal")
for _, d in ipairs(new_values.diagnostics) do
    check(d.severity == "warning", "unregistered type/domain must be review-only")
end

local warning_markup = Structure.validateKnowledgeObject({
    args = {entity_type = "Species", domain = "History"}
})
check(
    string.find(warning_markup, "[[Category:BITwiki semantic vocabulary review]]", 1, true) ~= nil,
    "unregistered classifications must reach maintenance review"
)
check(
    string.find(warning_markup, "bitwiki-semantic-validation-error", 1, true) == nil,
    "unregistered classifications must not produce public error notices"
)

local bad = Compiler.compileKnowledgeObject({status = "Verified"})
check(not bad.ok, "unsupported explicit epistemic status must remain invalid")
check(bad.diagnostics[1].severity == "error", "unsupported status must be an error")
local bad_markup = Structure.validateKnowledgeObject({args = {status = "Verified"}})
check(
    string.find(bad_markup, "bitwiki-semantic-validation-error", 1, true) ~= nil,
    "invalid statuses must retain visible validation error"
)

local domain_markup = Structure.renderDomains({
    args = {domain = "Biology, Philosophy, Biology"}
})
check(
    domain_markup == "[[Domain::Biology]], [[Domain::Philosophy]]",
    "each unique domain must be emitted as a separate semantic assertion"
)
check(Structure.renderDomains({args = {}}) == "", "empty domains emit no assertion")

local status_markup = Structure.renderStatus({args = {status = "Established"}})
check(
    status_markup == "[[Epistemic status::Established]]",
    "valid explicit standing must render"
)
check(
    Structure.renderStatus({args = {status = "Verified"}}) == "''Unrecognized standing''",
    "invalid status must not be persisted as a semantic assertion"
)
check(Structure.renderStatus({args = {}}) == "", "absent status emits no assertion")

print("Semantic Lua contract tests: " .. count .. " assertions passed")
