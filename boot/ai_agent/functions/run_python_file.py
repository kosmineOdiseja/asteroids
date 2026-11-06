import os
import subprocess
import sys
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": (
            "Executes a Python file relative to the working directory "
            "with optional arguments and returns its output"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the Python file to execute, "
                        "relative to the working directory"
                    ),
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Optional command-line arguments "
                        "to pass to the Python file"
                    ),
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None,
) -> str:
    try:
        working_dir_abs = os.path.realpath(
            os.path.abspath(working_directory)
        )

        absolute_file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )
        absolute_file_path = os.path.realpath(absolute_file_path)

        if (
            os.path.commonpath([working_dir_abs, absolute_file_path])
            != working_dir_abs
        ):
            return (
                f'Error: Cannot execute "{file_path}" '
                "as it is outside the permitted working directory"
            )

        if not os.path.isfile(absolute_file_path):
            return (
                f'Error: "{file_path}" does not exist '
                "or is not a regular file"
            )

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = [sys.executable, absolute_file_path]

        if args:
            command.extend(args)

        process = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []

        if process.returncode != 0:
            output.append(
                f"Process exited with code {process.returncode}"
            )

        if not process.stdout and not process.stderr:
            output.append("No output produced")
        else:
            if process.stdout:
                output.append(f"STDOUT:\n{process.stdout}")

            if process.stderr:
                output.append(f"STDERR:\n{process.stderr}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"