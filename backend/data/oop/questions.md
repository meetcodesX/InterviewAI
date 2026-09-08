# Object-Oriented Programming (OOP) Interview Questions

## Easy

### Q1: What are the four foundational pillars of Object-Oriented Programming, and what does each accomplish?
**Answer:** The four foundational pillars of Object-Oriented Programming are Encapsulation, Abstraction, Inheritance, and Polymorphism. **Encapsulation** bundles data and methods that operate on that data into a single unit (a class) while restricting direct access to internal state. **Abstraction** hides complex implementation details and exposes only essential interfaces to callers. **Inheritance** enables new classes to derive properties and behaviors from existing parent classes, fostering code reuse. **Polymorphism** allows objects of different classes to respond to identical method invocations in their own unique, context-specific ways.
**Key Points:**
- Encapsulation: Bundling data and methods; access control via private/protected modifiers.
- Abstraction: Exposing public interfaces while concealing internal mechanics.
- Inheritance: Subclasses inheriting state and behavior from superclasses.
- Polymorphism: Single interface, multiple implementations (runtime and compile-time).
**Evaluation Criteria:** Candidate should clearly enumerate all four pillars, provide distinct definitions for each, and avoid conflating abstraction with encapsulation.

### Q2: What is Encapsulation, and how is it implemented in modern object-oriented languages?
**Answer:** Encapsulation is the principle of bundling state (fields) and behavior (methods) together inside a class while hiding the internal representation of the object from external code. It is implemented using access modifiers—such as `private`, `protected`, and `public`—to ensure that fields cannot be mutated arbitrarily from the outside. Instead, controlled read and write operations are exposed through public getters, setters, or domain-driven methods that enforce business validation rules. This protects object invariants, reduces unexpected side-effects, and allows internal data structures to be refactored without breaking external consumer code.
**Key Points:**
- Bundling data and operations inside a cohesive class boundary.
- Information hiding via access modifiers (`private`, `protected`, `public`).
- Enforces validation and invariant consistency via getters/setters/methods.
- Enables safe internal refactoring without affecting public contracts.
**Evaluation Criteria:** Look for an understanding of access control, protection of class invariants, and how encapsulation enables safe internal refactoring.

### Q3: What is Inheritance in OOP, and what are its primary advantages and potential risks?
**Answer:** Inheritance is a mechanism where a child class (subclass or derived class) inherits state and behaviors from a parent class (superclass or base class), establishing an "is-a" relationship (e.g., a `Dog` is an `Animal`). Its primary advantage is code reuse, eliminating duplication across related entities and allowing polymorphic handling through base type references. However, overusing inheritance leads to tightly coupled class hierarchies where changes to a base class can unpredictably break derived subclasses—a pitfall known as the "fragile base class" problem. In modern software engineering, composition is generally preferred over deep inheritance hierarchies.
**Key Points:**
- Models "is-a" conceptual relationships.
- Enables code reuse and foundational polymorphism.
- Risk: Tight coupling between superclasses and subclasses.
- Fragile base class problem: Base class changes can cascade regressions downstream.
**Evaluation Criteria:** Candidate should identify the "is-a" relationship, explain code reuse benefits, and candidly acknowledge coupling risks associated with deep inheritance trees.

### Q4: What is Polymorphism, and what is the difference between compile-time and runtime polymorphism?
**Answer:** Polymorphism, meaning "many forms," allows objects of different types to be manipulated through a unified interface. Compile-time (or static) polymorphism is resolved during compilation and is typically implemented via method overloading (multiple methods with the same name but different parameter signatures) or operator overloading. Runtime (or dynamic) polymorphism is resolved during execution using method overriding, where a derived class provides a specific implementation of a virtual method declared in its base class. Dynamic polymorphism allows a collection of base-type references to invoke overridden derived methods at runtime without the caller needing to know the concrete types.
**Key Points:**
- Ability to process objects differently based on their data type or class.
- Compile-time (static): Method overloading; resolved by compiler based on signatures.
- Runtime (dynamic): Method overriding; resolved via dynamic dispatch during execution.
- Enables extensible, decoupled code adhering to the Open/Closed Principle.
**Evaluation Criteria:** Candidate should clearly separate compile-time (overloading) from runtime (overriding) polymorphism and explain how dynamic dispatch functions.

### Q5: How does Abstraction differ from Encapsulation?
**Answer:** While both principles support information hiding, Abstraction focuses on *what* an object does, whereas Encapsulation focuses on *how* an object protects and manages its internal data. Abstraction hides complexity by presenting an intuitive, simplified interface to the caller—such as using an abstract class or interface to define actions like `startCar()` without exposing internal engine mechanics. Encapsulation restricts direct access to internal variables and state, bundling data with methods that manipulate it to maintain data integrity. In short, abstraction is design-level simplification of interfaces, while encapsulation is implementation-level restriction of internal state.
**Key Points:**
- Abstraction: Focuses on "what" an object does; hides complexity behind high-level interfaces.
- Encapsulation: Focuses on "how" data is protected; bundles state and operations within boundaries.
- Abstraction is achieved through interfaces and abstract classes.
- Encapsulation is achieved through access modifiers (`private`) and accessor methods.
**Evaluation Criteria:** Candidate must clearly articulate the conceptual boundary: abstraction conceals system complexity via interfaces, whereas encapsulation conceals data state via access restriction.

### Q6: What is the difference between a Class and an Object?
**Answer:** A class is a blueprint, prototype, or user-defined type that defines the attributes (state) and methods (behavior) that entities of its type will possess; it occupies memory primarily for metadata and method definitions. An object is a concrete, living instance of a class created in memory at runtime (usually on the heap) containing its own distinct set of attribute values. For example, `Car` is a class defining properties like `color` and `speed`, while a red Tesla model with license plate `XYZ-123` is a specific object instance created from that class. You can instantiate countless unique objects from a single class blueprint.
**Key Points:**
- Class: Blueprint, type definition, or template; contains no runtime state.
- Object: Physical, concrete runtime instance with allocated memory holding unique state.
- Analogy: Architectural blueprint vs. actual constructed building.
- Instantiation: Allocates memory on the heap and executes the constructor.
**Evaluation Criteria:** Look for understanding of compile-time definition (blueprint) versus runtime memory instantiation (stateful instance).

### Q7: What is the purpose of a Constructor, and how does it differ from a regular method?
**Answer:** A constructor is a special member function automatically executed when a new object instance of a class is created. Its primary purpose is to initialize the newly created object's state, allocate necessary resources, and enforce invariants so the object is never left in an uninitialized or invalid state. Unlike regular methods, constructors have the same name as the class, have no explicit return type (not even `void`), and cannot be invoked directly like normal member functions. Many languages also provide default no-argument constructors if no explicit constructor is defined, and support constructor overloading to allow different initialization styles.
**Key Points:**
- Special function invoked automatically upon object instantiation (`new ClassName()`).
- Purpose: Initialize fields, allocate resources, and ensure valid initial state.
- Syntax: Shares class name, has no return type, and cannot be called like a standard method.
- Supports overloading: Multiple constructors with different parameters.
**Evaluation Criteria:** Candidate should explain initialization guarantees, structural differences from standard methods, and the concept of constructor overloading.

### Q8: What is the difference between Method Overloading and Method Overriding?
**Answer:** Method Overloading occurs within the same class when multiple methods share the same name but have different parameter lists (differing parameter types, counts, or order), representing compile-time polymorphism. Method Overriding occurs across an inheritance hierarchy when a subclass provides a specific implementation of a method that is already defined in its superclass, sharing the exact same name, return type, and parameter signature. Overloading is resolved at compile-time by the compiler matching arguments, whereas overriding is resolved dynamically at runtime based on the actual object instance type via dynamic dispatch.
**Key Points:**
- Overloading: Same class, same method name, different parameter signatures; compile-time resolution.
- Overriding: Superclass and subclass, identical method signature; runtime dynamic resolution.
- Return type: Changing return type alone is insufficient for overloading; overriding requires compatible types.
- Annotations: Overriding often utilizes annotations (e.g., `@Override`) to ensure compiler safety.
**Evaluation Criteria:** Candidate must contrast scope (same class vs. subclass), signature requirements (must differ vs. must match), and binding time (compile-time vs. runtime).

### Q9: What are Access Modifiers (public, private, protected), and how do they control visibility?
**Answer:** Access modifiers are keywords that set the accessibility and visibility boundaries of classes, methods, and variables within an object-oriented codebase. `public` members are accessible from any other class anywhere in the application. `private` members are completely hidden and accessible only from within the declaring class itself, establishing the core boundary of encapsulation. `protected` members are accessible within the declaring class, its derived subclasses, and often classes within the same package/namespace depending on language specifications. Using the most restrictive access modifier possible (the principle of least privilege) minimizes coupling and prevents accidental external mutations.
**Key Points:**
- `public`: Unrestricted visibility to all callers across packages/modules.
- `private`: Strictly restricted to the declaring class; foundational to encapsulation.
- `protected`: Accessible within declaring class and its derived subclasses.
- Principle of Least Privilege: Default to `private`, expose only deliberate APIs as `public`.
**Evaluation Criteria:** Candidate should define all three modifiers accurately and link their usage to the Principle of Least Privilege and encapsulation integrity.

### Q10: What is the purpose of the `this` (or `self`) keyword in object-oriented programming?
**Answer:** The `this` (or `self` in languages like Python) keyword is an implicit reference pointing to the current instance of the class executing the method. It is used to resolve naming ambiguities when method parameters or local variables share the exact same names as instance variables (e.g., `this.name = name`). Additionally, it is used to pass the current object instance as an argument to other methods, return the current instance to enable fluent method chaining (Builder pattern), and invoke alternative constructors within the same class (`this()`).
**Key Points:**
- Reference pointing to the current object instance in memory.
- Disambiguates instance fields from local parameters with identical names.
- Enables fluent API design and method chaining by returning `this`.
- Supports constructor chaining within the same class.
**Evaluation Criteria:** Candidate should explain instance referencing, name disambiguation, and advanced uses such as method chaining and constructor delegation.

---

## Medium

### Q1: What is the difference between an Abstract Class and an Interface, and when should you choose one over the other?
**Answer:** An interface is a pure behavioral contract specifying *what* methods an implementing class must provide, without maintaining object state (fields), and a class can implement multiple interfaces. An abstract class is an incomplete blueprint that can define both abstract methods and fully implemented concrete methods, as well as instance variables and constructors, but a class can inherit from only one abstract class (in single-inheritance languages like Java and C#). You should choose an interface when you want to define a decoupled role or capability across unrelated classes (e.g., `Comparable`, `Serializable`). You should choose an abstract class when you want to share common state, internal helper methods, or provide base implementations across closely related classes in an "is-a" hierarchy.
**Key Points:**
- Interface: Pure contract of behavior; no instance state; multiple implementation allowed.
- Abstract Class: Partial implementation blueprint; can maintain state and constructors; single inheritance.
- Multiple inheritance: Classes can implement many interfaces, but inherit from only one base class.
- Selection criteria: Abstract class for shared base state/logic; interface for decoupled capabilities across hierarchies.
**Evaluation Criteria:** Candidate should contrast state, inheritance limits (single vs. multiple), and provide clear architectural criteria for choosing between them.

### Q2: Why is "Composition over Inheritance" considered an essential object-oriented design heuristic?
**Answer:** "Composition over Inheritance" recommends modeling relationships using "has-a" relationships (composing objects with references to other objects) rather than "is-a" relationships (class inheritance). Class inheritance introduces tight coupling, because derived classes are exposed to the implementation details of their superclasses (breaking encapsulation) and cannot alter inherited behavior dynamically at runtime. Composition keeps classes loosely coupled, promotes single-responsibility components, and allows behaviors to be swapped or reconfigured dynamically at runtime by injecting different implementations. Furthermore, composition avoids the combinatorial explosion of subclasses that occurs when combining orthogonal features via inheritance.
**Key Points:**
- Favor "has-a" composition over "is-a" class inheritance.
- Inheritance exposes subclass to base class implementation details (violates encapsulation).
- Composition enables runtime behavior swapping via dependency injection.
- Avoids rigid, deeply nested class hierarchies and combinatorial subclass explosion.
**Evaluation Criteria:** Candidate must explain why inheritance violates encapsulation, how composition allows runtime flexibility, and why deep inheritance trees become unmaintainable.

### Q3: Explain the Single Responsibility Principle (SRP) and Open/Closed Principle (OCP) in the context of object-oriented design.
**Answer:** The Single Responsibility Principle asserts that a class should have one, and only one, reason to change, meaning it must encapsulate a single cohesive concern. For example, separating an `Invoice` entity from an `InvoicePrinter` and an `InvoiceRepository` ensures that formatting changes or database migrations do not impact billing business logic. The Open/Closed Principle dictates that classes should be open for extension but closed for modification. Rather than editing existing, tested classes with conditional statements whenever new behavior is introduced, designers use polymorphism, interfaces, and patterns like Strategy or Decorator to plug in new functionality without touching existing source code.
**Key Points:**
- SRP: One reason to change; cohesive focus on a single business actor or concern.
- SRP example: Separating data modeling, persistence, and presentation into distinct classes.
- OCP: Classes should be open for extension but closed for modification.
- OCP mechanisms: Polymorphism, strategy patterns, abstract interfaces replacing switch statements.
**Evaluation Criteria:** Look for clear definitions of both principles, the concept of "reason to change," and code design techniques that enable extension without code modification.

### Q4: Explain the Liskov Substitution Principle (LSP) and provide a concrete example that violates it.
**Answer:** The Liskov Substitution Principle requires that objects of a superclass should be replaceable with objects of a subclass without altering the correctness of the program. A classic violation is the `Square` inheriting from `Rectangle` problem: if a `Rectangle` exposes `setWidth(w)` and `setHeight(h)`, client code reasonably assumes that modifying width leaves height unchanged. However, a `Square` subclass must override `setWidth()` to mutate both dimensions simultaneously to maintain its invariant, breaking caller expectations and causing bugs in algorithms calculating area. Another common LSP violation is a derived subclass throwing `NotSupportedException` or `UnimplementedError` for an inherited base method, signaling that the hierarchy is conceptually flawed.
**Key Points:**
- Subtypes must be substitutable for their base types without altering program correctness.
- Subclasses must preserve behavioral contracts, preconditions, and postconditions.
- Classic violation: `Square` inheriting from `Rectangle` (breaks dimension independence invariant).
- Code smell: Subclasses throwing `NotSupportedException` or callers checking types with `instanceof`.
**Evaluation Criteria:** Candidate should explain behavioral subtyping (preconditions cannot be strengthened, postconditions cannot be weakened) and walk through the classic Rectangle-Square violation.

### Q5: Explain the Interface Segregation Principle (ISP) and Dependency Inversion Principle (DIP).
**Answer:** The Interface Segregation Principle states that clients should not be forced to depend on interfaces they do not use, advocating for small, role-specific interfaces rather than large, bloated "fat" interfaces (e.g., breaking a massive `Worker` interface into `Workable` and `Feedable` so a `RobotWorker` isn't forced to implement an empty `eat()` method). The Dependency Inversion Principle states that high-level business policy modules should not depend on low-level detail modules; both must depend on abstractions. Furthermore, abstractions should not depend on details; details should depend on abstractions. DIP decouples business logic from specific persistence engines, third-party libraries, or communication protocols by inverting dependency directions using interfaces.
**Key Points:**
- ISP: Decompose monolithic "fat" interfaces into cohesive, client-specific role interfaces.
- ISP prevents forcing classes to implement dummy or throwaway methods.
- DIP: High-level modules and low-level modules must both depend on abstractions.
- Decouples core business domain from infrastructure concerns (databases, network APIs).
**Evaluation Criteria:** Candidate must define ISP in terms of client interface bloat, explain the directional inversion in DIP, and connect DIP to modern dependency injection practices.

### Q6: What is the Strategy Design Pattern, and how does it replace complex conditional statements with polymorphism?
**Answer:** The Strategy pattern defines a family of algorithms, encapsulates each one into a separate class, and makes them interchangeable at runtime through a common interface. Instead of a monolithic class containing long `if-else` or `switch` statements to determine behavior (such as selecting between credit card, PayPal, or crypto payment algorithms), the host context delegates the execution to an injected `PaymentStrategy` interface. Adding a new payment algorithm simply requires creating a new class implementing the interface, leaving existing code completely untouched. This pattern directly implements the Open/Closed Principle and eliminates fragile, sprawling conditional control flow.
**Key Points:**
- Encapsulates algorithms into interchangeable classes sharing a common interface.
- Context delegates execution to the strategy rather than executing conditional logic.
- Eliminates brittle `switch` / `if-else` blocks and reduces cyclomatic complexity.
- Implements the Open/Closed Principle by allowing dynamic addition of new strategies.
**Evaluation Criteria:** Candidate should explain the components (Context, Strategy Interface, Concrete Strategies) and explain how it adheres to OCP and simplifies conditionals.

### Q7: What is the Observer Design Pattern, and what challenges arise with memory management when using it?
**Answer:** The Observer pattern defines a one-to-many dependency between objects such that when one object (the Subject) changes its state, all its registered dependents (Observers) are notified and updated automatically. The Subject maintains an internal list of observers and exposes `attach()`, `detach()`, and `notify()` methods, decoupling the event emitter from event consumers. A major architectural challenge is memory management, specifically the "lapsed listener" problem: if observers register with a long-lived subject but fail to explicitly unregister, the subject retains strong references to them, preventing garbage collection and causing severe memory leaks. This is often resolved by using weak references (`WeakReference`) or scoped event subscription lifecycles.
**Key Points:**
- One-to-many notification mechanism between Subject and registered Observers.
- Promotes loose coupling; Subject does not know concrete observer types.
- Lapsed Listener Problem: Strong references retained by subject cause persistent memory leaks.
- Mitigation: Explicit `unsubscribe()` routines or using weak references (`WeakReference`).
**Evaluation Criteria:** Candidate should define the pattern's mechanics, describe loose coupling benefits, and identify the lapsed listener memory leak problem with solutions.

### Q8: What is the difference between Static (Early) Binding and Dynamic (Late) Binding in OOP?
**Answer:** Static (early) binding occurs at compile time when the compiler binds a method call directly to a specific memory address based on the declared reference type; this is used for `static`, `private`, and `final` methods, as well as overloaded methods. Dynamic (late) binding occurs at runtime when the execution environment determines which method implementation to execute based on the actual type of the object instance in memory, rather than the reference type. Dynamic binding is the underlying mechanism that powers virtual methods, method overriding, and runtime polymorphism. While static binding offers faster execution speed due to direct branching and inlining opportunities, dynamic binding provides architectural flexibility and modular extensibility.
**Key Points:**
- Static (Early) Binding: Resolved at compile time based on reference type; used for static/private/final methods.
- Dynamic (Late) Binding: Resolved at runtime based on the concrete object instance in memory.
- Dynamic binding enables runtime polymorphism and virtual method overriding.
- Performance: Static binding allows compiler inlining; dynamic binding incurs slight dispatch overhead.
**Evaluation Criteria:** Look for understanding of compile-time vs. runtime resolution, association with method types (static/final vs. virtual), and connection to runtime polymorphism.

### Q9: What is the "Diamond Problem" in multiple inheritance, and how do modern OOP languages resolve or prevent it?
**Answer:** The Diamond Problem occurs in languages supporting multiple class inheritance when a class $D$ inherits from two classes $B$ and $C$, which both inherit from a single base class $A$. If $B$ and $C$ both override a method from $A$, class $D$ faces ambiguity regarding which version of the method to inherit and execute, and whether $D$ should contain one or two copies of $A$'s state. Languages like C++ resolve this using `virtual base classes` to share state and explicit scope resolution operators (`B::method()`) to disambiguate calls. Modern languages like Java, C#, and Kotlin prevent the problem entirely by disallowing multiple class inheritance, permitting multiple inheritance only through interfaces with explicit conflict resolution rules for default methods.
**Key Points:**
- Ambiguity arising when a subclass inherits conflicting implementations from two intermediate classes sharing a common ancestor.
- Ambiguity over method resolution and duplication of inherited member fields.
- C++ solution: Virtual inheritance (`virtual public Base`) and explicit namespace resolution.
- Modern language approach (Java/C#): Single class inheritance, allowing multiple interface implementations with explicit collision rules.
**Evaluation Criteria:** Candidate should draw or describe the diamond inheritance shape, explain the ambiguity of both state and behavior, and contrast C++ virtual inheritance with Java/C# single-inheritance constraints.

### Q10: What is the Decorator Design Pattern, and how does it dynamically extend object behavior without subclassing?
**Answer:** The Decorator pattern dynamically attaches additional responsibilities and behaviors to an object at runtime, providing a flexible alternative to subclassing for extending functionality. It works by having both the concrete component and the decorator implement the same abstract interface; the decorator holds a wrapped reference to an instance of that interface and forwards calls to it while executing supplemental logic before or after. For example, wrapping a base `FileInputStream` inside a `BufferedInputStream` and then a `GZIPInputStream` adds buffering and decompression capabilities transparently. This avoids the explosive proliferation of static subclasses that would otherwise be required to support every possible combination of features.
**Key Points:**
- Attaches behavior dynamically at runtime without modifying underlying classes.
- Decorator implements the same interface as the component it wraps (transparent wrapper).
- Forwards operations to the wrapped instance while adding pre/post-processing behaviors.
- Prevents subclass combinatorial explosion (e.g., `BufferedGzipFileInputStream`).
**Evaluation Criteria:** Candidate should explain interface parity, object wrapping/forwarding mechanics, and the prevention of class explosion.

---

## Hard

### Q1: How do Virtual Method Tables (vtables) and Virtual Table Pointers (vptrs) work internally to implement dynamic dispatch in compiled OOP languages?
**Answer:** In compiled languages like C++, whenever a class defines or inherits a virtual function, the compiler creates a static Virtual Method Table (`vtable`) for that class containing an array of function pointers corresponding to its virtual methods. Every instance of that class is secretly augmented with a hidden Virtual Pointer (`vptr`) pointing to its class's specific `vtable`. When a virtual method is called via a base pointer or reference (e.g., `basePtr->draw()`), the compiler does not emit a direct `call` instruction; instead, it generates instructions to dereference the object's `vptr`, locate the method offset in the `vtable`, and perform an indirect call to that function address. This introduces a slight overhead: extra memory per object for the `vptr`, cache-miss potential from pointer indirection, and the inability of the compiler to inline the function call without devirtualization optimizations.
**Key Points:**
- `vtable`: Static array of function pointers created per class containing virtual methods.
- `vptr`: Hidden pointer embedded in each object instance referencing its class's `vtable`.
- Dynamic dispatch mechanics: `vptr` dereference $\to$ index lookup in `vtable` $\to$ indirect function call.
- Performance implications: Memory overhead per instance, pointer indirection, loss of compiler inlining.
**Evaluation Criteria:** Candidate must detail the exact low-level mechanics (vtable array, per-instance vptr, offset indexing, indirect call instruction) and explain the performance trade-offs.

### Q2: How do you architect an extensible Rules Engine or Pipeline using SOLID principles and GoF design patterns?
**Answer:** An extensible rules engine is designed by decoupling rule definition, evaluation, and orchestration through interfaces and composition. Each business rule implements a `Rule` interface exposing an `evaluate(Context)` method (Command/Specification pattern), allowing rules to be tested and instantiated independently in accordance with the Single Responsibility Principle. Complex rules are constructed hierarchically using the Composite pattern, combining atomic rules with logical operators like `AndRule`, `OrRule`, and `NotRule`. The execution pipeline coordinates rules using the Chain of Responsibility or Strategy pattern, where an orchestrator evaluates rules against an immutable context and aggregates results. New business requirements are accommodated by authoring new rule classes without modifying the core evaluation engine, perfectly satisfying the Open/Closed Principle.
**Key Points:**
- Specification / Command pattern: Encapsulates individual business rules into discrete, testable classes.
- Composite pattern: Combines atomic rules into complex logical trees (`And`, `Or`, `Not`).
- Chain of Responsibility / Pipeline: Passes domain context through sequential rule evaluators.
- Open/Closed Principle: System is extended by adding new rule implementations without touching the engine core.
**Evaluation Criteria:** Look for cohesive integration of multiple design patterns (Specification, Composite, Chain of Responsibility) and clear adherence to SOLID principles.

### Q3: What is the Fragile Base Class problem, and how does component-based composition eliminate its architectural risks?
**Answer:** The Fragile Base Class problem occurs when seemingly safe, isolated modifications to a base class introduce unintended bugs or broken invariants in derived subclasses that depend on the base class's internal implementation details. For example, if a base `CustomSet` modifies its `addAll()` method to internally call `add()`, a subclass that overridden both methods to track insertion counts will accidentally double-count elements. This happens because inheritance breaks encapsulation by exposing base implementation mechanics to derived classes. Component-based composition eliminates this by treating components as black-box objects interacting strictly through well-defined public interfaces without shared internal implementation state. Dependencies are injected, behaviors are delegated, and internal refactoring of a component cannot trigger side effects in client classes.
**Key Points:**
- Unintended subclass breakage caused by modifying internal base class implementation details.
- Root cause: Inheritance breaks encapsulation across parent-child class boundaries.
- Classic example: Self-invocation of overridden methods causing double counting in collections.
- Composition remedy: Black-box interfaces, delegation, and dependency injection isolate components completely.
**Evaluation Criteria:** Candidate should clearly explain how inheritance violates encapsulation, illustrate how internal base class changes break subclass invariants, and demonstrate how composition prevents the problem.

### Q4: Explain the Visitor Design Pattern, Double Dispatch, and why Visitor is used over standard polymorphism in Abstract Syntax Trees (ASTs).
**Answer:** The Visitor pattern separates algorithms from the objects on which they operate by allowing a "visitor" object to execute operations across a disparate collection of heterogeneous element classes. It solves the limitation that most languages support only Single Dispatch (method execution depends on the runtime type of a single receiving object). Visitor implements **Double Dispatch**: the client calls `element.accept(visitor)`, passing `this` to the visitor (`visitor.visit(this)`), allowing the runtime types of *both* the element and the visitor to determine the executed method. In compilers and AST processing, node types (e.g., `BinaryExpr`, `Literal`, `IfStatement`) are relatively stable, but operations performed on them (type-checking, code generation, linting, optimization) grow continuously. Visitor enables adding an arbitrary number of new operations simply by creating new visitor classes without polluting AST node definitions.
**Key Points:**
- Separates algorithms from object structures; enables adding operations without modifying classes.
- Overcomes single-dispatch constraints via Double Dispatch (`accept(visitor)` $\to$ `visit(this)`).
- Two dispatch lookups determine execution based on types of both receiver and visitor.
- Ideal for compilers/ASTs: Stable node hierarchies with rapidly expanding operational requirements.
**Evaluation Criteria:** Candidate must clearly explain Single vs. Double Dispatch, trace the two-step dispatch flow, and articulate why AST processing is the ideal use case.

### Q5: How does the Prototype Design Pattern work, and what are the nuances and memory risks of Shallow Copying versus Deep Copying?
**Answer:** The Prototype pattern creates new objects by cloning an existing prototype instance rather than invoking constructors, which is particularly beneficial when object creation is computationally expensive or requires complex configuration. In a **Shallow Copy**, the primitive fields are copied by value, but references to nested objects are copied by reference, meaning both the original and cloned objects point to the exact same child objects in memory. In a **Deep Copy**, the object and its entire graph of referenced child objects are recursively duplicated in memory. The risks of shallow copying include unintended side-effects and data corruption when mutating shared state, while deep copying risks infinite recursion on cyclic object graphs, high memory allocation, and significant CPU serialization overhead.
**Key Points:**
- Prototype pattern: Object creation via cloning existing template instances.
- Shallow Copy: Duplicates top-level primitives; shares internal object references.
- Deep Copy: Recursively clones the entire object graph, creating fully independent copies.
- Edge case risks: Cyclic references causing infinite recursion, memory bloat, thread contention on shared state.
**Evaluation Criteria:** Candidate should contrast memory structures of shallow vs. deep copies, identify the danger of mutating shared child references, and explain how cyclic graphs complicate deep copies.

### Q6: What are Mixins and Traits, and how do they provide horizontal code reuse without the pitfalls of classical multiple inheritance?
**Answer:** Mixins and Traits are language mechanisms designed to provide horizontal code reuse across disparate class hierarchies without suffering from the Diamond Problem of multiple class inheritance. A **Trait** is a cohesive collection of method definitions (and optional default implementations) that contains no instance state; conflicts between identical method names in multiple traits must be resolved explicitly by the composing class (as in Scala, Rust, or PHP). A **Mixin** is a class containing methods for use by other classes without having to be the parent class, often parameterized and linearized into a single inheritance chain at compile time (as in Ruby or Python). Because traits forbid state and enforce explicit conflict resolution, they allow modular capabilities (e.g., `Logging`, `JsonSerializable`) to be composed safely across unrelated classes.
**Key Points:**
- Horizontal reuse: Sharing functionality across orthogonal classes without an "is-a" hierarchy.
- Traits: Stateless behavioral units; require explicit conflict resolution when names collide.
- Mixins: Parameterized inheritance linearization providing modular behavior injection.
- Eliminates the Diamond Problem by disallowing state duplication and ordering linearization explicitly.
**Evaluation Criteria:** Candidate should contrast vertical inheritance with horizontal capability composition, explain state absence in traits, and describe how conflict resolution operates.

### Q7: How do you design a thread-safe Object Pool in an object-oriented system, and what performance trade-offs govern its use?
**Answer:** An Object Pool manages a reusable cache of pre-allocated, expensive objects (e.g., database connections, network sockets, thread workers) to avoid frequent allocation and garbage collection churn. A thread-safe pool is implemented using a concurrent, non-blocking queue or bounded blocking queue (e.g., `ConcurrentLinkedQueue`) protected by atomic primitives or locks, exposing `acquire()` and `release()` operations. The pool must enforce object validation on checkout/checkin, reset object state upon return to prevent state contamination, and implement eviction policies for stale or broken resources. While object pools were historically popular, in modern runtimes with hyper-optimized generational garbage collectors, pooling small, short-lived memory objects is an anti-pattern that increases lock contention and cache fragmentation; pooling should be reserved strictly for heavyweight, I/O-bound, or external system resources.
**Key Points:**
- Purpose: Reuses heavyweight, expensive-to-initialize resources (sockets, database connections).
- Thread safety: Lock-free concurrent queues, semaphores, or mutexes managing pool capacity.
- State reset: Returned objects must be cleansed to prevent data leaks between callers.
- Performance reality: Modern GCs handle short-lived allocations faster than pools; pool only heavyweight I/O resources.
**Evaluation Criteria:** Candidate should explain synchronization mechanisms, state reset hygiene, and modern JVM/runtime realities where naive object pooling degrades performance.

### Q8: Explain the Law of Demeter (Principle of Least Knowledge) and the architectural dangers of "train wreck" code.
**Answer:** The Law of Demeter (LoD) states that a module or method should have limited knowledge of the internal structure of other objects, interacting only with its immediate neighbors. Formally, a method $M$ of object $A$ should only invoke methods on: $A$ itself, parameters passed into $M$, objects created within $M$, or direct component fields of $A$. Violations produce "train wreck" code statements—such as `order.getCustomer().getAddress().getCity().toLowerCase()`—which tightly couple the calling class to the entire navigation path and internal topology of four different classes. When any intermediate class refactors its structure, the calling code breaks. Respecting LoD requires delegating responsibility (e.g., `order.getDeliveryCity()`), preserving encapsulation and shielding callers from structural changes.
**Key Points:**
- Principle of Least Knowledge: Objects should talk only to their immediate friends.
- Train wreck code: Long method invocation chains (`a.getB().getC().getD().doSomething()`).
- High fragility: Callers are tightly coupled to the entire structural topology of the domain graph.
- Remediation: Delegate behaviors down the chain ("Tell, Don't Ask") so intermediate state is encapsulated.
**Evaluation Criteria:** Look for formal Demeter rules, identification of "train wreck" method chaining, and the "Tell, Don't Ask" principle as a refactoring remedy.

### Q9: Contrast the Template Method pattern with the Strategy pattern, and explain how the "Hollywood Principle" applies.
**Answer:** Both patterns enforce inversion of control, but they achieve it through different structural mechanisms: Template Method relies on class inheritance, whereas Strategy relies on object composition. In **Template Method**, an abstract base class defines the invariant skeletal algorithm in a `final` template method, delegating specific invariant steps to abstract or hook methods overridden by subclasses. In **Strategy**, the algorithm is factored into an independent interface, and the host context delegates the entire execution to an injected strategy instance, allowing behaviors to be swapped at runtime. Both exemplify the "Hollywood Principle" ("Don't call us, we'll call you"), where low-level components plug into a high-level framework that dictates when and how low-level methods are invoked. Strategy is generally preferred because it provides runtime flexibility and avoids rigid inheritance coupling.
**Key Points:**
- Template Method: Uses inheritance; base class controls skeleton, subclasses override steps.
- Strategy: Uses composition; context delegates entire algorithm to an interchangeable strategy object.
- Hollywood Principle: High-level abstractions orchestrate the workflow, invoking low-level code.
- Trade-off: Template Method locks workflow into static inheritance; Strategy allows dynamic runtime swapping.
**Evaluation Criteria:** Candidate should contrast structural mechanisms (inheritance vs. composition), explain algorithm execution control, and articulate the Hollywood Principle.

### Q10: How do Domain-Driven Design (DDD) tactical patterns (Entities, Value Objects, Aggregates) elevate OOP domain models above Anemic Domain Models?
**Answer:** An Anemic Domain Model is an anti-pattern where domain classes consist merely of public getters and setters with zero business logic, while all business rules reside in procedural service classes, violating basic object-oriented encapsulation. Tactical DDD restores rich object orientation through three constructs: **Value Objects** are immutable objects defined solely by their attributes (e.g., `Money`, `Address`) with no conceptual identity, encapsulating validation and calculation logic. **Entities** possess a unique conceptual identity that persists through state changes across time (e.g., `User`, `Order`). An **Aggregate** is a cluster of entities and value objects treated as a single unit for data changes, bounded by an **Aggregate Root** that directly mediates all external modifications to enforce business invariants transactionally. This ensures that domain objects are expressive, self-validating, and strictly protect their own consistency boundaries.
**Key Points:**
- Anemic Domain Model: Data and behavior are separated (dumb DTOs manipulated by procedural services).
- Rich Domain Model: Encapsulates business logic, behavior, and invariants within domain classes.
- Value Objects: Immutable, identity-free, self-validating descriptors of characteristics.
- Entities: Identity-driven lifecycles; Aggregates/Aggregate Roots enforce transactional consistency boundaries.
**Evaluation Criteria:** Candidate must contrast anemic vs. rich domain models, define the distinct roles of Entities and Value Objects, and explain how Aggregate Roots protect business invariants.
