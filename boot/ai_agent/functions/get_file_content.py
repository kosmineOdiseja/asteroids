from pathlib import Path

from config import MAX_CHARS


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": (
            "Reads and returns the contents of a specified file "
            "relative to the working directory"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the file to read, relative to "
                        "the working directory"
                    ),
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = Path(working_directory).resolve()
        abs_file_path = (abs_working_dir / file_path).resolve()

        if not abs_file_path.is_relative_to(abs_working_dir):
            return (
                f'Error: Cannot read "{file_path}" '
                "as it is outside the permitted working directory"
            )

        if not abs_file_path.is_file():
            return (
                f'Error: File not found or is not a regular file: '
                f'"{file_path}"'
            )

        with abs_file_path.open("r", encoding="utf-8") as file:
            content = file.read(MAX_CHARS)

            if file.read(1):
                content += (
                    f'[...File "{file_path}" '
                    f'truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        return f"Error: {e}"