import tkinter as tk
import random


# Gives the game a title and sets colour and dimentions of the game


class QuizGame:
    def __init__(self, root):
        self.root = root

        # Window settings
        self.root.title("Quiz Game")
        self.root.geometry("900x700")
        self.root.configure(bg="#111111")
        self.root.resizable(False, False)


# Starts the game


if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()