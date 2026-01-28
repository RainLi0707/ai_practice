import io
import sys
import pandas as pd
import matplotlib.pyplot as plt

class PythonSandboxService:
    """
    Executes Python code locally.
    WARNING: INSECURE. For demo purposes only.
    """
    def execute(self, code: str):
        print(f"[Sandbox] Executing code:\n{code}")
        
        # Capture stdout
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        
        try:
            # We provide a safe-ish globals dictionary
            safe_globals = {
                "pd": pd,
                "plt": plt,
                "print": print
            }
            exec(code, safe_globals)
            output = redirected_output.getvalue()
            return f"Execution Success.\nOutput:\n{output}"
        except Exception as e:
            return f"Execution Logic Error: {e}"
        finally:
            sys.stdout = old_stdout
