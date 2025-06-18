import os
from google.genai import types


def write_file(working_directory, file_path, content):
    cwd = os.path.abspath(working_directory)
    work_path = os.path.abspath(os.path.join(cwd, file_path))

    if not work_path.startswith(cwd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(work_path):
        try:
            os.makedirs(os.path.dirname(work_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    if os.path.exists(work_path) and os.path.isdir(work_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(work_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: writing to file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
