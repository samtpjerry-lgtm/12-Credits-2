import tkinter as tk
import random


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
        # MAZE VARIABLES  (Step 1)
        # ====================================================

        self.maze_level = 0
        self.canvas_size = 600
        self.cell_size = 30
        self.maze_width = 20
        self.maze_height = 20
        self.player_x = 1
        self.player_y = 1
        self.exit_x = self.maze_width - 2
        self.exit_y = self.maze_height - 2
        self.maze = None
        self.canvas = None

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

        # ====================================================
        # ANSWER BUTTONS
        # ====================================================

        answers = question["answers"].copy()
        random.shuffle(answers)

        for answer in answers:
            button = tk.Button(
                self.root,
                text=answer,
                font=("Courier New", 16, "bold"),
                fg="white",
                bg="#222222",
                activebackground="#00ffff",
                activeforeground="black",
                width=25,
                height=2,
                command=lambda selected=answer: self.check_answer(selected)
            )
            button.pack(pady=8)

    # ========================================================
    # CHECK ANSWER
    # ========================================================

    def check_answer(self, selected_answer):

        question = self.questions[self.question_number]

        if selected_answer == question["correct"]:
            self.score += 1

        self.question_number += 1

        if self.question_number < len(self.questions):
            self.show_quiz()
        else:
            self.show_results()

    # ========================================================
    # SHOW RESULTS
    # ========================================================

    def show_results(self):

        # Clear anything currently on the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Results title
        title = tk.Label(
            self.root,
            text="⚡ QUIZ COMPLETE ⚡",
            font=("Courier New", 32, "bold"),
            fg="#00ffff",
            bg="#111111"
        )
        title.pack(pady=80)

        # Score
        score_label = tk.Label(
            self.root,
            text=f"You scored {self.score}/{len(self.questions)}",
            font=("Courier New", 24, "bold"),
            fg="white",
            bg="#111111"
        )
        score_label.pack(pady=20)

        # Restart button
        restart_button = tk.Button(
            self.root,
            text="PLAY AGAIN",
            font=("Courier New", 16, "bold"),
            fg="white",
            bg="#222222",
            activebackground="#00ffff",
            activeforeground="black",
            width=20,
            height=2,
            command=self.restart_game
        )
        restart_button.pack(pady=30)

        # Quit button
        quit_button = tk.Button(
            self.root,
            text="QUIT",
            font=("Courier New", 16, "bold"),
            fg="white",
            bg="#222222",
            activebackground="#00ffff",
            activeforeground="black",
            width=20,
            height=2,
            command=self.root.destroy
        )
        quit_button.pack(pady=10)

    # ========================================================
    # RESTART GAME
    # ========================================================

    def restart_game(self):

        self.score = 0
        self.question_number = 0
        self.maze_level = 0

        self.show_quiz()

    # ========================================================
    # MAZE GENERATION  (Step 2)
    # ========================================================

    def generate_maze(self):
        # Start with all walls
        maze = [
            [1 for _ in range(self.maze_width)]
            for _ in range(self.maze_height)
        ]

        # Recursive backtracking to carve paths
        def carve(x, y):
            maze[y][x] = 0

            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if (
                    1 <= nx < self.maze_width - 1
                    and 1 <= ny < self.maze_height - 1
                    and maze[ny][nx] == 1
                ):
                    maze[y + dy // 2][x + dx // 2] = 0
                    carve(nx, ny)

        carve(1, 1)

        # Make sure the exit area is open
        maze[self.exit_y][self.exit_x] = 0
        maze[self.exit_y - 1][self.exit_x] = 0
        maze[self.exit_y][self.exit_x - 1] = 0

        return maze

    # ========================================================
    # DRAW MAZE  (Step 3)
    # ========================================================

    def draw_maze(self):
        self.canvas.delete("all")

        for y in range(self.maze_height):
            for x in range(self.maze_width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if self.maze[y][x] == 1:
                    # Wall
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="#252525",
                        outline="#444444"
                    )
                    self.canvas.create_rectangle(
                        x1 + 4, y1 + 4, x2 - 4, y2 - 4,
                        fill="#171717",
                        outline=""
                    )
                else:
                    # Floor
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="#080808",
                        outline="#111111"
                    )

        # Green exit
        ex = self.exit_x * self.cell_size
        ey = self.exit_y * self.cell_size

        self.canvas.create_rectangle(
            ex + 4, ey + 4,
            ex + self.cell_size - 4, ey + self.cell_size - 4,
            fill="#00ff66",
            outline="#00ffaa",
            width=2
        )
        self.canvas.create_rectangle(
            ex + 10, ey + 10,
            ex + 20, ey + 20,
            fill="#003300",
            outline=""
        )

        # Player
        px = self.player_x * self.cell_size
        py = self.player_y * self.cell_size

        self.canvas.create_rectangle(
            px + 5, py + 5,
            px + self.cell_size - 5, py + self.cell_size - 5,
            fill="#00aaff",
            outline="#66ddff",
            width=2
        )

        # Eyes
        self.canvas.create_rectangle(
            px + 10, py + 9, px + 13, py + 12,
            fill="white", outline=""
        )
        self.canvas.create_rectangle(
            px + 18, py + 9, px + 21, py + 12,
            fill="white", outline=""
        )

    # ========================================================
    # START MAZE  (Step 4)
    # ========================================================

    def start_maze(self):
        # Clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.maze_level += 1
        self.player_x = 1
        self.player_y = 1
        self.maze = self.generate_maze()

        # Title
        title = tk.Label(
            self.root,
            text="☠ PIXEL MAZE ☠",
            font=("Courier New", 28, "bold"),
            fg="#ff3333",
            bg="#111111"
        )
        title.pack(pady=10)

        # Instructions
        instructions = tk.Label(
            self.root,
            text="Use W A S D or ARROW KEYS to move • Find the green exit",
            font=("Courier New", 12),
            fg="white",
            bg="#111111"
        )
        instructions.pack(pady=5)

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # Draw the maze
        self.draw_maze()

        # Enable keyboard controls
        self.root.bind("<KeyPress>", self.move_player)
        self.root.focus_set()

    # ========================================================
    # MOVE PLAYER  (Step 5)
    # ========================================================

    def move_player(self, event):
        key = event.keysym.lower()

        dx = 0
        dy = 0

        if key in ("up", "w"):
            dy = -1
        elif key in ("down", "s"):
            dy = 1
        elif key in ("left", "a"):
            dx = -1
        elif key in ("right", "d"):
            dx = 1
        else:
            return

        new_x = self.player_x + dx
        new_y = self.player_y + dy

        # Stay inside the maze
        if not (0 <= new_x < self.maze_width and 0 <= new_y < self.maze_height):
            return

        # Hit a wall?
        if self.maze[new_y][new_x] == 1:
            return

        # Move the player
        self.player_x = new_x
        self.player_y = new_y
        self.draw_maze()

        # Check if player reached the exit
        if self.player_x == self.exit_x and self.player_y == self.exit_y:
            self.escape_maze()

    # ========================================================
    # ESCAPE MAZE  (Step 6)
    # ========================================================

    def escape_maze(self):
        # Unbind keys so they stop working
        self.root.unbind("<KeyPress>")

        # Clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(
            self.root,
            text="✓ MAZE ESCAPED!",
            font=("Courier New", 38, "bold"),
            fg="#00ff66",
            bg="#111111"
        )
        label.pack(pady=100)

        text = tk.Label(
            self.root,
            text="You found the exit!\n\nBack to the quiz...",
            font=("Courier New", 18),
            fg="white",
            bg="#111111"
        )
        text.pack()

        # Return to the quiz after a short delay
        self.root.after(1500, self.show_quiz)


# ============================================================
# START GAME
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()