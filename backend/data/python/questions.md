# Python Interview Questions

## Easy

### Q1: What is the difference between mutable and immutable data types in Python? Give examples.
**Answer:** In Python, every variable is a reference to an object in memory. A mutable object is one whose state or content can be modified after creation without changing its identity (`id()`). In contrast, an immutable object cannot be modified once created; any operation that appears to modify it actually creates a new object in memory.
- **Mutable types:** `list`, `dict`, `set`, `bytearray`, and user-defined class instances (unless frozen).
- **Immutable types:** `int`, `float`, `complex`, `str`, `tuple`, `frozenset`, `bytes`, and `bool`.
For example, appending an element to a list modifies the list in-place:
```python
a = [1, 2]
print(id(a))
a.append(3)
print(id(a))  # Same memory address
```
Modifying a string creates a new string object:
```python
s = "hello"
print(id(s))
s += " world"
print(id(s))  # Different memory address
```
A common pitfall with mutability is default function arguments: using mutable default values like `def func(lst=[])` retains modifications across subsequent calls. The idiomatic solution is `def func(lst=None): if lst is None: lst = []`.
**Key Points:**
- Mutable objects allow in-place modification; immutable objects cannot be changed in place.
- Identity (`id()`) stays constant for mutable mutations, but changes when modifying immutable variables.
- Default arguments in function definitions evaluate only once at definition time, making mutable defaults dangerous.
- Tuples are immutable containers, but they can contain mutable elements (e.g., a tuple containing a list).
**Evaluation Criteria:**
- Correctly categorizes common types into mutable and immutable.
- Explains memory reference / object identity behavior using `id()`.
- Identifies the mutable default argument pitfall and provides the standard `None` idiom fix.

---

### Q2: What is PEP 8, and why should developers adhere to it?
**Answer:** PEP 8 (Python Enhancement Proposal 8) is the official style guide for Python code authored by Guido van Rossum, Barry Warsaw, and Nick Coghlan. Its primary philosophy is that "readability counts" and code is read much more often than it is written.
Key guidelines in PEP 8 include:
- **Indentation:** 4 spaces per indentation level (never tabs).
- **Line Length:** Limit all lines to a maximum of 79 characters (or 88/100 characters in modern formatters like Black).
- **Naming Conventions:**
  - `snake_case` for functions, methods, and variables.
  - `PascalCase` (or `CapWords`) for classes.
  - `UPPER_CASE_WITH_UNDERSCORES` for module-level constants.
  - Leading underscore `_protected` for non-public internal methods/attributes, and double leading underscore `__private` for name mangling.
- **Imports:** Grouped in three sections separated by blank lines: Standard library, third-party libraries, and local application imports. Imports should be at the top of the file.
- **Whitespace:** Avoid extraneous whitespace inside parentheses, brackets, or before commas.
Adherence ensures consistency across open-source and corporate teams, reduces cognitive load during code reviews, and enables automated tooling (linters like Flake8, Ruff, and formatters like Black).
**Key Points:**
- Core purpose: Code readability and consistency.
- 4-space indentation; 79-character line guideline.
- Standard naming conventions for classes, functions, and constants.
- Import ordering: standard library, third-party, local modules.
- Modern ecosystem tools: Black, Ruff, Flake8, isort.
**Evaluation Criteria:**
- Understands that PEP 8 is a convention, not a syntax compiler requirement.
- Mentions concrete rules (naming conventions, indentation, import organization).
- Names real-world tools that enforce PEP 8.

---

### Q3: What are list comprehensions in Python, and when should you avoid using them?
**Answer:** A list comprehension provides a concise, readable way to construct lists from existing iterables. It combines a `for` loop and optional conditional filtering into a single expression:
`[expression for item in iterable if condition]`
Example:
```python
# Traditional loop
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x**2)

# List comprehension equivalent
squares = [x**2 for x in range(10) if x % 2 == 0]
```
List comprehensions are generally faster than standard `for` loops because the loop bytecode executes at C-speed without repeated calls to `list.append`.
**When to avoid:**
1. **Complex logic:** When nested loops or multiple condition branches make the comprehension hard to read.
2. **Large datasets:** List comprehensions build the entire list in memory immediately. If processing millions of rows, generator expressions `(x**2 for x in range(10**7))` or iterator streams should be used instead to conserve RAM.
3. **Side effects:** Comprehensions should be used to create new data structures, not to execute side-effects (e.g., do not write `[print(x) for x in items]`).
**Key Points:**
- Syntax and transformation from standard loops.
- Performance benefits due to optimized C-level iteration vs bytecode method calls.
- Readability threshold: Avoid multi-nested comprehensions.
- Memory implications: Avoid large dataset allocation; prefer generator expressions.
- Avoid using comprehensions purely for side effects.
**Evaluation Criteria:**
- Clearly describes syntax and output structure.
- Explains memory trade-offs between lists and generator expressions.
- Demonstrates engineering maturity by prioritizing code readability over cleverness.

---

### Q4: What is the difference between `==` and `is` in Python?
**Answer:**
- `==` is the equality comparison operator. It checks whether the *values* of two objects are equal by invoking the left operand's `__eq__()` magic method.
- `is` is the identity comparison operator. It checks whether two variables refer to the exact same object in memory, equivalent to comparing their memory addresses: `id(a) == id(b)`.

Example:
```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True, because values are identical
print(a is b)  # False, because they are distinct list instances in memory
print(a is c)  # True, because c references the exact same list instance
```
Special cases:
- Python interns small integers (typically between -5 and 256) and short strings for memory efficiency. Therefore, `x = 100; y = 100; x is y` may evaluate to `True`, but relying on this for equality is dangerous.
- `is` should strictly be used when checking singletons like `None` (`if val is None:`), `True`, or `False`.
**Key Points:**
- `==` tests value equivalence (`__eq__`); `is` tests memory address identity (`id()`).
- Separate objects can have identical values but different identities.
- Small integer caching / string interning can give false impressions of `is`.
- Proper usage of `is` is primarily for identity checks against singletons (`None`).
**Evaluation Criteria:**
- Clarifies value vs object reference distinction.
- Highlights singleton checking best practices (`is None`).
- Understands integer caching / interning hazards.

---

### Q5: How do Python virtual environments work, and why should you use them?
**Answer:** A Python virtual environment is an isolated directory tree containing a specific Python interpreter executable, its standard library copies or symlinks, and an independent set of installed third-party packages in its `site-packages` directory.
**Why use them:**
1. **Dependency Isolation:** Different projects often depend on incompatible versions of the same library (e.g., Project A needs `django==3.2`, Project B needs `django==4.2`).
2. **System Interpreter Protection:** Installing packages globally into the system Python via `sudo pip install` can corrupt operating system tools that rely on specific Python libraries.
3. **Reproducibility:** Combined with `requirements.txt` or `Pipfile.lock` / `poetry.lock`, virtual environments ensure consistent builds across development, staging, and production.
**How they work:**
Creating an environment with `python -m venv .venv` creates a directory with `bin/` (or `Scripts/` on Windows) and `lib/pythonX.Y/site-packages`. When activated, it sets the `VIRTUAL_ENV` environment variable and prepends `.venv/bin` to `PATH`. When `python` or `pip` is called, the shell finds the environment's binaries first.
**Key Points:**
- Solves dependency conflict across projects.
- Prevents pollution/corruption of the host operating system's system Python.
- Operates by manipulating the `PATH` environment variable and localizing `site-packages`.
- Modern tools: `venv` (built-in), `virtualenv`, `poetry`, `pipenv`, `conda`, `uv`.
**Evaluation Criteria:**
- Explains isolation of `site-packages` and interpreter.
- Describes the activation mechanism (PATH manipulation).
- Explains why global package installation is an anti-pattern.

---

### Q6: How does exception handling work in Python (`try`, `except`, `else`, `finally`)?
**Answer:** Python handles runtime errors using structured exception blocks:
- `try`: The block of code being monitored for exceptions.
- `except ExceptionType as err`: Catches and handles specific exceptions if they occur in the `try` block.
- `else`: Executes *only* if the `try` block completed successfully without raising any exceptions. This separates error handling from code that should run only on success.
- `finally`: Executes unconditionally, regardless of whether an exception occurred, was caught, or was re-raised. It is guaranteed to run even if `return`, `break`, or `continue` is invoked.

Example:
```python
try:
    f = open("data.txt", "r")
    content = f.read()
except FileNotFoundError as e:
    print(f"File missing: {e}")
except IOError as e:
    print(f"Read error: {e}")
else:
    process_data(content)
finally:
    if 'f' in locals() and not f.closed:
        f.close()
```
Best practices:
- Never use a bare `except:` without specifying the exception class, as it catches `KeyboardInterrupt` and `SystemExit`.
- Catch the most specific exception first, followed by broader exceptions.
**Key Points:**
- Roles of `try`, `except`, `else`, and `finally`.
- Execution guarantee of `finally` for resource cleanup.
- Purpose of `else` to prevent catching exceptions in subsequent execution lines.
- Avoiding bare `except:` and avoiding `except Exception:` unless logging/re-raising.
**Evaluation Criteria:**
- Explains the exact role and condition for `else` vs `finally`.
- Demonstrates awareness of resource management and exception specificity.

---

### Q7: How do you read and write files safely in Python using context managers?
**Answer:** The safest and most idiomatic way to handle file I/O in Python is using the `with` statement (a context manager):
```python
# Reading safely
with open("input.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())

# Writing safely
with open("output.txt", "w", encoding="utf-8") as file:
    file.write("Hello, World!\n")
```
**Why this is safe:**
1. **Automatic Resource Cleanup:** When execution exits the `with` block (normally or due to an unhandled exception), Python calls `file.__exit__()`, which guarantees `file.close()` is executed immediately.
2. **File Descriptor Leaks:** Without `with`, an unhandled exception before `file.close()` leaves the OS file descriptor open, leading to descriptor exhaustion in long-running processes.
3. **Explicit Encoding:** Specifying `encoding="utf-8"` avoids platform-dependent default encodings (e.g., Windows cp1252 vs Linux UTF-8).
4. **Line Iteration:** Iterating over `file` line-by-line reads lazily into memory via buffering instead of loading the entire multi-gigabyte file with `file.read()`.
**Key Points:**
- `with` statement utilizes the context manager protocol (`__enter__` and `__exit__`).
- Guarantees deterministic closure of file descriptors even upon exceptions.
- Memory efficiency of iterating over line streams.
- Importance of explicit character encodings.
**Evaluation Criteria:**
- Uses the `with open(...)` construct.
- Articulates the consequence of unclosed file handles (descriptor leak).
- Mentions chunked/lazy reading for memory efficiency.

---

### Q8: What are `*args` and `**kwargs` in Python function definitions?
**Answer:** `*args` and `**kwargs` allow functions to accept a variable number of positional and keyword arguments:
- `*args` (positional argument packing): The asterisk unpacks any extra positional arguments passed to the function into a `tuple`.
- `**kwargs` (keyword argument packing): The double asterisk unpacks any extra named/keyword arguments into a `dict`.

Example:
```python
def make_api_request(endpoint: str, *args, method: str = "GET", **kwargs):
    print(f"Endpoint: {endpoint}")
    print(f"Positional parameters: {args}")   # tuple
    print(f"Keyword headers/params: {kwargs}") # dict

make_api_request("/users", 1, 2, method="POST", timeout=30, auth="Bearer token")
```
Unpacking during function calls:
The same syntax can be used in reverse to unpack collections into function arguments:
```python
params = (10, 20)
options = {"color": "blue", "size": "large"}
draw_shape(*params, **options)
```
**Key Points:**
- `*args` captures arbitrary positional arguments into a `tuple`.
- `**kwargs` captures arbitrary keyword arguments into a `dict`.
- Argument order in signatures: standard positional, `*args`, keyword-only arguments, `**kwargs`.
- Can also be used at call sites to unpack iterables and dictionaries.
**Evaluation Criteria:**
- Accurately identifies resulting data structures (tuple for `*args`, dict for `**kwargs`).
- Explains both packing (parameter definition) and unpacking (function invocation).

---

### Q9: What is the purpose of `pip` and `requirements.txt`?
**Answer:**
- `pip` is the standard package installer for Python. It allows developers to install, inspect, update, and uninstall third-party packages distributed via the Python Package Index (PyPI) or version control repositories.
- `requirements.txt` is a standard flat-file configuration listing project dependencies and their specific version constraints.

Example `requirements.txt`:
```text
fastapi>=0.100.0,<1.0.0
uvicorn[standard]==0.23.2
pydantic~=2.4.0
pytest==7.4.2
```
Common commands:
- Installing from file: `pip install -r requirements.txt`
- Exporting environment: `pip freeze > requirements.txt` (though `pip freeze` exports all transitive dependencies flatly).
Modern alternatives like `pip-tools` (`requirements.in` -> compiled `requirements.txt`), `Poetry`, or `uv` provide lockfiles to ensure deterministic, cryptographically verified dependency resolution.
**Key Points:**
- `pip` manages PyPI package lifecycle.
- `requirements.txt` declares application dependencies and version pins.
- Version specifiers: `==` (exact), `>=` (minimum), `~=` (compatible release).
- Difference between direct dependencies and frozen transitive dependencies.
**Evaluation Criteria:**
- Explains `pip` CLI commands and requirements file syntax.
- Understands version pinning for reproducibility.

---

### Q10: What are type hints in Python, and how are they used?
**Answer:** Introduced in Python 3.5 (PEP 484), type hints allow developers to annotate function signatures, variables, and class attributes with expected data types. Python remains dynamically typed at runtime; type hints do not enforce static typing during interpreter execution, but are validated using static analysis tools like `mypy`, `pyright`, and IDE linters.
Example:
```python
from typing import List, Dict, Optional, Union, Callable

def calculate_discount(
    prices: list[float], 
    discount_rate: float, 
    customer_id: str | None = None
) -> float:
    total = sum(prices)
    return total * (1.0 - discount_rate)
```
Python 3.10+ introduced union syntax (`str | None` instead of `Optional[str]`) and built-in generic collections (`list[int]` instead of `typing.List[int]`).
**Benefits:**
1. Clear self-documenting code.
2. Catches type errors and `None`-dereference bugs before runtime.
3. Enhanced IDE autocomplete and refactoring support.
4. Used by runtime validation libraries like Pydantic and FastAPI for automated data validation and OpenAPI schema generation.
**Key Points:**
- Type hints are annotations; Python does not throw runtime TypeError merely for mismatched annotations.
- Verified at static analysis time via `mypy` or `pyright`.
- Modern syntax (Python 3.9/3.10+): built-in generics (`list`, `dict`) and pipe union (`|`).
- Enables runtime frameworks like Pydantic.
**Evaluation Criteria:**
- Emphasizes that Python remains dynamically typed at runtime.
- Demonstrates modern type annotation syntax.
- Explains practical benefits in large codebases and microservices.

---

## Medium

### Q1: What are Python decorators? Write a custom decorator that measures the execution time of a function.
**Answer:** A decorator is a structural design pattern in Python that wraps another function to extend or alter its behavior without modifying its source code. In Python, functions are first-class citizens: they can be passed as arguments, returned from other functions, and bound to variables.
A decorator takes a callable as an argument and returns a new callable. The `@decorator` syntax is syntactic sugar for `func = decorator(func)`.

Custom timing decorator implementation:
```python
import time
from functools import wraps
from typing import Callable, Any

def time_it(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.6f}s")
        return result
    return wrapper

@time_it
def compute_heavy_task(n: int) -> int:
    """Computes sum of squares."""
    return sum(i * i for i in range(n))
```
**Why `@wraps(func)` is crucial:**
Without `@wraps`, the decorated function loses its introspection metadata: `compute_heavy_task.__name__` would report `"wrapper"` and its docstring `__doc__` would be overwritten. `functools.wraps` copies the original function's name, docstring, module, and annotations to the wrapper.
**Key Points:**
- First-class function principles.
- `@decorator` syntax equivalence to `func = decorator(func)`.
- Use of `*args` and `**kwargs` in wrapper functions for generic applicability.
- Crucial role of `functools.wraps` in preserving metadata (`__name__`, `__doc__`).
**Evaluation Criteria:**
- Provides working, idiomatic code with `*args` and `**kwargs`.
- Uses `functools.wraps` and explains why it is necessary.
- Uses `time.perf_counter()` rather than `time.time()` for accurate benchmarking.

---

### Q2: What are generators and the `yield` keyword? How do they differ from regular functions?
**Answer:** A generator is a special type of iterator in Python that produces items lazily on-demand rather than computing and storing them all in memory at once.
- When a function contains the `yield` keyword, it becomes a generator function.
- Calling a generator function does not execute its body; instead, it returns a generator object implementing the iterator protocol (`__iter__()` and `__next__()`).
- When `next()` is called on the generator, execution proceeds until it encounters a `yield` statement. The yielded value is returned, and the function's local state, execution frame, and instruction pointer are frozen.
- On subsequent `next()` calls, execution resumes immediately after the `yield` statement until another `yield` is reached or the function returns (raising `StopIteration`).

Example:
```python
def fibonacci_stream():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Consuming finite items without infinite memory allocation
gen = fibonacci_stream()
for _ in range(5):
    print(next(gen))  # 0, 1, 1, 2, 3
```
Comparison:
- **Regular function:** Computes entire return object, returns once with `return`, and destroys its stack frame.
- **Generator function:** Produces a stream of values one-by-one with `yield`, pausing and preserving state between iterations with minimal $O(1)$ memory overhead.
**Key Points:**
- `yield` pauses execution and saves execution context.
- Adheres to iterator protocol (`__iter__`, `__next__`, `StopIteration`).
- $O(1)$ auxiliary memory footprint regardless of stream size.
- Generator expressions: `(x**2 for x in huge_list)`.
**Evaluation Criteria:**
- Clearly describes state preservation and execution pausing.
- Contras memory usage of lists vs generators for large datasets.
- Mentions iterator protocol and `StopIteration`.

---

### Q3: Explain Python's Method Resolution Order (MRO) and how `super()` works in multiple inheritance.
**Answer:** In Python, classes can inherit from multiple parent classes. Method Resolution Order (MRO) is the deterministic order in which Python searches for an attribute or method in a class hierarchy. Python uses the **C3 Linearization Algorithm** to construct the MRO.
The algorithm guarantees two properties:
1. Children precede their parents.
2. The order of parent classes listed in the class definition is preserved (monotonicity).

You can inspect a class's MRO using `Class.__mro__` or `Class.mro()`.
```python
class A:
    def process(self):
        print("A process")

class B(A):
    def process(self):
        print("B start")
        super().process()
        print("B end")

class C(A):
    def process(self):
        print("C start")
        super().process()
        print("C end")

class D(B, C):
    def process(self):
        print("D start")
        super().process()
        print("D end")

d = D()
d.process()
# MRO: D -> B -> C -> A -> object
```
**How `super()` works:**
`super()` does not simply call the immediate parent in the static source code. In Python 3, `super()` dynamically delegates method calls to the *next class in the MRO* of the calling instance. In the Diamond Problem above, `B`'s `super().process()` does not invoke `A.process()`; it invokes `C.process()`. This cooperative multiple inheritance guarantees each class method runs exactly once.
**Key Points:**
- C3 Linearization algorithm.
- Checking MRO via `Class.mro()`.
- `super()` resolves to the next class in the runtime MRO, not necessarily the lexical parent.
- Safe resolution of the Diamond Problem in object graphs.
**Evaluation Criteria:**
- Identifies C3 Linearization.
- Correctly predicts diamond pattern execution order.
- Explains dynamic behavior of `super()` in multi-inheritance chains.

---

### Q4: How do context managers work under the hood? Implement a custom context manager in two ways.
**Answer:** Context managers manage resource allocation and deallocation deterministically using the `with` statement.
Under the hood, entering a `with expr as var:` block:
1. Calls `context_manager = expr`.
2. Calls `var = context_manager.__enter__()`.
3. Executes the body.
4. When exiting the block, calls `context_manager.__exit__(exc_type, exc_val, exc_tb)`.
   - If an exception occurred, `exc_type` has the exception class.
   - If `__exit__` returns `True`, the exception is swallowed; if it returns `False` or `None`, the exception is propagated.

**Implementation 1: Class-based context manager**
```python
class DatabaseTransaction:
    def __init__(self, db_conn):
        self.conn = db_conn

    def __enter__(self):
        self.conn.begin_transaction()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
            print(f"Transaction rolled back due to {exc_val}")
            return False  # Propagate exception
        self.conn.commit()
        return True
```

**Implementation 2: Generator-based via `contextlib.contextmanager`**
```python
from contextlib import contextmanager

@contextmanager
def db_transaction(db_conn):
    db_conn.begin_transaction()
    try:
        yield db_conn
        db_conn.commit()
    except Exception as e:
        db_conn.rollback()
        raise e
```
**Key Points:**
- The protocol consists of `__enter__` and `__exit__`.
- Parameters of `__exit__`: exception type, exception value, and traceback.
- Exception suppression logic (returning `True` vs `False`).
- Alternative concise implementation using `contextlib.contextmanager` with `try/yield/finally`.
**Evaluation Criteria:**
- Demonstrates both class protocol and `contextlib` approach.
- Accurately details the arguments and return value semantics of `__exit__`.

---

### Q5: What is the Global Interpreter Lock (GIL), and what are its implications for concurrency?
**Answer:** The Global Interpreter Lock (GIL) is a mutex (mutual exclusion lock) used by CPython (the reference implementation of Python) to ensure that only one native OS thread executes Python bytecode at any given moment, even on multi-core processors.
**Why it exists:**
CPython's memory management relies heavily on reference counting (`PyObject_HEAD`). Without the GIL, concurrent operations in multiple threads could produce race conditions while updating reference counts, leading to memory leaks or premature deallocation of objects in use.
**Implications for concurrency:**
1. **CPU-bound tasks:** Pure computational tasks (e.g., matrix multiplication, image processing) achieve no speedup using `threading`. In fact, thread contention and context-switching overhead often make multithreaded CPU tasks slower than single-threaded equivalents.
   - *Solution:* Use `multiprocessing` (separate processes, separate memory spaces, separate GILs) or offload computation to C/Rust extensions (like NumPy, PyTorch) that release the GIL during heavy computations.
2. **I/O-bound tasks:** While waiting for network requests, disk reads, or database responses, Python threads release the GIL. Therefore, `threading` or `asyncio` provides high concurrency and performance gains for network calls or I/O workloads.
*Note:* Python 3.12+ has introduced per-interpreter GILs, and PEP 703 (free-threaded Python) is making the GIL optional in Python 3.13+.
**Key Points:**
- Mutex protecting CPython's reference counting and internal state.
- Single thread executes bytecode at a time per CPython process.
- CPU-bound tasks require `multiprocessing` or C extensions.
- I/O-bound tasks work effectively with `threading` and `asyncio` because the GIL is released during I/O.
- Modern direction: Per-interpreter GIL and PEP 703 free-threaded builds.
**Evaluation Criteria:**
- Explains *why* the GIL exists (reference counting thread safety).
- Differentiates CPU-bound vs I/O-bound concurrency behavior.
- Proposes appropriate alternatives (`multiprocessing`, `asyncio`, C-extensions).

---

### Q6: What is the difference between shallow copy and deep copy in Python?
**Answer:** Both shallow and deep copies duplicate an object, but they differ fundamentally in how they handle nested or compound objects.
- **Shallow Copy (`copy.copy()` or slice `[:]`):** Creates a new compound object, but populates it with references to the original nested child objects. If a nested object is modified, both the original and shallow copy reflect that change.
- **Deep Copy (`copy.deepcopy()`):** Recursively creates a new compound object and copies of all child and descendant objects found within it. Modifications to nested objects in the copy have zero effect on the original.

Example:
```python
import copy

original = [[1, 2, 3], ["a", "b"]]

# Shallow copy
shallow = copy.copy(original)
shallow[0].append(99)
print(original[0])  # [1, 2, 3, 99] - Original is modified!

# Deep copy
deep = copy.deepcopy(original)
deep[0].append(1000)
print(original[0])  # [1, 2, 3, 99] - Original remains unaffected
```
Caveat: `copy.deepcopy()` handles recursive references and circular object graphs safely by maintaining a memoization dictionary during traversal.
**Key Points:**
- Shallow copy copies the outer container, retaining references to child objects.
- Deep copy creates independent copies of all child and nested objects recursively.
- Pitfall of modifying nested mutable structures in shallow copies.
- `deepcopy` uses a memo dict to handle self-referential / cyclic data structures.
**Evaluation Criteria:**
- Explains reference sharing in shallow copies.
- Illustrates nested mutable state divergence.
- Mentions how circular references are handled in deep copy.

---

### Q7: What are `__slots__` in Python classes, and when should you use them?
**Answer:** By default, Python instances store their attributes in a dynamic dictionary named `__dict__`. This allows arbitrary new attributes to be attached to an instance at runtime, but each dictionary incurs significant memory overhead (typically hundreds of bytes per object).
`__slots__` allows a developer to explicitly declare a fixed set of attribute names for class instances.
```python
class Coordinate:
    __slots__ = ('x', 'y', 'z')
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
```
**Benefits:**
1. **Dramatic Memory Reduction:** Instances do not create a `__dict__`. Instead, attributes are stored in a compact, fixed-size C array of pointers. This can reduce memory usage by 60-80% when creating millions of small objects.
2. **Faster Attribute Access:** Direct array offset lookups are slightly faster than dictionary hashing.
3. **Attribute Restriction:** Prevents accidental assignment of misspelled attributes (raises `AttributeError`).

**Trade-offs / When not to use:**
- Disallows dynamic addition of undeclared attributes.
- Breaks multiple inheritance unless handled carefully (multiple parents with non-empty slots cause conflicts).
- Inheritance quirk: Subclasses do not inherit `__slots__` automatically; if a subclass does not define `__slots__`, it will create a `__dict__`.
**Key Points:**
- Replaces instance `__dict__` with a static array of pointers.
- Primary use-case: Micro-optimization for millions of lightweight instances.
- Memory savings (60-80%) and slight lookup speed improvement.
- Restrictions on dynamic attribute assignment and multiple inheritance.
**Evaluation Criteria:**
- Contrasts `__dict__` with `__slots__`.
- Identifies memory reduction as the primary motivation.
- Notes caveats regarding inheritance.

---

### Q8: How does asynchronous programming with `asyncio`, `async`, and `await` work in Python?
**Answer:** `asyncio` is a built-in library for concurrent programming using a single-threaded **event loop** and cooperative multitasking.
Instead of preemptive multitasking (where the OS switches threads), cooperative multitasking allows tasks to yield control voluntarily when waiting for I/O.
- `async def`: Defines a **coroutine** function. Calling it does not run it; it returns a coroutine object.
- `await`: Pauses execution of the coroutine and yields control back to the event loop until the awaited `Awaitable` (coroutine, Task, or Future) completes.
- **Event Loop:** The central orchestration engine that monitors running tasks and registered I/O file descriptors (using OS primitives like `epoll` or `kqueue`). When data is ready, the event loop resumes the paused coroutine.

Example:
```python
import asyncio
import httpx

async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def main():
    urls = ["https://api.example.com/items/1", "https://api.example.com/items/2"]
    # Run concurrent tasks
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```
**Critical rule:** Blocking operations (e.g., `time.sleep()`, synchronous `requests.get()`, heavy CPU loops) block the entire event loop, freezing all concurrent coroutines. Non-blocking libraries (`asyncio.sleep`, `aiohttp`, `httpx`) or `asyncio.to_thread()` must be used instead.
**Key Points:**
- Single-threaded cooperative multitasking via an event loop.
- Coroutines yield control at `await` expressions.
- High scalability for concurrent I/O operations with low memory overhead compared to OS threads.
- Threat of blocking the event loop with synchronous calls.
**Evaluation Criteria:**
- Explains the single-threaded event loop mechanism.
- Explains the role of `async`, `await`, and `asyncio.gather`.
- Emphasizes the hazard of synchronous blocking calls inside coroutines.

---

### Q9: What are magic (dunder) methods in Python? Explain `__str__` vs `__repr__` and `__call__`.
**Answer:** Magic methods (dunder methods, short for "double underscore") are special predefined methods in Python classes that allow objects to hook into Python language operators and built-in behaviors (such as operator overloading, indexing, string representation, iteration, and context management).

**1. `__str__` vs `__repr__`:**
- `__repr__(self)`: Intended for developers, debugging, and logging. Its output should be unambiguous and, whenever practical, look like valid Python code to recreate the object (e.g., `Point(x=1, y=2)`). Invoked by `repr(obj)` or interactive REPL.
- `__str__(self)`: Intended for end-users. Its output should be human-readable, clean, and informative. Invoked by `str(obj)` or `print(obj)`.
*Fallback rule:* If `__str__` is not defined, Python falls back to `__repr__`.

```python
class User:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r}, username={self.username!r})"

    def __str__(self) -> str:
        return f"{self.username} (ID: {self.user_id})"
```

**2. `__call__`:**
Implementing `__call__(self, *args, **kwargs)` makes an instance of a class callable like a standard function.
```python
class Multiplier:
    def __init__(self, factor: int):
        self.factor = factor

    def __call__(self, value: int) -> int:
        return value * self.factor

double = Multiplier(2)
print(double(10))  # 20
```
This is useful for stateful closures, caching decorators, and neural network layer abstractions (e.g., PyTorch `nn.Module`).
**Key Points:**
- Dunder methods intercept built-in language semantics.
- `__repr__` is for unambiguous developer debugging; `__str__` is for readable end-user display.
- `__call__` turns instances into callable objects, bridging stateful classes and functional abstractions.
**Evaluation Criteria:**
- Clearly distinguishes target audience and formatting requirements of `__repr__` vs `__str__`.
- Explains the purpose and real-world utility of `__call__`.

---

### Q10: How do `dataclasses` compare to standard classes and Pydantic models in Python?
**Answer:**
- **Standard Class:** Requires manual boilerplate for `__init__`, `__repr__`, `__eq__`, and hashing. Does not perform type checking or runtime validation.
- **`@dataclass` (Standard Library, Python 3.7+):** A decorator that automatically generates boilerplate methods (`__init__`, `__repr__`, `__eq__`, `__hash__`, `order=True`) based on type-annotated class attributes. It focuses purely on boilerplate reduction for in-memory data structures. It does *not* perform runtime type coercion or validation.
- **Pydantic (`BaseModel`):** A high-performance third-party data validation and parsing library. Unlike dataclasses, Pydantic parses input data, strictly coerces types at runtime (e.g., parsing string `"123"` to integer `123`), validates complex field constraints, handles JSON serialization, and generates JSON schemas (crucial for FastAPI and OpenAPI).

Comparison Table:
| Feature | Standard Class | `@dataclass` | Pydantic `BaseModel` |
| :--- | :--- | :--- | :--- |
| Boilerplate generation | Manual | Automated | Automated |
| Runtime Type Validation | No | No (hints only) | Yes (strict or coerced) |
| Standard Library | Built-in | Built-in | Third-party (C/Rust-accelerated in v2) |
| Performance overhead | Minimal | Minimal | Higher parsing cost (mitigated by Rust core) |
| Best Use Case | Domain logic & behavior | Internal data containers | API schemas, configs, external payloads |

```python
from dataclasses import dataclass
from pydantic import BaseModel, Field

@dataclass
class PointDC:
    x: float
    y: float

class PointPydantic(BaseModel):
    x: float
    y: float = Field(..., ge=0.0)

# Dataclass accepts invalid types silently at runtime:
p_dc = PointDC("abc", "def")  # No error

# Pydantic validates and raises ValidationError:
# p_py = PointPydantic(x="invalid", y=-5) -> Raises ValidationError
```
**Key Points:**
- `dataclass` eliminates boilerplate (`__init__`, `__repr__`, `__eq__`) without runtime type enforcement.
- Pydantic enforces runtime data validation, coercion, and serialization.
- Dataclasses for internal domain representations; Pydantic for system boundaries and APIs.
**Evaluation Criteria:**
- Accurately states that dataclasses do not validate types at runtime.
- Explains Pydantic's role in schema validation and serialization.
- Provides clear architectural recommendations on when to choose each.

---

## Hard

### Q1: How does Python's memory management work under the hood? Explain reference counting and cyclic garbage collection.
**Answer:** CPython's memory management operates on a three-tiered architecture: Python core object allocators, reference counting, and a generational cyclic garbage collector.

**1. Reference Counting (Primary Collector):**
Every Python object (`PyObject`) contains an internal field `ob_refcnt`.
- Whenever a variable references the object, is passed to a function, or is placed in a container, its reference count increases by 1.
- Whenever a variable goes out of scope, is reassigned, or is explicitly deleted with `del`, its reference count decreases by 1.
- As soon as `ob_refcnt == 0`, the memory allocated to the object is immediately reclaimed.
- *Limitation:* Reference counting cannot detect **reference cycles** (e.g., Object A references Object B, and Object B references Object A, while no external variables point to either).

**2. Generational Cyclic Garbage Collector (`gc` module):**
To resolve circular references, CPython runs a cyclic garbage collector that tracks container objects (`dict`, `list`, `set`, `tuple`, custom classes).
- **Generations:** Objects are organized into three generations: Gen 0, Gen 1, and Gen 2.
  - Gen 0 contains newly allocated container objects.
  - If an object survives a collection in Gen 0, it is promoted to Gen 1, and eventually to Gen 2 (long-lived objects).
- **Cycle Detection Algorithm:**
  1. The collector maintains a doubly linked list of tracked container objects and creates a temporary copy of each object's reference count (`gc_refs`).
  2. For each container, it decrements the `gc_refs` of any object it points to.
  3. Any object whose `gc_refs` drops to 0 is an internal cycle candidate.
  4. Objects reachable from outside the cycle are retained; unreachable cycles are isolated, finalizers are run, and memory is freed.
- **Tuning:** Controlled via `gc.collect()`, `gc.disable()`, and `gc.set_threshold()`.
**Key Points:**
- Immediate deterministic cleanup via reference counting (`ob_refcnt`).
- Inability of reference counting to resolve cyclic references.
- Generational collection (Gen 0, Gen 1, Gen 2) based on the weak generational hypothesis (most objects die young).
- Tri-color / trial-deletion cycle-finding algorithm on container objects.
**Evaluation Criteria:**
- Demonstrates deep knowledge of `ob_refcnt`.
- Explains the mechanism of reference cycles with an example.
- Describes the generational promotion strategy and cycle detection mechanism.

---

### Q2: What is the Python Descriptor Protocol, and how do `@property`, `classmethod`, and ORMs use it?
**Answer:** The descriptor protocol is the underlying mechanism that powers Python's attribute lookup, methods, properties, and ORM field mappings.
A descriptor is any object that implements at least one of the three protocol methods:
- `__get__(self, instance, owner=None)`
- `__set__(self, instance, value)`
- `__delete__(self, instance)`

**Data Descriptors vs Non-Data Descriptors:**
- **Data descriptor:** Implements `__set__` and/or `__delete__`. It takes precedence over instance `__dict__` during attribute lookup.
- **Non-data descriptor:** Implements only `__get__` (e.g., standard methods). If the instance `__dict__` has a key with the same name, the instance attribute overrides the non-data descriptor.

**How `@property` works:**
`property` is a built-in data descriptor.
```python
class CustomProperty:
    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("Unreadable attribute")
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("Can't set attribute")
        self.fset(instance, value)
```

**How ORMs (SQLAlchemy, Django ORM) work:**
ORMs define model columns as descriptors (e.g., `name = Column(String)`). When you access `user.name`:
- `__get__` intercepts the call, reads the underlying database record from the instance's tracked state, and handles lazy-loading.
- `__set__` intercepts assignments, runs field validation, marks the column as "dirty", and queues the change for the next transaction commit.
**Key Points:**
- Methods of descriptor protocol: `__get__`, `__set__`, `__delete__`.
- Precedence hierarchy: Data descriptors > Instance dictionary > Non-data descriptors > Class dictionary.
- How regular methods bind `self` (methods are non-data descriptors returning bound method callables).
- Practical real-world applications: `@property`, `@classmethod`, and ORM field abstractions.
**Evaluation Criteria:**
- Clearly distinguishes between data and non-data descriptors and lookup precedence.
- Explains how `@property` is constructed under the hood.
- Details how ORMs leverage descriptors to intercept column reads and writes.

---

### Q3: Explain Python metaclasses. When would you use them, and how do they differ from class decorators?
**Answer:** In Python, classes themselves are objects. A metaclass is the "class of a class"—it defines how a class is constructed, instantiated, and validated.
By default, all classes in Python are instances of the base metaclass `type`.
The class creation process:
`Class = MetaClass(name, bases, namespace_dict)`

Custom Metaclass implementation (e.g., enforcing an API contract):
```python
class InterfaceEnforcer(type):
    def __new__(mcs, name, bases, namespace):
        # Prevent enforcement on the base class itself
        if bases:
            if "execute" not in namespace or not callable(namespace["execute"]):
                raise TypeError(f"Class '{name}' must implement an 'execute()' method.")
        return super().__new__(mcs, name, bases, namespace)

class BaseTask(metaclass=InterfaceEnforcer):
    pass

class DataTask(BaseTask):
    def execute(self):
        print("Executing data task...")

# class InvalidTask(BaseTask): pass
# TypeError: Class 'InvalidTask' must implement an 'execute()' method.
```
**Metaclasses vs Class Decorators:**
- **Class Decorators:** Run *after* the class has already been completely constructed by `type`. They can inspect and modify attributes or wrap methods cleanly. They are simpler, more composable, and preferred for 95% of use cases.
- **Metaclasses:** Run *during* class creation before the class object even exists in the namespace. They have full control over `__prepare__` (which controls the class namespace dict before execution) and inheritance trees. Subclasses automatically inherit the metaclass of their parent, whereas class decorators must be explicitly reapplied to every subclass.
**Key Points:**
- Classes are instances of `type`.
- `__new__` vs `__init__` in metaclasses.
- Automatic inheritance of metaclasses by derived subclasses.
- Class decorators run post-construction; metaclasses run during construction.
- Use cases: Framework architecture, automatic registration, abstract enforcement, ORM schema compilation.
**Evaluation Criteria:**
- Understands that `type` is the default metaclass.
- Explains the sequence: `__prepare__` -> `__new__` -> `__init__`.
- Articulates why class decorators are usually preferred and when metaclasses are strictly necessary.

---

### Q4: Design a robust, production-grade asynchronous producer-consumer pipeline with `asyncio.Queue`, backpressure, and graceful shutdown.
**Answer:** A production-grade async pipeline must handle concurrency limits, backpressure (preventing producers from exhausting memory when consumers are slow), error isolation, and signal handling for graceful shutdown.

```python
import asyncio
import signal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Pipeline")

async def producer(queue: asyncio.Queue, stop_event: asyncio.Event, producer_id: int):
    item_id = 0
    while not stop_event.is_set():
        try:
            item = f"prod-{producer_id}-item-{item_id}"
            # Put with timeout to allow checking stop_event
            await asyncio.wait_for(queue.put(item), timeout=1.0)
            logger.info(f"Produced: {item}")
            item_id += 1
            await asyncio.sleep(0.1)
        except asyncio.TimeoutError:
            continue
        except asyncio.CancelledError:
            break
    logger.info(f"Producer {producer_id} terminated.")

async def consumer(queue: asyncio.Queue, consumer_id: int):
    while True:
        try:
            item = await queue.get()
            # Process item
            await asyncio.sleep(0.3)  # Simulating work
            logger.info(f"Consumer {consumer_id} processed: {item}")
            queue.task_done()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error processing {item}: {e}")
            queue.task_done()

async def main():
    # maxsize enforces backpressure
    queue = asyncio.Queue(maxsize=10)
    stop_event = asyncio.Event()

    producers = [asyncio.create_task(producer(queue, stop_event, i)) for i in range(2)]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(4)]

    # Run for a demonstration period
    await asyncio.sleep(2.0)

    # Graceful Shutdown Sequence:
    logger.info("Initiating graceful shutdown...")
    # 1. Stop producers
    stop_event.set()
    await asyncio.gather(*producers)

    # 2. Drain remaining queue items
    await queue.join()
    logger.info("Queue completely drained.")

    # 3. Cancel consumers
    for c in consumers:
        c.cancel()
    await asyncio.gather(*consumers, return_exceptions=True)
    logger.info("All workers cleanly stopped.")

if __name__ == "__main__":
    asyncio.run(main())
```
**Key Points:**
- `maxsize` parameter in `asyncio.Queue` creates backpressure by blocking producers when the queue is full.
- `queue.task_done()` and `queue.join()` ensure all enqueued tasks finish processing before shutdown.
- Two-stage shutdown: Stop producers first -> wait for `queue.join()` -> cancel consumer tasks.
- Handling `asyncio.CancelledError` properly.
**Evaluation Criteria:**
- Incorporates backpressure via bounded queue size.
- Implements correct shutdown order avoiding dropped messages.
- Demonstrates error handling inside worker loops.

---

### Q5: How does CPython implement dictionaries internally, and how was it optimized in Python 3.6+?
**Answer:** In Python 3.6+ (originally designed by Raymond Hettinger and implemented by Inada Naoki), Python dictionaries were completely overhauled to be compact and preserve insertion order.
**Old Implementation (Pre-3.6):**
Used a sparse hash table where each bucket contained:
`[hash_code, key_pointer, value_pointer]`
To keep hash collisions low, the table had to remain 1/3 empty (sparse). This resulted in substantial unused memory because every empty entry still consumed 24 bytes (on 64-bit platforms).

**New Implementation (Compact Dict):**
The modern implementation splits the dictionary into two arrays:
1. **Dense Array (`entries`):** An array containing only valid entries in the exact order they were inserted:
   `entries = [[hash, key, value], [hash, key, value], ...]`
2. **Sparse Array (`indices`):** A small integer array (1-byte `int8`, 2-byte `int16`, etc.) that acts as the hash table.
   `indices = [None, 0, None, 1, None, None]`

**Lookup Mechanism:**
1. Compute the hash of the key: `h = hash(key)`.
2. Compute index bucket: `idx = h & (table_size - 1)`.
3. Check `indices[idx]`. If empty, key does not exist.
4. If non-empty, retrieve the entry offset `pos = indices[idx]`.
5. Check `entries[pos]`. If hash and key match (`==`), return value.
6. If collision occurs, probe using Python's pseudo-random perturbation formula: `idx = (5 * idx + 1 + perturb) & (table_size - 1)`.

**Benefits:**
- Reduces dictionary memory consumption by 20% to 40%.
- Guarantees iteration in insertion order as a language specification.
- Resizing simply rebuilds the small `indices` array.
**Key Points:**
- Split architecture: Sparse `indices` table + dense `entries` table.
- Open addressing with perturbation probing for collision resolution.
- Memory savings due to dense packing of 24-byte entry tuples.
- Deterministic insertion order preservation.
**Evaluation Criteria:**
- Explains the two-array compact dictionary structure.
- Details the collision resolution strategy (open addressing with perturbation).
- Explains how insertion ordering became an intrinsic property.

---

### Q6: How do you identify, diagnose, and fix memory leaks in production Python applications?
**Answer:** Python memory leaks typically fall into three categories:
1. **Unintentional object retention:** Objects remain referenced in global registries, class variables, long-lived caches (e.g., unbounded `@lru_cache`), or event listener lists.
2. **Cyclic references with non-collectable dependencies:** Cycles involving C extensions or suppressed garbage collection.
3. **C-extension memory leaks:** Native memory allocated via `malloc()` in C/C++ extensions that is never released.

**Diagnostic Tooling & Workflow:**
1. **`tracemalloc` (Built-in standard library):**
   Takes snapshots of Python memory allocations attributing them to exact source code lines.
   ```python
   import tracemalloc
   tracemalloc.start()
   snapshot1 = tracemalloc.take_snapshot()
   # Run workload...
   snapshot2 = tracemalloc.take_snapshot()
   top_stats = snapshot2.compare_to(snapshot1, 'lineno')
   for stat in top_stats[:5]:
       print(stat)
   ```
2. **`objgraph`:**
   Visualizes object reference graphs and finds which object is preventing garbage collection:
   ```python
   import objgraph
   objgraph.show_most_common_types(limit=10)
   # Inspect backreferences holding an object alive
   leaking_objs = objgraph.by_type('LeakingState')
   if leaking_objs:
       objgraph.show_backrefs(leaking_objs[0], max_depth=5, filename='leak.png')
   ```
3. **`memray` (Bloomberg's profiler):**
   Modern profiler that tracks both Python bytecode allocations and native C/C++ allocations with zero code modification.

**Remediation Strategies:**
- Use `weakref` (`weakref.ref` or `weakref.WeakValueDictionary`) for caches and observer patterns so references do not block garbage collection.
- Bound all caches with TTL or LRU capacity limits.
- Ensure context managers or `finally` blocks clear large buffers (`del large_df`).
**Key Points:**
- Root causes: Global lists, unbounded caches, uncollected cycles, C-extension leaks.
- Step-by-step methodology using `tracemalloc`, `objgraph`, and `memray`.
- Using `weakref` to break reference ownership in caching/event designs.
**Evaluation Criteria:**
- Distinguishes between native memory leaks and Python object reference retention.
- Recommends concrete tools (`tracemalloc`, `objgraph`, `memray`).
- Suggests architectural fixes (weakref, bounded caches, explicit lifecycle teardown).

---

### Q7: Explain the PyObject structure and the Python C API memory allocators (PyMalloc).
**Answer:** In CPython, everything is a `PyObject`. At the C level, every object starts with the `PyObject_HEAD` macro:
```c
struct _object {
    _PyObject_HEAD_EXTRA // doubly-linked list pointers for tracing
    Py_ssize_t ob_refcnt;
    struct _typeobject *ob_type;
};
```
- `ob_refcnt`: 64-bit integer tracking reference count.
- `ob_type`: Pointer to the object's type object (which defines methods, size, and behavior).
- Variable-length objects (like `tuple`, `list`, `str`) use `PyVarObject_HEAD`, which adds `Py_ssize_t ob_size`.

**Memory Allocation Hierarchy (PyMalloc):**
Standard C `malloc()` has high overhead and causes memory fragmentation when allocating millions of tiny objects (e.g., small integers, floats, short strings). CPython implements a custom allocator called **PyMalloc** for small requests ($\le 512$ bytes):
1. **Arenas:** 256 KB memory chunks requested from the OS via standard `malloc` or `mmap`.
2. **Pools:** Each arena is divided into 4 KB pools. A pool only allocates objects of a single fixed size-class (e.g., 16-byte pool, 32-byte pool, up to 512 bytes).
3. **Blocks:** Each pool is subdivided into uniform blocks of that size-class. Allocating and freeing blocks uses an ultra-fast singly linked free-list with $O(1)$ allocation time and zero fragmentation within that size class.
4. **Large Allocations (> 512 bytes):** Fall back directly to system `malloc`.
**Key Points:**
- `PyObject` structure: `ob_refcnt` and `ob_type`.
- Problem solved by PyMalloc: Fragmentation and system call overhead for small objects ($\le 512$ bytes).
- Architecture: Arenas (256 KB) $\rightarrow$ Pools (4 KB) $\rightarrow$ Blocks (size-classes).
- Large allocations bypass PyMalloc and call system `malloc`.
**Evaluation Criteria:**
- Details the fields of `PyObject_HEAD`.
- Articulates why general-purpose system allocators fail for Python's allocation profile.
- Explains the Arena/Pool/Block hierarchy of PyMalloc.

---

### Q8: What are `__getattr__` vs `__getattribute__`, and how can you safely implement dynamic attribute interception?
**Answer:** Both methods intercept attribute access, but at fundamentally different stages of the lookup pipeline:
1. `__getattribute__(self, name)`:
   - Called **unconditionally** for *every single* attribute access on the instance.
   - Evaluated before checking instance `__dict__` or class attributes.
   - Danger: Accessing any `self.attribute` inside `__getattribute__` will recursively invoke `__getattribute__`, resulting in a `RecursionError` (infinite stack overflow).
   - Safe access requires delegating to the superclass: `super().__getattribute__(name)`.
2. `__getattr__(self, name)`:
   - Called **only as a fallback** when the attribute is *not* found in the instance dictionary, class hierarchy, or descriptors.
   - Safe and idiomatic for lazy loading, dynamic proxies, and RPC clients.

Example of a safe dynamic logging proxy:
```python
class AuditedClient:
    def __init__(self, target):
        # Must bypass __setattr__ if overridden, or use standard dict assignment
        super().__setattr__("_target", target)

    def __getattribute__(self, name):
        # Unconditional logging
        if not name.startswith("_"):
            print(f"[AUDIT] Accessing attribute: {name}")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        # Fallback for dynamic dispatch
        target = super().__getattribute__("_target")
        if hasattr(target, name):
            attr = getattr(target, name)
            print(f"[AUDIT] Dynamic dispatch to target for: {name}")
            return attr
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
```
**Key Points:**
- `__getattribute__` is unconditional and easily causes infinite recursion if not calling `super()`.
- `__getattr__` is called only after normal attribute resolution fails.
- Safe modification of `self.__dict__` or delegation via `super()`.
- Common patterns: RPC stubs, dynamic adapters, security wrappers.
**Evaluation Criteria:**
- Clearly highlights the unconditional nature of `__getattribute__` vs fallback nature of `__getattr__`.
- Warns about the recursion trap and provides the `super()` solution.

---

### Q9: What are the implications of PEP 703 (Making the Global Interpreter Lock Optional / Free-threaded Python)?
**Answer:** PEP 703 represents one of the most ambitious architectural changes in Python's history: removing the GIL from CPython to enable true multi-core parallel execution across native threads.
**Technical Challenges & Changes:**
1. **Biased Reference Counting:**
   - Standard reference counting requires atomic instructions (`lock xadd` in x86) for thread safety. Atomic operations on every object touch would cause massive CPU cache-line bouncing and slow single-threaded execution by 30-50%.
   - PEP 703 uses *biased reference counting*: Each object is biased towards the thread that created it. That thread increments/decrements non-atomically. Other threads use atomic instructions and a deferred decref list.
2. **Immortal Objects:**
   - Core runtime singletons (`None`, `True`, `False`, small integers, interned strings) are marked as immortal; their reference count operations are no-ops, eliminating lock contention.
3. **Mimalloc Memory Allocator:**
   - Replaces PyMalloc with Microsoft's thread-safe, scalable `mimalloc` allocator.
4. **Thread-safe Collections:**
   - Dictionaries and lists require fine-grained internal locking or lock-free reads to avoid race conditions during concurrent mutations.

**Implications for Developers:**
- Multithreaded Python code can achieve true $N\times$ speedups on $N$ cores for CPU-heavy tasks without `multiprocessing`.
- Existing C-extensions with non-thread-safe global state will experience data races unless rewritten with proper thread synchronization.
**Key Points:**
- Replaces GIL with biased reference counting and immortal objects.
- Uses `mimalloc` for thread-safe memory management.
- Eliminates the single-thread performance penalty of naive atomic increments.
- Enables true parallelism for CPU workloads, but places synchronization burden on extension authors.
**Evaluation Criteria:**
- Explains why naive atomic reference counting degrades single-thread speed.
- Outlines biased reference counting and immortal objects.
- Articulates impact on existing C-extensions and application concurrency.

---

### Q10: How do you interface Python with C/C++ libraries? Compare `ctypes`, `cffi`, and C-extensions with Cython.
**Answer:** Interfacing Python with native C/C++ code is essential for high-performance numerical computing, interacting with hardware, or reusing legacy systems.

**1. `ctypes` (Standard Library):**
- Foreign Function Interface (FFI) included in Python.
- Loads shared libraries (`.so`, `.dll`) dynamically and converts Python types to C types at runtime using pure Python code.
- *Pros:* No compilation step required; standard library.
- *Cons:* Slower due to runtime dynamic marshalling; easy to cause segmentation faults with invalid pointer dereferences.

**2. `cffi` (C Foreign Function Interface):**
- Can parse standard C declarations directly (`cdef`).
- Supports both ABI (in-memory dynamic binding) and API mode (compiles a dedicated C extension wrapper).
- *Pros:* Much safer than `ctypes`, high performance in API mode, PyPy compatible.
- *Cons:* Requires C compiler toolchain in API mode.

**3. Cython / Pybind11 / Native C-Extensions:**
- **Cython:** An optimizing static compiler that compiles Python-like `.pyx` code with static C type annotations directly into C/C++ CPython extension modules.
- **Pybind11:** Modern header-only C++11 library that binds C++ classes and functions to Python cleanly.
- *Pros:* Maximum raw performance. Allows explicit releasing of the GIL with `with nogil:`, executing native parallel code across all CPU cores.
- *Cons:* Heavy build dependency; complex compilation and distribution (wheels for multiple OS/architectures).

Comparison Table:
| Tool | Build Step Needed | Safety | Performance | Best Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `ctypes` | None | Low | Medium | Quick bindings to system DLLs |
| `cffi` | Optional | High | High | Python wrappers around mature C libraries |
| Cython | Required | Medium | Maximum | Speeding up algorithmic Python code & NumPy extensions |
| Pybind11 | Required | High | Maximum | Exposing modern C++11/17 codebases to Python |
**Key Points:**
- `ctypes` is interpreted runtime FFI (no compiler needed).
- `cffi` offers safer C declaration parsing and API compilation.
- Cython/Pybind11 compile directly to CPython C-extension modules with `with nogil` support.
- Trade-offs between build complexity, execution speed, and memory safety.
**Evaluation Criteria:**
- Accurately contrasts all three paradigms.
- Highlights GIL release capabilities in Cython/C++ extensions.
- Evaluates tooling choice based on build overhead vs runtime performance.
