from confload.cli import Parser, SubParser, String, Int, Float, Bool, Toggle, List


parser = Parser(
    [
        String("name"),
    ],
    [
        String("lastname", aliases=["lastname", "l"]),
        List("children", aliases=["child", "c"]),
        Toggle("active", aliases=["active", "y"], default=False),
    ],
)


print(str(parser))
print(parser.aliases)
res = parser()

print(res)
# python3 test_parser.py -l abcde --child dco,rzu --lastname trew -c aem -c dga,lfr test
# => {'name': 'test', 'lastname': 'trew', 'children': ['dco', 'rzu', 'aem', 'dga', 'lfr']}