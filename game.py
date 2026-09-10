import tkinter as tk
import random

prinr('test')
 
# ============================================================
# QUIZ + PIXEL MAZE GAME
# ============================================================
 
class QuizMazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Maze")
        self.root.geometry("900x700")
        self.root.configure(bg="#111111")
        self.root.resizable(False, False)
 self.score = 0
        self.question_number = 0
        self.maze_level = 0
 
        # ----------------------------------------------------
        # QUESTIONS
        # First 5 are easy, then they get harder. Following a tutorial on how to make questions randomized so code is half done and not functional yet
        # ----------------------------------------------------
        self.questions = [
            {
                "question": "What is 2 + 2?",
                "answers": ["3", "4", "5", "6"],
                "correct": "4"
                