




import tkinter as tk
from tkinter import messagebox
import requests
import html
import random

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quix App (API-based) By Raju Alaria")
        self.master.geometry("700x500")

        self.score = 0
        self.qn = 0
        self.questions = self.get_questions()

        self.question_label = tk.Label(master, text="", wraplength=550, font=("Helvetica", 16, "bold"),fg="navy", bg="#f0f8ff", justify="center",)
        self.question_label.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(master, text="", width=50, font=("Helvetica", 12), command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.display_question()

    def get_questions(self):
        url = "https://opentdb.com/api.php?amount=10&type=multiple"
        response = requests.get(url)
        data = response.json()

        questions = []
        for item in data['results']:
            question = html.unescape(item['question'])
            correct = html.unescape(item['correct_answer'])
            incorrect = [html.unescape(ans) for ans in item['incorrect_answers']]
            options = incorrect + [correct]
            random.shuffle(options)
            questions.append({
                'question': question,
                'options': options,
                'answer': correct
            })
        return questions

    def display_question(self):
        if self.qn < len(self.questions):
            current = self.questions[self.qn]
            self.question_label.config(text=f"Q{self.qn+1}: {current['question']}")
            for i, opt in enumerate(current['options']):
                self.buttons[i].config(text=opt)
        else:
            messagebox.showinfo("Quiz Finished", f"Your score: {self.score}/{len(self.questions)}")
            self.master.destroy()

    def check_answer(self, index):
        selected = self.buttons[index].cget("text")
        correct = self.questions[self.qn]['answer']
        if selected == correct:
            self.score += 1
        self.qn += 1
        self.display_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
