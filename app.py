import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

class FlashcardQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quiz Game")
        self.root.geometry("800x500")
        self.root.configure(bg="#2b2b2b")

  
        
        self.database_name = "quiz_game.db"
        self.current_field = None
        self.current_questions = []
        self.current_question = None
        self.score = 0
        self.user_name = ""
        self.user_email = ""
        self.create_signup_screen()

    def fetch_questions(self, field):
        fields = {
          'gk': 'gk_questions',
          'grammer': 'grammer_questions',
          'sports': 'sport_questions',
          'math': 'math_questions',
          'poetry': 'poetry_questions',
          'technology': 'technology_questions'
        }
      
        table_name = fields.get(field)
        conn = sqlite3.connect('app_data.sqlite')
        cursor = conn.cursor()
        cursor.execute(f"SELECT question_text, answer, option1, option2, option3, option4 FROM {table_name}")
        questions = cursor.fetchall()
        conn.close()
        # self.total_q = len(questions)
        return questions

    def create_signup_screen(self):
        """Create a signup screen for user details."""
        self.clear_screen()

        signup_frame = tk.Frame(self.root, bg="#3a3a3a", padx=20, pady=20, relief="groove", bd=5)
        signup_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(signup_frame, text="Sign Up", font=("Arial", 28, "bold"), bg="#3a3a3a", fg="#ffffff").pack(pady=10)
        tk.Label(signup_frame, text="Enter your name:", font=("Arial", 18), bg="#3a3a3a", fg="#ffffff").pack(pady=5)
        self.name_entry = tk.Entry(signup_frame, font=("Arial", 16), width=50)
        self.name_entry.pack(pady=5)

        tk.Label(signup_frame, text="Enter your email:", font=("Arial", 18), bg="#3a3a3a", fg="#ffffff").pack(pady=5)
        self.email_entry = tk.Entry(signup_frame, font=("Arial", 16), width=50)
        self.email_entry.pack(pady=5)

        tk.Button(
            signup_frame,
            text="Submit",
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
            width=15,
            command=self.save_user_info,
        ).pack(pady=20)

    def save_user_info(self):
        """Save user info and go to the home screen."""
        self.user_name = self.name_entry.get().strip()
        self.user_email = self.email_entry.get().strip()

        if not self.user_name or not self.user_email:
            messagebox.showerror("Error", "Please fill out all fields!")
        else:
            conn = sqlite3.connect('app_data.sqlite')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (user_name,user_gmail) VALUES (?, ?)", (self.user_name, self.user_email))
            conn.commit()
            conn.close()
            self.create_home_screen()

    def create_home_screen(self):
        """Create the home screen where users select the quiz field."""
        self.clear_screen()

        home_frame = tk.Frame(self.root, bg="#3a3a3a", padx=10, pady=10, relief="groove", bd=5)
        home_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(home_frame, text=f"Welcome, {self.user_name}!", font=("Arial", 24, "bold"), bg="#3a3a3a", fg="#ffffff").grid(row=0, column=0, columnspan=3, pady=20)

        tk.Label(home_frame, text="Choose a Field:", font=("Arial", 16), bg="#3a3a3a", fg="#ffffff").grid(row=1, column=0, columnspan=3, pady=10)

        fields = ["GK", "Grammer", "Sports", "Math", "Poetry", "Technology"]

        for i, field in enumerate(fields):
            row = (i // 3) + 2
            column = i % 3

            tk.Button(
                home_frame,
                text=field,
                font=("Arial", 14),
                bg="#4CAF50",
                fg="white",
                width=15,
                height=2,
                command=lambda f=field.lower(): self.start_quiz(f),
            ).grid(row=row, column=column, padx=10, pady=10)

    def start_quiz(self, field):
        """Start the quiz for the selected field."""
        self.current_field = field
        self.current_questions = self.fetch_questions(field)
        self.score = 0
        self.ask_question()

    def ask_question(self):
        """Display a question for the user to answer."""
        self.clear_screen()

        question_frame = tk.Frame(self.root, bg="#3a3a3a", padx=50, pady=50, relief="groove", bd=8)
        question_frame.place(relx=0.5, rely=0.5, anchor="center")

        if len(self.current_questions) == 0:  # No questions left
            self.show_results()
            return

        question_data = random.choice(self.current_questions)
        self.current_questions.remove(question_data)

        self.current_question = {
            "question": question_data[0],
            "answer": question_data[1],
            "options": question_data[2:]
        }

        tk.Label(question_frame, text=f"Field: {self.current_field}", font=("Arial", 16), bg="#3a3a3a", fg="white").pack(pady=10)
        tk.Label(question_frame, text=f"Score: {self.score}", font=("Arial", 14), bg="#3a3a3a", fg="white").pack(pady=5)
        tk.Label(question_frame, text=self.current_question["question"], font=("Arial", 14), wraplength=500, bg="#3a3a3a", fg="white").pack(pady=20)

        self.selected_option = tk.StringVar(value="")
        for option in self.current_question["options"]:
            tk.Radiobutton(
                question_frame,
                text=option,
                variable=self.selected_option,
                value=option,
                font=("Arial", 14),
                bg="#3a3a3a",
                fg="#ffffff",
                selectcolor="black",
            ).pack(anchor="w", padx=20, pady=5)

        self.timer_label = tk.Label(question_frame, text="Time Left: 30s", font=("Arial", 14), bg="#3a3a3a", fg="white")
        self.timer_label.pack(pady=10)

        self.time_left = 30  # Reset the timer for this question
        self.update_timer()

        tk.Button(
            question_frame,
            text="Submit Answer",
            font=("Arial", 14),
            bg="green",
            fg="white",
            width=15,
            command=self.check_answer,
        ).pack(pady=10)

    def update_timer(self):
        """Update the countdown timer."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            self.ask_question()  # Proceed with the next question after time runs out

    def check_answer(self):
        """Check if the selected answer is correct and move to the next question."""
        user_answer = self.selected_option.get()

        if not user_answer:
            messagebox.showwarning("No Answer", "Please select an option before proceeding.")
            return

        correct_answer = self.current_question["answer"]

        if user_answer == correct_answer:
            self.score += 1

        self.ask_question()

    def show_results(self):
        """Display the final result after the quiz."""
        self.clear_screen()

        result_frame = tk.Frame(self.root, bg="#3a3a3a", padx=35, pady=35, relief="groove", bd=5)
        result_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(result_frame, text="Quiz Complete!", font=("Arial", 18, "bold"), bg="#3a3a3a", fg="#ffffff").pack(pady=10)
        tk.Label(result_frame, text=f"Your Final Score: {self.score}", font=("Arial", 16), bg="#3a3a3a", fg="#ffffff").pack(pady=20)

        tk.Button(
            result_frame,
            text="Back to Home",
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
            width=15,
            command=self.create_home_screen,
        ).pack(pady=20)

    def clear_screen(self):
        """Clear the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardQuizApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

