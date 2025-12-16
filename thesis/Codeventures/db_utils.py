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

    # Create questions table with difficulty
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            key TEXT PRIMARY KEY,
            question TEXT,
            answer TEXT,
            hint TEXT,
            difficulty TEXT
        )
    ''')

    # Create leaderboard table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY,
            name TEXT,
            score INTEGER,
            time_taken INTEGER,
            difficulty TEXT
        )
    ''')

    # Check if table is empty
    cursor.execute('SELECT count(*) FROM questions')
    if cursor.fetchone()[0] == 0:
        populate_questions(cursor)
        print("Database initialized with default questions.")

    # Populate leaderboard with sample data if empty
    cursor.execute('SELECT count(*) FROM leaderboard')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO leaderboard (name, score, time_taken, difficulty) VALUES (?, ?, ?, ?)", ("Alice", 100, 60, "Medium"))
        cursor.execute("INSERT INTO leaderboard (name, score, time_taken, difficulty) VALUES (?, ?, ?, ?)", ("Bob", 80, 75, "Easy"))
        cursor.execute("INSERT INTO leaderboard (name, score, time_taken, difficulty) VALUES (?, ?, ?, ?)", ("Charlie", 120, 90, "Hard"))
        print("Database initialized with sample leaderboard data.")

    conn.commit()
    conn.close()

def populate_questions(cursor):
    # (Question, Answer, Hint, Difficulty)
    # Difficulty: 'Easy', 'Medium', 'Hard'
    questions_data = {
          # --- Fundamentals: Control Flow ---
            "Control Flow": ("What keyword starts a conditional block?", "if", "Starts with 'i'", "Easy"),
            "elif": ("What keyword is used for an alternative condition?", "elif", "A shortened version of 'else if'.", "Medium"),
            "else_cf": ("What keyword executes when no conditions are met?", "else", "A four-letter word.", "Easy"),
            "break": ("What keyword exits a loop prematurely?", "break", "A word that means to stop.", "Medium"),
            "continue": ("What statement skips the rest of the current loop iteration?", "continue", "A word that means to move on.", "Hard"),
            "return_cf": ("What keyword exits a function and passes control back to the caller?", "return", "Starts with 'r'", "Medium"),

            # --- Fundamentals: Loops ---
            "Loops": ("What keyword starts a loop over items?", "for", "Starts with 'f'", "Easy"),
            "while": ("What keyword creates a loop that runs until a condition is false?", "while", "A five-letter word for duration.", "Easy"),
            "range": ("Which function generates a sequence of numbers for a loop?", "range", "A five-letter function.", "Medium"),
            "membership": ("What does the 'in' keyword check for in a loop header?", "membership", "A ten-letter concept.", "Hard"),
            "else_loop": ("What can be optionally attached to a loop to execute only if the loop finishes normally (without break)?", "else", "Same as the conditional fallback.", "Hard"),
            "indexed_loop": ("What type of iteration is it when a loop iterates through a list index-by-index?", "indexed", "An eight-letter word.", "Hard"),

            # --- Fundamentals: Functions ---
            "Functions": ("How do you define a function in Python?", "def", "Starts with 'd'", "Easy"),
            "local": ("What is a variable declared inside a function known as?", "local", "A five-letter word.", "Medium"),
            "global": ("What keyword is used to access a variable outside the current scope?", "global", "Starts with 'g'", "Medium"),
            "arguments": ("What is the term for the values passed to a function call?", "arguments", "A nine-letter plural noun.", "Medium"),
            "parameters": ("What is the term for the names defined in the function signature?", "parameters", "Starts with 'p'", "Medium"),
            "none": ("What value does a function return if no explicit return statement is used?", "none", "A type in Python.", "Hard"),

            # --- Fundamentals: Lists ---
            "Lists": ("Which method adds an item to a list?", "append", "Starts with 'a'", "Easy"),
            "pop": ("Which method removes an item at a specific index?", "pop", "A three-letter method.", "Medium"),
            "sort": ("Which method is used to sort the list in place?", "sort", "A four-letter word.", "Medium"),
            "len": ("What function returns the number of items in a list?", "len", "A three-letter function.", "Easy"),
            "zero": ("What is the starting index for all Python lists?", "zero", "A four-letter number.", "Easy"),
            "square_list": ("What type of brackets are used to define a list?", "square", "A six-letter shape.", "Easy"),

            # --- Fundamentals: Dictionaries ---
            "Dictionaries": ("What symbol separates keys and values?", ":", "It's a colon", "Easy"),
            "keys": ("What method returns a list of all keys in a dictionary?", "keys", "A four-letter plural noun.", "Medium"),
            "get": ("What method safely retrieves a value using a default if the key is missing?", "get", "A three-letter method.", "Medium"),
            "immutable": ("What must all keys in a dictionary be?", "immutable", "Starts with 'i'", "Hard"),
            "hash": ("What is a dictionary that uses a number as its key indexed by?", "hash", "A four-letter concept.", "Hard"),
            "curly": ("What type of brackets are used to define a dictionary?", "curly", "A five-letter word.", "Easy"),

            # --- Fundamentals: Sets ---
            "Sets": ("Which Python type is unordered and unique?", "set", "Starts with 's'", "Easy"),
            "intersection": ("Which set operation finds all elements in both sets?", "intersection", "A twelve-letter word.", "Medium"),
            "union": ("Which set operation finds all elements in either set?", "union", "A five-letter operation.", "Medium"),
            "remove": ("What method is used to remove an element, raising an error if it's not present?", "remove", "A six-letter method.", "Medium"),
            "discard": ("What method removes an element without raising an error if it's not present?", "discard", "An eight-letter method.", "Hard"),
            "issubset": ("What keyword checks for a subset relationship?", "issubset", "A ten-letter method.", "Hard"),

            # --- Fundamentals: Classes ---
            "Classes": ("What keyword defines a class?", "class", "Starts with 'c'", "Easy"),
            "self": ("What is the standard name for the first parameter of an instance method?", "self", "A four-letter keyword.", "Medium"),
            "blueprint": ("What is the blueprint for creating objects called?", "class", "Same as the definition keyword.", "Easy"),
            "method": ("What is a function defined inside a class called?", "method", "A six-letter noun.", "Easy"),
            "static": ("What is a variable associated with the class itself, not the instance?", "static", "A six-letter adjective.", "Hard"),
            "instance": ("What is a variable associated with a specific instance of the class called?", "instance", "An eight-letter word.", "Hard"),

            # --- Algorithms: Bubble Sort ---
            "Bubble Sort": ("What sorting algorithm repeatedly swaps adjacent elements if they are in the wrong order?", "bubble sort", "Starts with 'b'", "Easy"),
            "o(n^2)": ("What is the worst-case time complexity of this algorithm (using Big O notation)?", "o(n^2)", "Contains an exponent.", "Hard"),
            "inefficiency": ("What is the main drawback of using this sorting method?", "inefficiency", "A thirteen-letter word.", "Medium"),
            "sorted_pass": ("What state is achieved after the first pass of the algorithm?", "sorted", "The largest element is now in the correct position.", "Hard"),
            "o(n)": ("What is the best-case time complexity for a list that is already sorted?", "o(n)", "Linear time.", "Hard"),
            "flag": ("What technique can be added to detect if the list is already sorted and stop early?", "flag", "A four-letter status variable.", "Hard"),

            # --- Algorithms: Binary Search ---
            "Binary Search": ("What search algorithm works only on sorted arrays by repeatedly dividing the search interval in half?", "binary search", "Starts with 'b'", "Easy"),
            "o(log n)": ("What is the time complexity of this algorithm?", "o(log n)", "The fastest Big O for searching.", "Hard"),
            "middle": ("What is the first index checked during the algorithm's iteration?", "middle", "A six-letter word.", "Medium"),
            "required_sorted": ("What is the required condition for the input array?", "sorted", "A six-letter adjective.", "Medium"),
            "array": ("What type of data structure is typically searched using this method?", "array", "A five-letter data type.", "Easy"),
            "low high": ("What two values define the search range during an iteration?", "low high", "Two three-letter words.", "Hard"),

            # --- Algorithms: Factorial ---
            "Factorial": ("What algorithm calculates the product of all integers from 1 up to a given integer?", "factorial", "Starts with 'f'", "Easy"),
            "24": ("What is the factorial of the number 4?", "24", "A two-digit number.", "Medium"),
            "recursive_fact": ("What type of function is often used to implement this calculation (when it calls itself)?", "recursive", "A nine-letter adjective.", "Medium"),
            "1": ("What is the base case for the calculation (the factorial of 0)?", "1", "A single digit number.", "Medium"),
            "multiplication": ("What mathematical operation is central to calculating the next step?", "multiplication", "A fourteen-letter word.", "Easy"),
            "product": ("What is the term for calculating the product of a sequence of integers?", "product", "A seven-letter word.", "Easy"),

            # --- Algorithms: Fibonacci ---
            "Fibonacci": ("What is the sequence where each number is the sum of the two preceding ones?", "fibonacci", "Starts with 'f'", "Easy"),
            "13": ("What is the 7th number in the sequence (starting 0, 1, 1, 2, 3, 5, 8...)?", "13", "A two-digit number.", "Medium"),
            "o(2^n)": ("What is the time complexity of the naive recursive implementation?", "o(2^n)", "Exponential complexity.", "Hard"),
            "memoization": ("What technique can improve the performance of the recursive version?", "memoization", "A twelve-letter word.", "Hard"),
            "base cases": ("What is the name of the two starting numbers in the sequence (0 and 1)?", "base cases", "Two four-letter words.", "Medium"),
            "binst formula": ("What is the formula that relates the sequence to the golden ratio?", "binst formula", "A twelve-letter proper noun.", "Hard"),

            # --- Algorithms: Palindrome ---
            "Palindrome": ("What is a word or phrase that reads the same backward as forward?", "palindrome", "Starts with 'p'", "Easy"),
            "normalize": ("What must be done to a string (like removing spaces) before checking if it is a true palindrome?", "normalize", "A nine-letter verb.", "Medium"),
            "yes": ("What is the answer for the number 121?", "yes", "A three-letter confirmation.", "Easy"),
            "slice": ("What Python trick can quickly reverse a string to check it?", "slice", "A five-letter operation.", "Medium"),
            "equality": ("What property must the reversed version of the string have?", "equality", "An eight-letter concept.", "Medium"),
            "same": ("What is the reverse of a single character?", "same", "A four-letter word.", "Easy"),

            # --- Fill-in: List Comp. ---
            "List Comp.": ("Fill in the blank: [i ___ range(10)] to create a list from 0 to 9.", "for i in", "The word 'in' is one of the blanks.", "Medium"),
            "square_lc": ("What type of brackets are used to define a list comprehension?", "square", "A six-letter shape.", "Easy"),
            "if": ("What optional keyword can filter items within a comprehension?", "if", "A two-letter keyword.", "Medium"),
            "efficient": ("List comprehensions are generally more _ than traditional loops.", "efficient", "A nine-letter adjective.", "Medium"),
            "expression": ("What is the part of the comprehension before the for keyword?", "expression", "A ten-letter word.", "Hard"),
            "list": ("The result of a list comprehension is always what data type?", "list", "A four-letter data type.", "Easy"),

            # --- Fill-in: String Slice ---
            "String Slice": ("Fill in the blank: my_str[2:] will return the string starting from the _ index.", "second", "An ordinal number.", "Medium"),
            "fifth": ("Fill in the blank: my_str[:5] returns the string up to the _ index (but not including it).", "fifth", "An ordinal number.", "Medium"),
            "step": ("What is the third, optional component of a slice (e.g., [::2])?", "step", "A four-letter word.", "Hard"),
            "end": ("What does a negative index (e.g., [-1]) access?", "end", "The opposite of the start.", "Medium"),
            "reverse": ("What is the result of my_str[::-1]?", "reverse", "A seven-letter action.", "Medium"),
            "slice_char": ("What character is used to separate the slice indices?", ":", "Same as the dictionary separator.", "Easy"),

            # --- Fill-in: Func Return ---
            "Func Return": ("Fill in the blank: def add(a): ___ a + 1 to complete the function.", "return", "A keyword to send a value back.", "Easy"),
            "return value": ("What is the data sent back from a function called?", "return value", "Two words.", "Easy"),
            "return_kw": ("What keyword can be used to exit a function without returning a value (it returns None)?", "return", "The same keyword.", "Medium"),
            "multiple": ("A function can return how many values?", "multiple", "An eight-letter adjective.", "Medium"),
            "pure": ("A function that computes and gives back a result is called what?", "pure", "A four-letter adjective.", "Hard"),
            "calling": ("What is the process of getting the value from the function called?", "calling", "A seven-letter verb.", "Medium"),

            # --- Fill-in: Class Init ---
            "Class Init": ("What method is automatically called when a new instance of a class is created? __ _ __", "init", "A special double-underscore method.", "Medium"),
            "del": ("What is the name of the method that cleans up when an object is destroyed? __ ___ __", "del", "A three-letter double-underscore method.", "Hard"),
            "class_init": ("What keyword is used to create a new object instance?", "class", "The name of the blueprint.", "Easy"),
            "constructor": ("What is the entire initialization method officially called?", "constructor", "An eleven-letter word.", "Medium"),
            "self_ci": ("What is the first argument of the _init_ method usually named?", "self", "A four-letter word.", "Medium"),
            "instance_ci": ("What is the term for the object that is created from the class blueprint?", "instance", "An eight-letter word.", "Medium"),

            # --- Fill-in: Try-Except ---
            "Try-Except": ("Fill in the blank: try: x = 1 / 0 ___ ZeroDivisionError: print(\"Error\")", "except", "A keyword to catch the error.", "Medium"),
            "finally": ("What keyword executes code after the try block, regardless of errors?", "finally", "An eight-letter keyword.", "Medium"),
            "else_te": ("What keyword executes code only if the try block succeeds (no errors)?", "else", "Same as the conditional fallback.", "Hard"),
            "raise": ("What is the general keyword used to raise a user-defined error?", "raise", "A five-letter verb.", "Medium"),
            "exception": ("What is the term for a detected error during execution?", "exception", "A ten-letter word.", "Easy"),
            "try": ("Which block is where you place the code that might cause an error?", "try", "A three-letter keyword.", "Easy"),

            # --- Fill-in: File Open ---
            "File Open": ("Fill in the blank: ___('file.txt', 'r') as f: to open a file.", "open", "A common built-in function.", "Easy"),
            "w": ("What character is the mode for writing (overwriting) to a file?", "w", "A single lowercase letter.", "Medium"),
            "r": ("What character is the mode for reading a file?", "r", "A single lowercase letter.", "Medium"),
            "a": ("What character is the mode for appending to a file?", "a", "A single lowercase letter.", "Medium"),
            "os": ("What is the name of the standard module for interacting with the operating system?", "os", "Two lowercase letters.", "Medium"),
            "with": ("What keyword is often used to ensure a file is closed after use?", "with", "A four-letter keyword.", "Hard"),

            # --- Fill-in: Dict Index ---
            "Dict Index": ("Fill in the blank: Dictionaries are indexed by what?", "keys", "The name for the left side of the pair.", "Easy"),
            "items": ("What method returns a view object that displays a list of a dictionary's key-value tuple pairs?", "items", "A five-letter method.", "Medium"),
            "keyerror": ("What is the error raised when you try to access a non-existent key?", "keyerror", "An eight-letter error type.", "Medium"),
            "ordered": ("Dictionaries are always what (since Python 3.7)?", "ordered", "A seven-letter adjective.", "Hard"),
            "in": ("How do you check for the existence of a key in a dictionary?", "in", "A two-letter keyword.", "Easy"),
            "item": ("What is another name for a key-value pair?", "item", "A four-letter word.", "Easy"),

            # --- Fill-in: Set Add ---
            "Set Add": ("Which method adds a single item to a set?", "add", "A three-letter method name.", "Easy"),
            "update": ("What method is used to add multiple iterable items to a set?", "update", "A six-letter method.", "Medium"),
            "hashable": ("The elements of a set must be what?", "hashable", "An eight-letter property.", "Hard"),
            "set_empty": ("How do you create an empty set (it's not {})?", "set", "A three-letter function.", "Medium"),
            "pop_set": ("What keyword is used to remove an arbitrary element from a set?", "pop", "A three-letter method.", "Medium"),
            "set_fn": ("What is the built-in function used to create a set from a list?", "set", "A three-letter function.", "Easy"),

            # --- Fill-in: Lambda ---
            "Lambda": ("What is the keyword for an anonymous one-line function?", "lambda", "Starts with 'l'", "Medium"),
            "lambda_kw": ("What keyword does a lambda function implicitly contain instead of return?", "lambda", "It's the same keyword.", "Medium"),
            "expression_l": ("A lambda function can only contain a single what?", "expression", "A ten-letter word.", "Hard"),
            "higher order": ("What are these functions most commonly used with (e.g., map and filter)?", "higher order", "Two words.", "Hard"),
            "higher order_l": ("What type of function takes one or more functions as arguments?", "higher order", "Same as the common usage.", "Hard"),
            "anonymous": ("What is a short, disposable function called?", "anonymous", "A nine-letter adjective.", "Medium"),

            # --- Fill-in: Tuple Brackets ---
            "Tuple Brackets": ("Fill in the blank: Tuples use what type of brackets?", "parentheses", "Curved symbols.", "Easy"),
            "immutable_t": ("What is the defining characteristic of a tuple?", "immutable", "An nine-letter property.", "Easy"),
            "count": ("What method counts the number of times a value appears in a tuple?", "count", "A five-letter method.", "Medium"),
            "one": ("What is the smallest size a tuple can be (e.g., (1,))?", "one", "A three-letter number.", "Hard"),
            "unpacking": ("What is the process of extracting values from a tuple into separate variables called?", "unpacking", "A ten-letter word.", "Medium"),
            "comma": ("What must a one-element tuple end with to be recognized as a tuple?", "comma", "A five-letter punctuation.", "Hard"),

            # Fallback for topics not explicitly listed in the groups above:
            "Tuples": ("What is the defining characteristic of a tuple?", "immutable", "It starts with 'i'.", "Easy"),
            "Modules": ("What keyword is used to bring an external module into your script?", "import", "It starts with 'i'.", "Easy"),
            "JSON": ("What format is commonly used to send data from a server to a web page?", "json", "An acronym.", "Medium"),
            "Recursion": ("What is a function that calls itself called?", "recursion", "It starts with 'r'.", "Easy"),
            "Inheritance": ("What is the mechanism where one class acquires the properties of another?", "inheritance", "It starts with 'i'.", "Medium"),
            "Polymorphism": ("What is the ability of an object to take on many forms?", "polymorphism", "It starts with 'p'.", "Hard"),
            "Abstraction": ("What is the process of hiding the complex reality while exposing only the necessary parts?", "abstraction", "It starts with 'a'.", "Hard"),
            "Encapsulation": ("What is the concept of bundling data and the methods that operate on that data?", "encapsulation", "It starts with 'e'.", "Hard"),
    }

    for key, (question, answer, hint, difficulty) in questions_data.items():
        cursor.execute('INSERT INTO questions (key, question, answer, hint, difficulty) VALUES (?, ?, ?, ?, ?)', (key, question, answer, hint, difficulty))

def fetch_question(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row['question'], row['answer'], row['hint'], row['difficulty']
    return None

def fetch_all_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    rows = cursor.fetchall()
    conn.close()
    questions = {}
    for row in rows:
        questions[row['key']] = (row['question'], row['answer'], row['hint'], row['difficulty'])
    return questions

def filter_keys_by_difficulty(keys_list, chosen_difficulty):
    """
    Given a list of keys and a chosen difficulty ('Easy', 'Medium', 'Hard'),
    return a list of keys that match the difficulty criteria.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # We want to select keys from the DB that are in the keys_list AND match the difficulty logic

    # Logic:
    # Easy Mode -> Easy questions only
    # Medium Mode -> Easy and Medium questions
    # Hard Mode -> Easy, Medium, and Hard (All questions)

    allowed_difficulties = []
    if chosen_difficulty == "Easy":
        allowed_difficulties = ["Easy"]
    elif chosen_difficulty == "Medium":
        allowed_difficulties = ["Easy", "Medium"]
    else: # Hard
        allowed_difficulties = ["Easy", "Medium", "Hard"]

    placeholders = ','.join('?' for _ in keys_list)
    diff_placeholders = ','.join('?' for _ in allowed_difficulties)

    query = f'''
        SELECT key FROM questions
        WHERE key IN ({placeholders})
        AND difficulty IN ({diff_placeholders})
    '''

    params = keys_list + allowed_difficulties
    cursor.execute(query, params)

    rows = cursor.fetchall()
    conn.close()

    filtered_keys = [row['key'] for row in rows]

    # If the filtered list is empty (e.g. strict filtering left no options),
    # fallback to returning the original list to avoid soft-lock.
    if not filtered_keys:
        return keys_list

    return filtered_keys

def insert_score(name, score, time_taken, difficulty):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (name, score, time_taken, difficulty) VALUES (?, ?, ?, ?)", (name, score, time_taken, difficulty))
    conn.commit()
    conn.close()

def fetch_leaderboard(difficulty=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if difficulty:
        cursor.execute("SELECT * FROM leaderboard WHERE difficulty = ? ORDER BY score DESC, time_taken ASC LIMIT 50", (difficulty,))
    else:
        cursor.execute("SELECT * FROM leaderboard ORDER BY score DESC, time_taken ASC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    return rows
