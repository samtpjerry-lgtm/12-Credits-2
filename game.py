import tkinter as tk
import random


# Gives the game a title and sets the colour and dimensions of the game

class QuizGame:
    def __init__(self, root):
        self.root = root

        # ====================================================
        # WINDOW SETTINGS
        # ====================================================

        self.root.title("Quiz Game")
        self.root.geometry("900x700")
        self.root.configure(bg="#111111")
        self.root.resizable(False, False)

        # ====================================================
        # GAME VARIABLES
        # ====================================================

        self.score = 0
        self.question_number = 0

        # ====================================================
        # QUESTIONS
        # ====================================================

        self.questions = [
            {
                "question": "What is 2 + 2?",
                "answers": ["3", "4", "5", "6"],
                "correct": "4"
            },
            {
                "question": "What planet do we live on?",
                "answers": ["Mars", "Earth", "Venus", "Jupiter"],
                "correct": "Earth"
            },
            {
                "question": "How many days are in a week?",
                "answers": ["5", "6", "7", "8"],
                "correct": "7"
            },
            {
                "question": "What color do you get by mixing red and blue?",
                "answers": ["Green", "Orange", "Purple", "Yellow"],
                "correct": "Purple"
            },
            {
                "question": "What is 10 × 5?",
                "answers": ["15", "50", "55", "100"],
                "correct": "50"
            },

            # Medium
            {
                "question": "What is the square root of 144?",
                "answers": ["10", "11", "12", "14"],
                "correct": "12"
            },
            {
                "question": "Which element has the chemical symbol 'Au'?",
                "answers": ["Silver", "Gold", "Aluminium", "Argon"],
                "correct": "Gold"
            },
            {
                "question": "What is 15% of 200?",
                "answers": ["20", "25", "30", "35"],
                "correct": "30"
            },
            {
                "question": "Which country has the largest population?",
                "answers": ["India", "USA", "Brazil", "Japan"],
                "correct": "India"
            },
            {
                "question": "What is the binary representation of decimal 10?",
                "answers": ["1001", "1010", "1100", "1110"],
                "correct": "1010"
            },

            # Hard
            {
                "question": "If f(x) = x² - 3x + 2, what is f(4)?",
                "answers": ["4", "5", "6", "8"],
                "correct": "6"
            },
            {
                "question": "Which scientist formulated the three laws of planetary motion?",
                "answers": [
                    "Isaac Newton",
                    "Johannes Kepler",
                    "Galileo Galilei",
                    "Albert Einstein"
                ],
                "correct": "Johannes Kepler"
            },
            {
                "question": "What is the derivative of x³ + 2x² - 5x?",
                "answers": [
                    "3x² + 4x - 5",
                    "3x² + 2x - 5",
                    "x² + 4x - 5",
                    "3x³ + 4x² - 5"
                ],
                "correct": "3x² + 4x - 5"
            },
            {
                "question": "Which data structure uses LIFO (Last In, First Out)?",
                "answers": ["Queue", "Stack", "Tree", "Graph"],
                "correct": "Stack"
            },
            {
                "question": "What is the time complexity of binary search on a sorted array?",
                "answers": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
                "correct": "O(log n)"
            },

            # Extreme
            {
                "question": "What is the determinant of [[3, 2], [1, 4]]?",
                "answers": ["8", "10", "12", "14"],
                "correct": "10"
            },
            {
                "question": "In special relativity, what remains invariant between inertial reference frames?",
                "answers": [
                    "Time",
                    "Length",
                    "Spacetime interval",
                    "Kinetic energy"
                ],
                "correct": "Spacetime interval"
            },
            {
                "question": "Which algorithm has an average-case time complexity of O(n log n)?",
                "answers": [
                    "Bubble sort",
                    "Insertion sort",
                    "Merge sort",
                    "Linear search"
                ],
                "correct": "Merge sort"
            },
            {
                "question": "If a fair six-sided die is rolled twice, what is the probability of getting a sum of 7?",
                "answers": ["1/6", "1/8", "1/12", "1/18"],
                "correct": "1/6"
            },
            {
                "question": "What is the integral of 2x from x = 0 to x = 3?",
                "answers": ["6", "9", "12", "18"],
                "correct": "9"
            }
        ]

        # Show the first question
        self.show_quiz()


    # ========================================================
    # SHOW QUIZ
    # ========================================================

    def show_quiz(self):

        # Clear anything currently on the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Get the current question
        question = self.questions[self.question_number]

        # Game title
        title = tk.Label(
            self.root,
            text="⚡ QUIZ GAME ⚡",
            font=("Courier New", 32, "bold"),
            fg="#00ffff",
            bg="#111111"
        )
        title.pack(pady=25)

        # Question number and score
        status = tk.Label(
            self.root,
            text=f"Question {self.question_number + 1}/{len(self.questions)}"
                 f"     Score: {self.score}",
            font=("Courier New", 15),
            fg="white",
            bg="#111111"
        )
        status.pack()

        # Question
        question_label = tk.Label(
            self.root,
            text=question["question"],
            font=("Courier New", 19, "bold"),
            fg="white",
            bg="#111111",
            wraplength=780,
            justify="center"
        )
        question_label.pack(pady=50)


# ============================================================
# START GAME
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()
