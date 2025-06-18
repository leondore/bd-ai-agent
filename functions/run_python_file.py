import os, subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    cwd = os.path.abspath(working_directory)
    work_path = os.path.abspath(os.path.join(cwd, file_path))

    if not work_path.startswith(cwd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(work_path):
        return f'Error: File "{file_path}" not found.'

    if not work_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = ["python3", work_path]
        if args:
            command = command.extend(args)

        result = subprocess.run(
            command, capture_output=True, text=True, cwd=cwd, timeout=30
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"nSTDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
