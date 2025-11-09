from typingimport Dict
import ast 
import operator as op 

# safe eval for arthmetic expressions using ast
#supported operators
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult:mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
}




def _eval(node):
if isinstance(node, ast.Num): # <number>
return node.n
if isinstance(node, ast.BinOp):
left = _eval(node.left)
right = _eval(node.right)
operator = ALLOWED_OPERATORS[type(node.op)]
return operator(left, right)
if isinstance(node, ast.UnaryOp):
operand = _eval(node.operand)
operator = ALLOWED_OPERATORS[type(node.op)]
return operator(operand)
raise ValueError("Unsupported expression")




def tool_calculator(expr: str) -> Dict:
"""Safely evaluate a simple arithmetic expression and return structured result."""
try:
# parse expression
parsed = ast.parse(expr, mode='eval')
result = _eval(parsed.body)
return {"tool": "calculator", "input": expr, "output": str(result)}
except Exception as e:
return {"tool": "calculator", "input": expr, "output": f"error: {e}"}




def tool_web_search(query: str) -> Dict:
"""Mock web search for demo. Replace with real API integration later (SerpAPI / Bing / Google)."""
# Very small fake knowledge base for demo
KB = {
"react": "React is a JavaScript library for building user interfaces maintained by Facebook/Meta.",
"fastapi": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python.",
"python": "Python is a popular high-level programming language used for backend, data science, scripting, and more.",
}
summary = KB.get(query.lower(), f"Mock search result for '{query}': No real web access configured.")
return {"tool": "web_search", "input": query, "output": summary}
