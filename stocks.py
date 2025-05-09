# Summary: This module is just a shorter name for the program that can start either the Console or GUI version of the program.

import stock_console
import stock_GUI

def main():
    while True:
        print("""
Choose Interface:
1 - Console Mode
2 - GUI Mode
3 - Exit
""")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            stock_console.main()
        elif choice == "2":
            stock_GUI.main()
        elif choice == "3":
            print("Thank you for using the GUI or Console")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()