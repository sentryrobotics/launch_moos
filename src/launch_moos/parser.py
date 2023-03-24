import pyparsing as pp


pp.ParserElement.set_default_whitespace_chars(" \t")
new_line = pp.Suppress("\n")
comment = pp.Suppress("//" + pp.CharsNotIn("\n"))
comment_line = comment + new_line
whitespace = pp.ZeroOrMore(pp.Literal(" ")).suppress()

variable = pp.Word(pp.alphas + "_")("name")
identifier_name = pp.Word(pp.alphanums + ".-_")
# TODO - this is a mess, define all permitted values properly
value_anything = whitespace + (
    pp.SkipTo(comment, include=True, failOn=new_line)("value")
    | pp.SkipTo(pp.Literal("\n"))("value")
)

assign_statement = variable("name") + pp.Suppress("=") + identifier_name("value")
assign_statement_line = pp.Group(
    variable + pp.Suppress("=") + value_anything + new_line
)

global_section = pp.ZeroOrMore(comment_line | assign_statement_line | new_line)

params = pp.ZeroOrMore(
    pp.Group((assign_statement + pp.Suppress(",")) ^ assign_statement)
)
moosname = "~" + identifier_name("moosname")
process_config_run_line = (
    pp.CaselessKeyword("Run")
    + pp.Suppress("=")
    + identifier_name("executable")
    + pp.Suppress("@")
    + params("params")
    + pp.Opt(moosname)
    + new_line
)

process_config_section = pp.ZeroOrMore(
    comment_line | pp.Group(process_config_run_line) | assign_statement_line | new_line
)
processconfig = (
    pp.CaselessKeyword("processconfig")
    + pp.Suppress("=")
    + identifier_name("processconfig_name")
    + new_line
    + pp.Suppress("{")
    + new_line
    + process_config_section("config")
    + pp.Suppress("}")
    + new_line
)

moos_file = pp.ZeroOrMore(
    pp.Group(processconfig) | comment_line | assign_statement_line | new_line
)
