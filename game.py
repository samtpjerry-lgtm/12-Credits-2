import tkinter as tk
import random
import threading
from collections import deque

# Try to import winsound (only works on Windows)
try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False


class QuizGame:
    def __init__(self, root):
        self.root = root

        # ====================================================
        # WINDOW SETTINGS
        # ====================================================
        self.root.title("The Quiz That Should Not Be")
        self.root.geometry("900x700")
        self.root.configure(bg="#050505")
        self.root.resizable(False, False)

        # ====================================================
        # GAME VARIABLES
        # ====================================================
        self.score = 0
        self.question_number = 0

        # ====================================================
        # MAZE VARIABLES
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

        # Monster
        self.monster_x = 0
        self.monster_y = 0
        self.monster_job = None

        # ====================================================
        # QUESTIONS
        # ====================================================
        self.questions = [
            {"question": "What is 2 + 2?", "answers": ["3", "4", "5", "6"], "correct": "4"},
            {"question": "What planet do we live on?", "answers": ["Mars", "Earth", "Venus", "Jupiter"], "correct": "Earth"},
            {"question": "How many days are in a week?", "answers": ["5", "6", "7", "8"], "correct": "7"},
            {"question": "What color do you get by mixing red and blue?", "answers": ["Green", "Orange", "Purple", "Yellow"], "correct": "Purple"},
            {"question": "What is 10 × 5?", "answers": ["15", "50", "55", "100"], "correct": "50"},
            {"question": "What is the square root of 144?", "answers": ["10", "11", "12", "14"], "correct": "12"},
            {"question": "Which element has the chemical symbol 'Au'?", "answers": ["Silver", "Gold", "Aluminium", "Argon"], "correct": "Gold"},
            {"question": "What is 15% of 200?", "answers": ["20", "25", "30", "35"], "correct": "30"},
            {"question": "Which country has the largest population?", "answers": ["India", "USA", "Brazil", "Japan"], "correct": "India"},
            {"question": "What is the binary representation of decimal 10?", "answers": ["1001", "1010", "1100", "1110"], "correct": "1010"},
            {"question": "If f(x) = x² - 3x + 2, what is f(4)?", "answers": ["4", "5", "6", "8"], "correct": "6"},
            {"question": "Which scientist formulated the three laws of planetary motion?", "answers": ["Isaac Newton", "Johannes Kepler", "Galileo Galilei", "Albert Einstein"], "correct": "Johannes Kepler"},
            {"question": "What is the derivative of x³ + 2x² - 5x?", "answers": ["3x² + 4x - 5", "3x² + 2x - 5", "x² + 4x - 5", "3x³ + 4x² - 5"], "correct": "3x² + 4x - 5"},
            {"question": "Which data structure uses LIFO (Last In, First Out)?", "answers": ["Queue", "Stack", "Tree", "Graph"], "correct": "Stack"},
            {"question": "What is the time complexity of binary search on a sorted array?", "answers": ["O(n)", "O(n²)", "O(log n)", "O(1)"], "correct": "O(log n)"},
            {"question": "What is the determinant of [[3, 2], [1, 4]]?", "answers": ["8", "10", "12", "14"], "correct": "10"},
            {"question": "In special relativity, what remains invariant between inertial reference frames?", "answers": ["Time", "Length", "Spacetime interval", "Kinetic energy"], "correct": "Spacetime interval"},
            {"question": "Which algorithm has an average-case time complexity of O(n log n)?", "answers": ["Bubble sort", "Insertion sort", "Merge sort", "Linear search"], "correct": "Merge sort"},
            {"question": "If a fair six-sided die is rolled twice, what is the probability of getting a sum of 7?", "answers": ["1/6", "1/8", "1/12", "1/18"], "correct": "1/6"},
            {"question": "What is the integral of 2x from x = 0 to x = 3?", "answers": ["6", "9", "12", "18"], "correct": "9"}
        ]

        self.show_quiz()

    # ========================================================
    # SOUND EFFECTS (safe version)
    # ========================================================

    def play_sound(self, frequency, duration):
        if not HAS_SOUND:
            return
        def _play():
            try:
                winsound.Beep(frequency, duration)
            except:
                pass
        threading.Thread(target=_play, daemon=True).start()

    def sound_wrong(self):
        self.play_sound(180, 400)
        self.root.after(450, lambda: self.play_sound(120, 600))

    def sound_maze_enter(self):
        self.play_sound(100, 700)

    def sound_escape(self):
        self.play_sound(280, 300)
        self.root.after(320, lambda: self.play_sound(360, 400))

    def sound_correct(self):
        self.play_sound(320, 180)

    def sound_caught(self):
        self.play_sound(90, 800)
        self.root.after(850, lambda: self.play_sound(60, 1000))

    # ========================================================
    # SHOW QUIZ
    # ========================================================

    def show_quiz(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        question = self.questions[self.question_number]

        title = tk.Label(
            self.root,
            text="☠ THE QUIZ THAT SHOULD NOT BE ☠",
            font=("Courier New", 26, "bold"),
            fg="#8b0000",
            bg="#050505"
        )
        title.pack(pady=25)

        status = tk.Label(
            self.root,
            text=f"Question {self.question_number + 1}/{len(self.questions)}     Souls: {self.score}",
            font=("Courier New", 14),
            fg="#aa4444",
            bg="#050505"
        )
        status.pack()

        question_label = tk.Label(
            self.root,
            text=question["question"],
            font=("Courier New", 18, "bold"),
            fg="#cccccc",
            bg="#050505",
            wraplength=780,
            justify="center"
        )
        question_label.pack(pady=45)

        answers = question["answers"].copy()
        random.shuffle(answers)

        for answer in answers:
            button = tk.Button(
                self.root,
                text=answer,
                font=("Courier New", 15, "bold"),
                fg="#dddddd",
                bg="#1a0000",
                activebackground="#5c0000",
                activeforeground="#ffaaaa",
                width=28,
                height=2,
                relief="flat",
                bd=0,
                command=lambda selected=answer: self.check_answer(selected)
            )
            button.pack(pady=7)

    # ========================================================
    # CHECK ANSWER
    # ========================================================

    def check_answer(self, selected_answer):
        question = self.questions[self.question_number]

        if selected_answer == question["correct"]:
            self.sound_correct()
            self.score += 1
            self.question_number += 1

            if self.question_number < len(self.questions):
                self.show_quiz()
            else:
                self.show_results()
        else:
            self.sound_wrong()
            self.show_wrong()

    # ========================================================
    # SHOW WRONG
    # ========================================================

    def show_wrong(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(
            self.root,
            text="✗ YOU HAVE FAILED ✗",
            font=("Courier New", 36, "bold"),
            fg="#ff0000",
            bg="#050505"
        )
        label.pack(pady=50)

        message = tk.Label(
            self.root,
            text="THE LABYRINTH CLAIMS ANOTHER...",
            font=("Courier New", 18, "bold"),
            fg="#aa2222",
            bg="#050505"
        )
        message.pack()

        message2 = tk.Label(
            self.root,
            text="Something is hunting you now...",
            font=("Courier New", 15),
            fg="#666666",
            bg="#050505"
        )
        message2.pack(pady=25)

        self.root.after(1800, self.start_maze)

    # ========================================================
    # SHOW RESULTS
    # ========================================================

    def show_results(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.root,
            text="☠ THE QUIZ IS OVER ☠",
            font=("Courier New", 30, "bold"),
            fg="#8b0000",
            bg="#050505"
        )
        title.pack(pady=70)

        score_label = tk.Label(
            self.root,
            text=f"Souls collected: {self.score}/{len(self.questions)}",
            font=("Courier New", 22, "bold"),
            fg="#cccccc",
            bg="#050505"
        )
        score_label.pack(pady=20)

        restart_button = tk.Button(
            self.root,
            text="TRY AGAIN",
            font=("Courier New", 15, "bold"),
            fg="#dddddd",
            bg="#1a0000",
            activebackground="#5c0000",
            activeforeground="#ffaaaa",
            width=18,
            height=2,
            relief="flat",
            command=self.restart_game
        )
        restart_button.pack(pady=25)

        quit_button = tk.Button(
            self.root,
            text="LEAVE THIS PLACE",
            font=("Courier New", 15, "bold"),
            fg="#dddddd",
            bg="#1a0000",
            activebackground="#5c0000",
            activeforeground="#ffaaaa",
            width=18,
            height=2,
            relief="flat",
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
    # MAZE GENERATION (with multiple paths)
    # ========================================================

    def generate_maze(self):
        maze = [[1 for _ in range(self.maze_width)] for _ in range(self.maze_height)]

        def carve(x, y):
            maze[y][x] = 0
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 1 <= nx < self.maze_width - 1 and 1 <= ny < self.maze_height - 1 and maze[ny][nx] == 1:
                    maze[y + dy // 2][x + dx // 2] = 0
                    carve(nx, ny)

        carve(1, 1)

        # Open the exit area
        maze[self.exit_y][self.exit_x] = 0
        maze[self.exit_y - 1][self.exit_x] = 0
        maze[self.exit_y][self.exit_x - 1] = 0

        # Add extra paths so there are multiple routes
        for _ in range(18):
            x = random.randint(1, self.maze_width - 2)
            y = random.randint(1, self.maze_height - 2)
            if maze[y][x] == 1:
                maze[y][x] = 0

        return maze

    # ========================================================
    # DRAW MAZE
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
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#1a0505", outline="#2a0a0a")
                    self.canvas.create_rectangle(x1 + 4, y1 + 4, x2 - 4, y2 - 4, fill="#0f0303", outline="")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#080000", outline="#0c0000")

        # Exit
        ex = self.exit_x * self.cell_size
        ey = self.exit_y * self.cell_size
        self.canvas.create_rectangle(ex + 3, ey + 3, ex + self.cell_size - 3, ey + self.cell_size - 3,
                                     fill="#003300", outline="#00aa44", width=2)
        self.canvas.create_rectangle(ex + 9, ey + 9, ex + 21, ey + 21, fill="#001a00", outline="")

        # Player
        px = self.player_x * self.cell_size
        py = self.player_y * self.cell_size
        self.canvas.create_rectangle(px + 5, py + 5, px + self.cell_size - 5, py + self.cell_size - 5,
                                     fill="#440000", outline="#ff2222", width=2)
        self.canvas.create_rectangle(px + 9, py + 9, px + 13, py + 13, fill="#ff5555", outline="")
        self.canvas.create_rectangle(px + 17, py + 9, px + 21, py + 13, fill="#ff5555", outline="")

        # Monster
        mx = self.monster_x * self.cell_size
        my = self.monster_y * self.cell_size
        self.canvas.create_rectangle(mx + 3, my + 3, mx + self.cell_size - 3, my + self.cell_size - 3,
                                     fill="#110000", outline="#660000", width=2)
        self.canvas.create_rectangle(mx + 8, my + 8, mx + 13, my + 13, fill="#ff0000", outline="")
        self.canvas.create_rectangle(mx + 17, my + 8, mx + 22, my + 13, fill="#ff0000", outline="")

    # ========================================================
    # START MAZE
    # ========================================================

    def start_maze(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.sound_maze_enter()

        self.maze_level += 1
        self.player_x = 1
        self.player_y = 1
        self.maze = self.generate_maze()

        # Place monster far away
        self.monster_x = self.maze_width - 3
        self.monster_y = self.maze_height - 3
        while self.maze[self.monster_y][self.monster_x] == 1:
            self.monster_x = random.randint(2, self.maze_width - 3)
            self.monster_y = random.randint(2, self.maze_height - 3)

        title = tk.Label(
            self.root,
            text="☠ THE LABYRINTH ☠",
            font=("Courier New", 26, "bold"),
            fg="#8b0000",
            bg="#050505"
        )
        title.pack(pady=10)

        instructions = tk.Label(
            self.root,
            text="W A S D or ARROWS • It knows the way to you...",
            font=("Courier New", 12),
            fg="#aa4444",
            bg="#050505"
        )
        instructions.pack(pady=5)

        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#000000",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        self.draw_maze()
        self.root.bind("<KeyPress>", self.move_player)
        self.root.focus_set()

        self.schedule_monster()

    # ========================================================
    # SMART MONSTER (BFS)
    # ========================================================

    def find_next_step(self):
        start = (self.monster_x, self.monster_y)
        goal = (self.player_x, self.player_y)

        if start == goal:
            return start

        queue = deque([start])
        came_from = {start: None}
        visited = {start}

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            current = queue.popleft()
            if current == goal:
                break

            cx, cy = current
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < self.maze_width and 0 <= ny < self.maze_height and
                        self.maze[ny][nx] == 0 and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    came_from[(nx, ny)] = current
                    queue.append((nx, ny))

        if goal not in came_from:
            return start

        # Reconstruct path
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
            if current is None:
                break

        if path:
            return path[-1]
        return start

    def schedule_monster(self):
        delay = max(160, 650 - (self.maze_level * 85))
        self.monster_job = self.root.after(delay, self.move_monster)

    def move_monster(self):
        if self.monster_job is None:
            return

        next_pos = self.find_next_step()
        self.monster_x, self.monster_y = next_pos
        self.draw_maze()

        if self.monster_x == self.player_x and self.monster_y == self.player_y:
            self.caught_by_monster()
            return

        self.schedule_monster()

    def stop_monster(self):
        if self.monster_job is not None:
            self.root.after_cancel(self.monster_job)
            self.monster_job = None

    def caught_by_monster(self):
        self.stop_monster()
        self.root.unbind("<KeyPress>")
        self.sound_caught()

        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(
            self.root,
            text="IT CAUGHT YOU",
            font=("Courier New", 36, "bold"),
            fg="#ff0000",
            bg="#050505"
        )
        label.pack(pady=80)

        text = tk.Label(
            self.root,
            text="The labyrinth will not let you go so easily...\n\nTry again.",
            font=("Courier New", 16),
            fg="#aa4444",
            bg="#050505"
        )
        text.pack(pady=20)

        self.root.after(2200, self.start_maze)

    # ========================================================
    # MOVE PLAYER
    # ========================================================

    def move_player(self, event):
        key = event.keysym.lower()
        dx = dy = 0

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

        if not (0 <= new_x < self.maze_width and 0 <= new_y < self.maze_height):
            return
        if self.maze[new_y][new_x] == 1:
            return

        self.player_x = new_x
        self.player_y = new_y
        self.draw_maze()

        if self.monster_x == self.player_x and self.monster_y == self.player_y:
            self.caught_by_monster()
            return

        if self.player_x == self.exit_x and self.player_y == self.exit_y:
            self.escape_maze()

    # ========================================================
    # ESCAPE MAZE
    # ========================================================

    def escape_maze(self):
        self.stop_monster()
        self.root.unbind("<KeyPress>")
        self.sound_escape()

        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(
            self.root,
            text="YOU ESCAPED... FOR NOW",
            font=("Courier New", 28, "bold"),
            fg="#00aa44",
            bg="#050505"
        )
        label.pack(pady=80)

        text = tk.Label(
            self.root,
            text="The labyrinth releases its grip.\n\nBack to the questions...",
            font=("Courier New", 16),
            fg="#888888",
            bg="#050505"
        )
        text.pack(pady=20)

        self.root.after(1800, self.show_quiz)


# ============================================================
# START GAME
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()