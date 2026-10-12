import sys
import io
import time
import ast
import traceback
from typing import Dict, Any, List, Optional, Tuple, Set

class DSARunner:
    @staticmethod
    def analyze_code_ast(user_code: str) -> List[str]:
        """Static AST analysis to generate algorithmic quality hints."""
        hints = []
        try:
            tree = ast.parse(user_code)
            has_for_loop = False
            has_while_loop = False
            has_recursion = False
            func_names = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_names.add(node.name)
                elif isinstance(node, ast.For):
                    has_for_loop = True
                elif isinstance(node, ast.While):
                    has_while_loop = True
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in func_names:
                        has_recursion = True

            if has_recursion:
                hints.append("Recursion detected: Ensure base cases are explicitly defined to avoid RecursionError.")
            if has_while_loop:
                hints.append("While loop detected: Double-check pointer/index increment logic to avoid infinite loops.")
            if not (has_for_loop or has_while_loop or has_recursion):
                hints.append("Direct return / O(1) logic detected.")
        except SyntaxError as se:
            hints.append(f"Syntax Note: {se.msg} at line {se.lineno}")
        return hints

    @staticmethod
    def execute_solution(user_code: str, entry_class: str, entry_method: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Capture stdout
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        results = []
        all_passed = True
        error_msg = None
        start_time = time.perf_counter()

        # Run static AST quality check
        ast_hints = DSARunner.analyze_code_ast(user_code)

        try:
            # Prepare execution environment with typing builtins
            global_scope = {
                "__builtins__": __builtins__,
                "List": List,
                "Dict": Dict,
                "Optional": Optional,
                "Tuple": Tuple,
                "Set": Set,
                "list": list,
                "dict": dict
            }
            local_scope = {}

            # Execute user code definition
            exec(user_code, global_scope, local_scope)

            # Look for class in local_scope or global_scope
            target_class = local_scope.get(entry_class) or global_scope.get(entry_class)
            if not target_class:
                raise NameError(f"Class '{entry_class}' not found in code submission. Expected class '{entry_class}'.")

            solution_obj = target_class()
            method_to_call = getattr(solution_obj, entry_method, None)

            if not method_to_call:
                raise AttributeError(f"Method '{entry_method}' not found on class '{entry_class}'.")

            # Run test cases with execution timing
            for idx, tc in enumerate(test_cases, 1):
                kwargs = tc.get("args", {})
                expected = tc.get("expected")

                tc_start = time.perf_counter()
                try:
                    actual = method_to_call(**kwargs)
                    tc_duration = round((time.perf_counter() - tc_start) * 1000, 3) # ms

                    passed = (actual == expected)
                    if not passed:
                        all_passed = False

                    results.append({
                        "test_case": idx,
                        "input": kwargs,
                        "expected": expected,
                        "actual": actual,
                        "execution_time_ms": tc_duration,
                        "passed": passed
                    })
                except Exception as ex:
                    all_passed = False
                    tc_duration = round((time.perf_counter() - tc_start) * 1000, 3)
                    results.append({
                        "test_case": idx,
                        "input": kwargs,
                        "expected": expected,
                        "actual": f"Runtime Error: {type(ex).__name__}: {str(ex)}",
                        "execution_time_ms": tc_duration,
                        "passed": False
                    })
        except Exception as e:
            all_passed = False
            error_msg = f"{type(e).__name__}: {str(e)}"
        finally:
            sys.stdout = old_stdout

        total_duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        stdout_content = redirected_output.getvalue()

        return {
            "success": all_passed,
            "total_cases": len(test_cases),
            "passed_cases": sum(1 for r in results if r.get("passed", False)),
            "total_execution_time_ms": total_duration_ms,
            "results": results,
            "ast_hints": ast_hints,
            "stdout": stdout_content,
            "error": error_msg
        }

dsa_runner = DSARunner()
