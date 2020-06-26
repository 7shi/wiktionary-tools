if not arg[1] then
    print("usage: lua " .. arg[0] .. " parts word [args...]")
    return
end
lualib = "mediawiki-extensions-Scribunto/includes/engines/LuaCommon/lualib/"
package.path = lualib .. "?.lua;" .. lualib .. "mw.?.lua;" .. package.path
frame = {
    args = {"verbs"},
    title = word,
    getParent = function()
        args = {}
        for k, v in pairs(arg) do
            if k >= 2 then args[k - 1] = v end
        end
        return {args = args}
    end,
    expandTemplate = function(frame, title)
        --print(title.title)
    end,
}
mw = {
    getCurrentFrame = function()
        return frame
    end,
    loadData = require,
    title = {
        getCurrentTitle = function()
            return { text = arg[1], subpageText = arg[1], }
        end,
    },
    text    = require("text"),
    ustring = require("ustring/ustring"),
}
print(require("Module:en-headword").show(frame))
