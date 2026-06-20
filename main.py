import customtkinter as ctk
from tkinter import messagebox
from words import WORDS
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class HangmanGame:

    def __init__(self, root):

        self.root = root
        self.root.title("Cyber Hangman")
        self.root.geometry("1100x800")
        self.root.configure(fg_color="#0B1020")

        self.score = 0

        self.title_label = ctk.CTkLabel(
            root,
            text="⚔️ CYBER HANGMAN ⚔️",
            font=("Arial", 34, "bold"),
            text_color="#00FFFF"
        )
        self.title_label.pack(pady=15)

        self.score_label = ctk.CTkLabel(
            root,
            text="🏆 Score : 0",
            font=("Arial", 22, "bold"),
            text_color="#00FF99"
        )
        self.score_label.pack()

        self.timer_label = ctk.CTkLabel(
            root,
            text="⏳ 60",
            font=("Arial", 22, "bold"),
            text_color="#FFD700"
        )
        self.timer_label.pack(pady=5)

        self.difficulty = ctk.StringVar(value="Easy")

        self.level_menu = ctk.CTkOptionMenu(
            root,
            values=["Easy", "Medium", "Hard"],
            variable=self.difficulty,
            command=self.change_level
        )
        self.level_menu.pack(pady=10)

        self.canvas = ctk.CTkCanvas(
            root,
            width=320,
            height=300,
            bg="#111827",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        self.word_label = ctk.CTkLabel(
            root,
            text="",
            font=("Consolas", 40, "bold"),
            text_color="white"
        )
        self.word_label.pack(pady=15)

        self.attempt_label = ctk.CTkLabel(
            root,
            text="❤️ Lives Left : 6",
            font=("Arial", 22, "bold")
        )
        self.attempt_label.pack()

        self.keyboard_frame = ctk.CTkFrame(
            root,
            fg_color="#151C32"
        )
        self.keyboard_frame.pack(pady=15)

        self.restart_btn = ctk.CTkButton(
            root,
            text="🔄 Restart Game",
            command=self.restart_game,
            height=45,
            corner_radius=12
        )
        self.restart_btn.pack(pady=15)

        self.create_keyboard()

        self.root.bind("<Key>", self.keyboard_input)

        self.animate_title()

        self.restart_game()

    def animate_title(self):

        colors = [
            "#00FFFF",
            "#00FF99",
            "#FFD700",
            "#FF66CC",
            "#FFFFFF"
        ]

        current = self.title_label.cget("text_color")

        try:
            idx = colors.index(current)
            idx = (idx + 1) % len(colors)
        except:
            idx = 0

        self.title_label.configure(
            text_color=colors[idx]
        )

        self.root.after(
            300,
            self.animate_title
        )

    def create_keyboard(self):

        self.buttons = {}

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        row = 0
        col = 0

        for letter in letters:

            btn = ctk.CTkButton(
                self.keyboard_frame,
                text=letter,
                width=55,
                height=45,
                corner_radius=12,
                fg_color="#1E3A8A",
                hover_color="#2563EB",
                font=("Arial", 16, "bold"),
                command=lambda l=letter:
                self.guess_letter(l)
            )

            btn.grid(
                row=row,
                column=col,
                padx=4,
                pady=4
            )

            self.buttons[letter] = btn

            col += 1

            if col == 7:
                col = 0
                row += 1

    def keyboard_input(self, event):

        letter = event.char.upper()

        if letter.isalpha():

            if letter in self.buttons:

                if self.buttons[
                    letter
                ].cget("state") != "disabled":

                    self.guess_letter(letter)

    def change_level(self, value):
        self.restart_game()

    def restart_game(self):

        self.word = random.choice(
            WORDS[self.difficulty.get()]
        ).upper()

        self.guessed = []

        self.wrong = 0

        self.max_wrong = 6

        self.time_left = 60

        for btn in self.buttons.values():
            btn.configure(state="normal")

        self.draw_hangman()

        self.update_word()

        self.update_attempts()

        self.update_timer()

    def update_timer(self):

        self.timer_label.configure(
            text=f"⏳ {self.time_left}"
        )

        if self.time_left > 0:

            self.time_left -= 1

            self.timer_job = self.root.after(
                1000,
                self.update_timer
            )

        else:

            messagebox.showerror(
                "Time Up",
                f"⏳ Time Over!\nWord was {self.word}"
            )

            self.restart_game()

    def update_word(self):

        display = ""

        for ch in self.word:

            if ch in self.guessed:
                display += ch + " "
            else:
                display += "_ "

        self.word_label.configure(
            text=display
        )

    def update_attempts(self):

        left = self.max_wrong - self.wrong

        if left >= 4:
            color = "#00FF99"
        elif left >= 2:
            color = "#FFD700"
        else:
            color = "#FF4444"

        self.attempt_label.configure(
            text=f"❤️ Lives Left : {left}",
            text_color=color
        )

    def guess_letter(self, letter):

        self.buttons[
            letter
        ].configure(
            state="disabled"
        )

        if letter in self.word:

            self.guessed.append(letter)

        else:

            self.wrong += 1

            self.draw_hangman()

        self.update_word()

        self.update_attempts()

        self.check_game()

    def draw_hangman(self):

        self.canvas.delete("all")

        self.canvas.create_line(
            50,250,220,250,
            fill="white",
            width=4
        )

        self.canvas.create_line(
            100,250,100,40,
            fill="white",
            width=4
        )

        self.canvas.create_line(
            100,40,200,40,
            fill="white",
            width=4
        )

        self.canvas.create_line(
            200,40,200,70,
            fill="white",
            width=4
        )

        if self.wrong >= 1:
            self.canvas.create_oval(
                175,70,225,120,
                outline="#FF4444",
                width=4
            )

        if self.wrong >= 2:
            self.canvas.create_line(
                200,120,200,190,
                fill="#FF4444",
                width=4
            )

        if self.wrong >= 3:
            self.canvas.create_line(
                200,140,160,170,
                fill="#FF4444",
                width=4
            )

        if self.wrong >= 4:
            self.canvas.create_line(
                200,140,240,170,
                fill="#FF4444",
                width=4
            )

        if self.wrong >= 5:
            self.canvas.create_line(
                200,190,170,230,
                fill="#FF4444",
                width=4
            )

        if self.wrong >= 6:
            self.canvas.create_line(
                200,190,230,230,
                fill="#FF4444",
                width=4
            )

    def check_game(self):

        won = True

        for ch in self.word:

            if ch not in self.guessed:
                won = False

        if won:

            try:
                self.root.after_cancel(
                    self.timer_job
                )
            except:
                pass

            self.score += 10

            self.score_label.configure(
                text=f"🏆 Score : {self.score}"
            )

            self.word_label.configure(
                text="🏆 YOU WIN 🏆",
                text_color="#00FF99"
            )

            messagebox.showinfo(
                "Winner",
                f"🎉 Correct!\nWord: {self.word}"
            )

            self.restart_game()

        elif self.wrong >= self.max_wrong:

            try:
                self.root.after_cancel(
                    self.timer_job
                )
            except:
                pass

            self.word_label.configure(
                text="💀 GAME OVER 💀",
                text_color="#FF4444"
            )

            messagebox.showerror(
                "Game Over",
                f"Word was: {self.word}"
            )

            self.restart_game()


root = ctk.CTk()

app = HangmanGame(root)

root.mainloop()
