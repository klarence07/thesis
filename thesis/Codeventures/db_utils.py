import sqlite3
import os

DB_NAME = "codeventures.db"

def get_db_connection():
    # Use absolute path relative to this file to avoid path issues
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, DB_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            key TEXT PRIMARY KEY,
            question TEXT,
            answer TEXT,
            hint TEXT
        )
    ''')

    # Check if table is empty
    cursor.execute('SELECT count(*) FROM questions')
    if cursor.fetchone()[0] == 0:
        populate_questions(cursor)
        print("Database initialized with default questions.")

    conn.commit()
    conn.close()

def populate_questions(cursor):
    questions_data = {
          # --- Fundamentals: Control Flow (6 Questions) ---
            "Control Flow": ("What keyword starts a conditional block?", "if", "Starts with 'i'"),
            "elif": ("What keyword is used for an alternative condition?", "elif", "A shortened version of 'else if'."),
            "else_cf": ("What keyword executes when no conditions are met?", "else", "A four-letter word."),
            "break": ("What keyword exits a loop prematurely?", "break", "A word that means to stop."),
            "continue": ("What statement skips the rest of the current loop iteration?", "continue", "A word that means to move on."),
            "return_cf": ("What keyword exits a function and passes control back to the caller?", "return", "Starts with 'r'"),

            # --- Fundamentals: Loops (6 Questions) ---
            "Loops": ("What keyword starts a loop over items?", "for", "Starts with 'f'"),
            "while": ("What keyword creates a loop that runs until a condition is false?", "while", "A five-letter word for duration."),
            "range": ("Which function generates a sequence of numbers for a loop?", "range", "A five-letter function."),
            "membership": ("What does the 'in' keyword check for in a loop header?", "membership", "A ten-letter concept."),
            "else_loop": ("What can be optionally attached to a loop to execute only if the loop finishes normally (without break)?", "else", "Same as the conditional fallback."),
            "indexed_loop": ("What type of iteration is it when a loop iterates through a list index-by-index?", "indexed", "An eight-letter word."),

            # --- Fundamentals: Functions (6 Questions) ---
            "Functions": ("How do you define a function in Python?", "def", "Starts with 'd'"),
            "local": ("What is a variable declared inside a function known as?", "local", "A five-letter word."),
            "global": ("What keyword is used to access a variable outside the current scope?", "global", "Starts with 'g'"),
            "arguments": ("What is the term for the values passed to a function call?", "arguments", "A nine-letter plural noun."),
            "parameters": ("What is the term for the names defined in the function signature?", "parameters", "Starts with 'p'"),
            "none": ("What value does a function return if no explicit return statement is used?", "none", "A type in Python."),

            # --- Fundamentals: Lists (6 Questions) ---
            "Lists": ("Which method adds an item to a list?", "append", "Starts with 'a'"),
            "pop": ("Which method removes an item at a specific index?", "pop", "A three-letter method."),
            "sort": ("Which method is used to sort the list in place?", "sort", "A four-letter word."),
            "len": ("What function returns the number of items in a list?", "len", "A three-letter function."),
            "zero": ("What is the starting index for all Python lists?", "zero", "A four-letter number."),
            "square_list": ("What type of brackets are used to define a list?", "square", "A six-letter shape."),

            # --- Fundamentals: Dictionaries (6 Questions) ---
            "Dictionaries": ("What symbol separates keys and values?", ":", "It's a colon"),
            "keys": ("What method returns a list of all keys in a dictionary?", "keys", "A four-letter plural noun."),
            "get": ("What method safely retrieves a value using a default if the key is missing?", "get", "A three-letter method."),
            "immutable": ("What must all keys in a dictionary be?", "immutable", "Starts with 'i'"),
            "hash": ("What is a dictionary that uses a number as its key indexed by?", "hash", "A four-letter concept."),
            "curly": ("What type of brackets are used to define a dictionary?", "curly", "A five-letter word."),

            # --- Fundamentals: Sets (6 Questions) ---
            "Sets": ("Which Python type is unordered and unique?", "set", "Starts with 's'"),
            "intersection": ("Which set operation finds all elements in both sets?", "intersection", "A twelve-letter word."),
            "union": ("Which set operation finds all elements in either set?", "union", "A five-letter operation."),
            "remove": ("What method is used to remove an element, raising an error if it's not present?", "remove", "A six-letter method."),
            "discard": ("What method removes an element without raising an error if it's not present?", "discard", "An eight-letter method."),
            "issubset": ("What keyword checks for a subset relationship?", "issubset", "A ten-letter method."),

            # --- Fundamentals: Classes (6 Questions) ---
            "Classes": ("What keyword defines a class?", "class", "Starts with 'c'"),
            "self": ("What is the standard name for the first parameter of an instance method?", "self", "A four-letter keyword."),
            "blueprint": ("What is the blueprint for creating objects called?", "class", "Same as the definition keyword."),
            "method": ("What is a function defined inside a class called?", "method", "A six-letter noun."),
            "static": ("What is a variable associated with the class itself, not the instance?", "static", "A six-letter adjective."),
            "instance": ("What is a variable associated with a specific instance of the class called?", "instance", "An eight-letter word."),

            # --- Algorithms: Bubble Sort (6 Questions) ---
            "Bubble Sort": ("What sorting algorithm repeatedly swaps adjacent elements if they are in the wrong order?", "bubble sort", "Starts with 'b'"),
            "o(n^2)": ("What is the worst-case time complexity of this algorithm (using Big O notation)?", "o(n^2)", "Contains an exponent."),
            "inefficiency": ("What is the main drawback of using this sorting method?", "inefficiency", "A thirteen-letter word."),
            "sorted_pass": ("What state is achieved after the first pass of the algorithm?", "sorted", "The largest element is now in the correct position."),
            "o(n)": ("What is the best-case time complexity for a list that is already sorted?", "o(n)", "Linear time."),
            "flag": ("What technique can be added to detect if the list is already sorted and stop early?", "flag", "A four-letter status variable."),

            # --- Algorithms: Binary Search (6 Questions) ---
            "Binary Search": ("What search algorithm works only on sorted arrays by repeatedly dividing the search interval in half?", "binary search", "Starts with 'b'"),
            "o(log n)": ("What is the time complexity of this algorithm?", "o(log n)", "The fastest Big O for searching."),
            "middle": ("What is the first index checked during the algorithm's iteration?", "middle", "A six-letter word."),
            "required_sorted": ("What is the required condition for the input array?", "sorted", "A six-letter adjective."),
            "array": ("What type of data structure is typically searched using this method?", "array", "A five-letter data type."),
            "low high": ("What two values define the search range during an iteration?", "low high", "Two three-letter words."),

            # --- Algorithms: Factorial (6 Questions) ---
            "Factorial": ("What algorithm calculates the product of all integers from 1 up to a given integer?", "factorial", "Starts with 'f'"),
            "24": ("What is the factorial of the number 4?", "24", "A two-digit number."),
            "recursive_fact": ("What type of function is often used to implement this calculation (when it calls itself)?", "recursive", "A nine-letter adjective."),
            "1": ("What is the base case for the calculation (the factorial of 0)?", "1", "A single digit number."),
            "multiplication": ("What mathematical operation is central to calculating the next step?", "multiplication", "A fourteen-letter word."),
            "product": ("What is the term for calculating the product of a sequence of integers?", "product", "A seven-letter word."),

            # --- Algorithms: Fibonacci (6 Questions) ---
            "Fibonacci": ("What is the sequence where each number is the sum of the two preceding ones?", "fibonacci", "Starts with 'f'"),
            "13": ("What is the 7th number in the sequence (starting 0, 1, 1, 2, 3, 5, 8...)?", "13", "A two-digit number."),
            "o(2^n)": ("What is the time complexity of the naive recursive implementation?", "o(2^n)", "Exponential complexity."),
            "memoization": ("What technique can improve the performance of the recursive version?", "memoization", "A twelve-letter word."),
            "base cases": ("What is the name of the two starting numbers in the sequence (0 and 1)?", "base cases", "Two four-letter words."),
            "binst formula": ("What is the formula that relates the sequence to the golden ratio?", "binst formula", "A twelve-letter proper noun."),

            # --- Algorithms: Palindrome (6 Questions) ---
            "Palindrome": ("What is a word or phrase that reads the same backward as forward?", "palindrome", "Starts with 'p'"),
            "normalize": ("What must be done to a string (like removing spaces) before checking if it is a true palindrome?", "normalize", "A nine-letter verb."),
            "yes": ("What is the answer for the number 121?", "yes", "A three-letter confirmation."),
            "slice": ("What Python trick can quickly reverse a string to check it?", "slice", "A five-letter operation."),
            "equality": ("What property must the reversed version of the string have?", "equality", "An eight-letter concept."),
            "same": ("What is the reverse of a single character?", "same", "A four-letter word."),

            # --- Fill-in: List Comp. (6 Questions) ---
            "List Comp.": ("Fill in the blank: [i ___ range(10)] to create a list from 0 to 9.", "for i in", "The word 'in' is one of the blanks."),
            "square_lc": ("What type of brackets are used to define a list comprehension?", "square", "A six-letter shape."),
            "if": ("What optional keyword can filter items within a comprehension?", "if", "A two-letter keyword."),
            "efficient": ("List comprehensions are generally more _ than traditional loops.", "efficient", "A nine-letter adjective."),
            "expression": ("What is the part of the comprehension before the for keyword?", "expression", "A ten-letter word."),
            "list": ("The result of a list comprehension is always what data type?", "list", "A four-letter data type."),

            # --- Fill-in: String Slice (6 Questions) ---
            "String Slice": ("Fill in the blank: my_str[2:] will return the string starting from the _ index.", "second", "An ordinal number."),
            "fifth": ("Fill in the blank: my_str[:5] returns the string up to the _ index (but not including it).", "fifth", "An ordinal number."),
            "step": ("What is the third, optional component of a slice (e.g., [::2])?", "step", "A four-letter word."),
            "end": ("What does a negative index (e.g., [-1]) access?", "end", "The opposite of the start."),
            "reverse": ("What is the result of my_str[::-1]?", "reverse", "A seven-letter action."),
            "slice_char": ("What character is used to separate the slice indices?", ":", "Same as the dictionary separator."),

            # --- Fill-in: Func Return (6 Questions) ---
            "Func Return": ("Fill in the blank: def add(a): ___ a + 1 to complete the function.", "return", "A keyword to send a value back."),
            "return value": ("What is the data sent back from a function called?", "return value", "Two words."),
            "return_kw": ("What keyword can be used to exit a function without returning a value (it returns None)?", "return", "The same keyword."),
            "multiple": ("A function can return how many values?", "multiple", "An eight-letter adjective."),
            "pure": ("A function that computes and gives back a result is called what?", "pure", "A four-letter adjective."),
            "calling": ("What is the process of getting the value from the function called?", "calling", "A seven-letter verb."),

            # --- Fill-in: Class Init (6 Questions) ---
            "Class Init": ("What method is automatically called when a new instance of a class is created? __ _ __", "init", "A special double-underscore method."),
            "del": ("What is the name of the method that cleans up when an object is destroyed? __ ___ __", "del", "A three-letter double-underscore method."),
            "class_init": ("What keyword is used to create a new object instance?", "class", "The name of the blueprint."),
            "constructor": ("What is the entire initialization method officially called?", "constructor", "An eleven-letter word."),
            "self_ci": ("What is the first argument of the _init_ method usually named?", "self", "A four-letter word."),
            "instance_ci": ("What is the term for the object that is created from the class blueprint?", "instance", "An eight-letter word."),

            # --- Fill-in: Try-Except (6 Questions) ---
            "Try-Except": ("Fill in the blank: try: x = 1 / 0 ___ ZeroDivisionError: print(\"Error\")", "except", "A keyword to catch the error."),
            "finally": ("What keyword executes code after the try block, regardless of errors?", "finally", "An eight-letter keyword."),
            "else_te": ("What keyword executes code only if the try block succeeds (no errors)?", "else", "Same as the conditional fallback."),
            "raise": ("What is the general keyword used to raise a user-defined error?", "raise", "A five-letter verb."),
            "exception": ("What is the term for a detected error during execution?", "exception", "A ten-letter word."),
            "try": ("Which block is where you place the code that might cause an error?", "try", "A three-letter keyword."),

            # --- Fill-in: File Open (6 Questions) ---
            "File Open": ("Fill in the blank: ___('file.txt', 'r') as f: to open a file.", "open", "A common built-in function."),
            "w": ("What character is the mode for writing (overwriting) to a file?", "w", "A single lowercase letter."),
            "r": ("What character is the mode for reading a file?", "r", "A single lowercase letter."),
            "a": ("What character is the mode for appending to a file?", "a", "A single lowercase letter."),
            "os": ("What is the name of the standard module for interacting with the operating system?", "os", "Two lowercase letters."),
            "with": ("What keyword is often used to ensure a file is closed after use?", "with", "A four-letter keyword."),

            # --- Fill-in: Dict Index (6 Questions) ---
            "Dict Index": ("Fill in the blank: Dictionaries are indexed by what?", "keys", "The name for the left side of the pair."),
            "items": ("What method returns a view object that displays a list of a dictionary's key-value tuple pairs?", "items", "A five-letter method."),
            "keyerror": ("What is the error raised when you try to access a non-existent key?", "keyerror", "An eight-letter error type."),
            "ordered": ("Dictionaries are always what (since Python 3.7)?", "ordered", "A seven-letter adjective."),
            "in": ("How do you check for the existence of a key in a dictionary?", "in", "A two-letter keyword."),
            "item": ("What is another name for a key-value pair?", "item", "A four-letter word."),

            # --- Fill-in: Set Add (6 Questions) ---
            "Set Add": ("Which method adds a single item to a set?", "add", "A three-letter method name."),
            "update": ("What method is used to add multiple iterable items to a set?", "update", "A six-letter method."),
            "hashable": ("The elements of a set must be what?", "hashable", "An eight-letter property."),
            "set_empty": ("How do you create an empty set (it's not {})?", "set", "A three-letter function."),
            "pop_set": ("What keyword is used to remove an arbitrary element from a set?", "pop", "A three-letter method."),
            "set_fn": ("What is the built-in function used to create a set from a list?", "set", "A three-letter function."),

            # --- Fill-in: Lambda (6 Questions) ---
            "Lambda": ("What is the keyword for an anonymous one-line function?", "lambda", "Starts with 'l'"),
            "lambda_kw": ("What keyword does a lambda function implicitly contain instead of return?", "lambda", "It's the same keyword."),
            "expression_l": ("A lambda function can only contain a single what?", "expression", "A ten-letter word."),
            "higher order": ("What are these functions most commonly used with (e.g., map and filter)?", "higher order", "Two words."),
            "higher order_l": ("What type of function takes one or more functions as arguments?", "higher order", "Same as the common usage."),
            "anonymous": ("What is a short, disposable function called?", "anonymous", "A nine-letter adjective."),

            # --- Fill-in: Tuple Brackets (6 Questions) ---
            "Tuple Brackets": ("Fill in the blank: Tuples use what type of brackets?", "parentheses", "Curved symbols."),
            "immutable_t": ("What is the defining characteristic of a tuple?", "immutable", "An nine-letter property."),
            "count": ("What method counts the number of times a value appears in a tuple?", "count", "A five-letter method."),
            "one": ("What is the smallest size a tuple can be (e.g., (1,))?", "one", "A three-letter number."),
            "unpacking": ("What is the process of extracting values from a tuple into separate variables called?", "unpacking", "A ten-letter word."),
            "comma": ("What must a one-element tuple end with to be recognized as a tuple?", "comma", "A five-letter punctuation."),

            # Fallback for topics not explicitly listed in the groups above:
            "Tuples": ("What is the defining characteristic of a tuple?", "immutable", "It starts with 'i'."),
            "Modules": ("What keyword is used to bring an external module into your script?", "import", "It starts with 'i'."),
            "JSON": ("What format is commonly used to send data from a server to a web page?", "json", "An acronym."),
            "Recursion": ("What is a function that calls itself called?", "recursion", "It starts with 'r'."),
            "Inheritance": ("What is the mechanism where one class acquires the properties of another?", "inheritance", "It starts with 'i'."),
            "Polymorphism": ("What is the ability of an object to take on many forms?", "polymorphism", "It starts with 'p'."),
            "Abstraction": ("What is the process of hiding the complex reality while exposing only the necessary parts?", "abstraction", "It starts with 'a'."),
            "Encapsulation": ("What is the concept of bundling data and the methods that operate on that data?", "encapsulation", "It starts with 'e'."),
    }

    for key, (question, answer, hint) in questions_data.items():
        cursor.execute('INSERT INTO questions (key, question, answer, hint) VALUES (?, ?, ?, ?)', (key, question, answer, hint))

def fetch_question(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row['question'], row['answer'], row['hint']
    return None

def fetch_all_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    rows = cursor.fetchall()
    conn.close()
    questions = {}
    for row in rows:
        questions[row['key']] = (row['question'], row['answer'], row['hint'])
    return questions
