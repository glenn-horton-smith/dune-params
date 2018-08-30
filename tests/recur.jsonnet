
local addctx = function(obj, ctx=[])
if std.objectHas(obj, 'text')
then obj + { context: ctx }
else { [k]:addctx(obj[k], ctx+[k]) for k in std.objectFields(obj) };


local top = {
    a: {
        b: {
            c: {
                param1: {
                    text: "a-b-c-param1",
                },
            },
            param1: {
                text: "a-b-param2",
            },
        }
    }
};

addctx(top)
