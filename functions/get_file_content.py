import os
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
         file_contents += f'[...File "{file_path}" truncated at 10000 characters]'

      return file_contents

  except Exception as e:
        print(f"Error reading file: {e}")
