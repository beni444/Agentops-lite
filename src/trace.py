import json

class TraceLogger:
    def __init__(self):
        self.trace = {
            "steps": []
        }

    def log_tool_call(self, name, args, result):
        self.trace["steps"].append({
            "tool": name,
            "args": args,
            "result": result
        })

    def export(self):
        return json.dumps(self.trace, indent=2)
