"""
Simple Python Calculator
Author: Student Project
"""

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b


def show_menu():
    print("\n==== Python Calculator ====")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")


while True:
    show_menu()

    choice = input("Choose an option (1-5): ")

    if choice == "5":
        print("Goodbye!")
        break

    if choice not in ["1", "2", "3", "4"]:
        print("Invalid option. Try again.")
        continue

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Please enter valid numbers.")
        continue

    if choice == "1":
        result = add(num1, num2)
        print(f"Result: {result}")

    elif choice == "2":
        result = subtract(num1, num2)
        print(f"Result: {result}")

    elif choice == "3":
        result = multiply(num1, num2)
        print(f"Result: {result}")

    elif choice == "4":
        result = divide(num1, num2)
        print(f"Result: {result}")
