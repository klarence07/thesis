lessons = [
    {
        "title": "Hello World",
        "instruction": "Write a program that prints 'Hello, world!'",
        "check": lambda output: output.strip() == "Hello, world!",
    },
    {
        "title": "Print Your Name",
        "instruction": "Write a program that prints your name.",
        "check": lambda output: "Alice" in output,  # Replace with your name!
    },
    {
        "title": "Sum Two Numbers",
        "instruction": "Write a program that prints the sum of 2 + 3.",
        "check": lambda output: output.strip() == "5",
    },
]
