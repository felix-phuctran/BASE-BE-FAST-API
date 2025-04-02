import csv
import json
import os


def write_file(file_path, content, extension, mode="w"):
    """
    Writes content to a file based on the specified file extension.

    Args:
        file_path (str): The path to the file where content will be written.
        content (str | dict | list): The content to write. For JSON, provide a dict; for CSV, provide a list of rows.
        extension (str): The file extension ("txt", "json", or "csv").
        mode (str): The mode in which the file should be opened (default is "w" for write).

    Returns:
        None

    Example:
        >>> write_file("example.txt", "Hello, world!", "txt")
        >>> write_file("example.json", {"key": "value"}, "json")
        >>> write_file("example.csv", [["Name", "Age"], ["Alice", 30]], "csv")

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    try:
        if extension == "txt":
            with open(file_path, mode, encoding="utf-8") as file:
                file.write(content)
        elif extension == "json":
            with open(file_path, mode, encoding="utf-8") as file:
                json.dump(content, file, ensure_ascii=False, indent=4)
        elif extension == "csv":
            with open(file_path, mode, newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                if isinstance(content, list):
                    writer.writerows(content)
                else:
                    raise ValueError("CSV content must be a list of rows")
        else:
            raise ValueError(f"Unsupported file extension: {extension}")
    except Exception as e:
        print(f"Error writing file: {e}")

def read_file(file_path, extension):
    """
    Reads content from a file based on the specified file extension.

    Args:
        file_path (str): The path to the file to read.
        extension (str): The file extension ("txt", "json", or "csv").

    Returns:
        str | dict | list | None: The content of the file. Returns None if an error occurs.

    Example:
        >>> read_file("example.txt", "txt")
        'Hello, world!'
        >>> read_file("example.json", "json")
        {"key": "value"}
        >>> read_file("example.csv", "csv")
        [["Name", "Age"], ["Alice", "30"]]

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    try:
        match extension:
            case "txt":
                with open(file_path, "r", encoding="utf-8") as file:
                    return file.read()
            case "json":
                with open(file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            case "csv":
                with open(file_path, "r", newline='', encoding="utf-8") as file:
                    reader = csv.reader(file)
                    return [row for row in reader]
            case _:
                raise ValueError(f"Unsupported file extension: {extension}")
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, "example")
    os.makedirs(data_dir, exist_ok=True)

    txt_path = os.path.join(data_dir, "example.txt")
    json_path = os.path.join(data_dir, "example.json")
    csv_path = os.path.join(data_dir, "example.csv")

    # Writing examples
    write_file(txt_path, "Hello, world!", "txt")
    write_file(json_path, {"key": "value"}, "json")
    write_file(csv_path, [["Name", "Age"], ["Alice", 30], ["Bob", 25]], "csv")

    # Reading examples
    print(read_file(txt_path, "txt"))
    print(read_file(json_path, "json"))
    print(read_file(csv_path, "csv"))

