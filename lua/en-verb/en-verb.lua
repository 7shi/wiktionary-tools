start = 1
if arg[1] == "-s" then start = 2 end
if not arg[start] then
    print("usage: lua " .. arg[0] .. " [-s] word [args...]")
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
            if k > start then args[k - start] = v end
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
            return { text = arg[start], subpageText = arg[start], }
        end,
    },
    text    = require("text"),
    ustring = require("ustring/ustring"),
}
result = require("Module:en-headword").show(frame)
if start > 1 then result = string.gsub(result, "<.->", "") end
print(result)
