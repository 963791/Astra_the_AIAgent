# agent.py
# Use Chat Completions
resp = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=prompt_messages,
max_tokens=400,
temperature=0.2,
)
return resp.choices[0].message.content




async def run_agent_stream(user_msg: str) -> AsyncGenerator[str, None]:
"""Generator that yields SSE-formatted chunks (strings) for streaming responses to frontend."""
tool = decide_tool(user_msg)


# If calculator tool
if tool == "calculator":
# naive extraction: find expression after keywords
expr = user_msg
for kw in ["calculate", "compute", "evaluate", "what is", "solve"]:
if kw in expr.lower():
expr = expr.lower().split(kw, 1)[-1].strip()
break
# fallback: use whole message
res = tool_calculator(expr)
yield f"data: [tool:calculator] {res['output']}\n\n"
# Ask LLM to present it nicely
prompt = [
{"role": "system", "content": "You are Astra, a friendly and concise assistant."},
{"role": "user", "content": f"User asked: {user_msg}\nCalculator result: {res['output']}\nPlease give a short friendly response."}
]
llm_resp = await call_openai_chat(prompt)
# stream in parts
for i in range(0, len(llm_resp), 120):
yield f"data: {llm_resp[i:i+120]}\n\n"
return


# If web_search tool
if tool == "web_search":
# try to extract query
q = user_msg
for kw in ["search", "find", "lookup"]:
if kw in q.lower():
q = q.lower().split(kw, 1)[-1].strip()
break
res = tool_web_search(q or user_msg)
yield f"data: [tool:web_search] {res['output']}\n\n"
prompt = [
{"role": "system", "content": "You are Astra, a helpful assistant that uses search results to answer."},
{"role": "user", "content": f"User asked: {user_msg}\nSearch result: {res['output']}\nPlease give a concise answer based on the search."}
]
llm_resp = await call_openai_chat(prompt)
for i in range(0, len(llm_resp), 120):
yield f"data: {llm_resp[i:i+120]}\n\n"
return


# Default: Ask LLM directly
prompt = [
{"role": "system", "content": "You are Astra: helpful, friendly, concise. If you are unsure, say you don't know and suggest how to find out."},
{"role": "user", "content": user_msg}
]
llm_resp = await call_openai_chat(prompt)
for i in range(0, len(llm_resp), 120):
await asyncio.sleep(0.01)
yield f"data: {llm_resp[i:i+120]}\n\n"