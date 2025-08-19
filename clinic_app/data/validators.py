\
    from typing import Dict, Any, List
    from jinja2 import Environment, meta

    def missing_in_context(html: str, context: Dict[str, Any]) -> List[str]:
        env = Environment()
        ast = env.parse(html)
        vars_ = meta.find_undeclared_variables(ast)
        roots = set(k.split('.')[0] for k in vars_)
        avail = set(context.keys())
        return sorted([v for v in roots if v not in avail and v not in {"loop","self","super"}])
