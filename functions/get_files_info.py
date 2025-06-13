import os

def get_files_info(working_directory, directory=None):
  try:
    cwd = os.path.abspath(working_directory)
    work_dir = cwd

    if directory:
      work_dir = os.path.abspath(os.path.join(cwd, directory))

    if not work_dir.startswith(cwd):
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(work_dir):
      return f'Error: "{directory}" is not a directory'

    file_list = []
    dir_contents = os.listdir(work_dir)
    for file_name in dir_contents:
      file_path = os.path.join(work_dir, file_name)
      file_size = os.path.getsize(file_path)
      is_dir = os.path.isdir(file_path)

      file_list.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(file_list)
  except Exception as e:
        print(f"Error getting directory info: {e}")