import os
import ast
from pathlib import Path

def get_signatures(file_path):
    """Extract class and function signatures from a Python file using AST."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        signatures = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                signatures.append(f"  fn {node.name}({', '.join(args)})")
            elif isinstance(node, ast.ClassDef):
                signatures.append(f"  class {node.name}")
                for subnode in node.body:
                    if isinstance(subnode, ast.FunctionDef):
                        args = [arg.arg for arg in subnode.args.args]
                        signatures.append(f"    method {subnode.name}({', '.join(args)})")
        return signatures
    except Exception as e:
        return [f"  Error parsing {file_path.name}: {e}"]

def generate_repo_map(root_dir, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = {".git", "__pycache__", "node_modules", ".venv", "env", ".opencode"}
    
    repo_map = []
    root_path = Path(root_dir)
    
    for path in sorted(root_path.rglob("*.py")):
        # Check if any parent directory is in exclude_dirs
        if any(part in exclude_dirs for part in path.parts):
            continue
            
        rel_path = path.relative_to(root_path)
        repo_map.append(f"FILE: {rel_path}")
        signatures = get_signatures(path)
        repo_map.extend(signatures)
        repo_map.append("") # Spacer
        
    return "\n".join(repo_map)

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else "repo_map.txt"
    
    print(f"Generating repo map for {target}...")
    content = generate_repo_map(target)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Repo map saved to {output_file}")
