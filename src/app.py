import tkinter as tk
from paint import Paint

root = tk.Tk()

def main():
    app = Paint(root)
    root.mainloop()

if __name__ == "__main__":
    main()