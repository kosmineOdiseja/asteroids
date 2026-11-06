from functions.get_file_content import get_file_content


if __name__ == "__main__":
    result = get_file_content("calculator", "lorem.txt")

    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print()

    test_cases = [
        "main.py",
        "pkg/calculator.py",
        "/bin/cat",
        "pkg/does_not_exist.py",
    ]

    for file_path in test_cases:
        print(f"Result for '{file_path}':")
        print(get_file_content("calculator", file_path))
        print()