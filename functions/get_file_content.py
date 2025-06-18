import os
from google.genai import types

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        cwd = os.path.abspath(working_directory)
        work_path = os.path.abspath(os.path.join(cwd, file_path))

        if not work_path.startswith(cwd):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(work_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(work_path, "r") as file:
            file_contents = file.read(MAX_CHARS)

            if len(file_contents) >= MAX_CHARS:
                file_contents += (
                    f'[...File "{file_path}" truncated at 10000 characters]'
                )

            return file_contents

    except Exception as e:
        return f"Error reading file: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            )
        },
        required=["file_path"],
    ),
)
