#Python calculator
#Briged McCarthy 2024

# Number input and operation input
num1 = int(input("Type the first number for your equation: "))
num2 = int(input("Type the second number for your equation: "))
operation = int(input("Choose your operation (addition(1), subtraction(2), multiplication(3), division(4): "))

# Basic calculator program
if operation == 1:
    print(num1 + num2)
if operation == 2:
    print(num1 - num2)
if operation == 3:
    print(num1 * num2)
if operation == 4:
    print(num1 / num2)