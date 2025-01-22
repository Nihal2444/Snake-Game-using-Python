import tkinter as tk
import random
import os
from PIL import Image, ImageTk

class SnakeGame:
    def __init__(self, master, width=800, height=600):
        self.master = master
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        self.paused = False
        self.game_running = True
        self.move_x = 10
        self.move_y = 0
        self.snake_segments = [(100, 100), (90, 100), (80, 100)]
        self.snake = []
        self.food = None
        self.obstacles = []
        self.speed = 100
        self.level = 1
        self.score = 0
        self.start_button = None
        self.py_label = tk.Label(self.master, text="P      Y", fg="green", bg="black", font=("Arial", 42))
        self.on_label = tk.Label(self.master, text="O      N", fg="green", bg="black", font=("Arial", 42))
        self.py_label.place(relx=0.2, rely=0.3, anchor=tk.CENTER)
        self.on_label.place(relx=0.8, rely=0.3, anchor=tk.CENTER)
        self.credit_label = tk.Label(self.master, text="By ' N ' Games.com....", fg="light green", bg="black",
                                     font=("Arial", 24))
        self.credit_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        self.start_screen()

        # Load and display the snake image with "PY" and "ON" labels
        self.snake_image = Image.open(r"C:\Users\nihal\OneDrive\Desktop\image8.ico")
        self.snake_image = self.snake_image.resize((150, 150), Image.LANCZOS)
        self.snake_photo = ImageTk.PhotoImage(self.snake_image)
        self.snake_label = tk.Label(self.master, image=self.snake_photo, bg="black")
        self.snake_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    def start_screen(self):
        button_width = 10  # Adjust width as needed

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game, width=button_width)
        self.start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.exit_button = tk.Button(self.master, text="   EXIT   ", command=self.exit_game, width=button_width)
        self.exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    def start_game(self):
        self.canvas.delete("all")
        if self.credit_label:
            self.credit_label.destroy()
        if self.snake_label:
            self.snake_label.destroy()
        if self.py_label:
            self.py_label.destroy()
        if self.on_label:
            self.on_label.destroy()
        if self.exit_button:
            self.exit_button.destroy()
        self.create_snake()
        self.create_food()
        self.create_obstacles()
        self.update_score_display()
        self.master.bind("<Key>", self.change_direction)
        self.start_button.destroy()

    def create_snake(self):
        self.snake_segments = [(100, 100), (90, 100), (80, 100)]
        self.snake = []
        for segment in self.snake_segments:
            part = self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green")
            self.snake.append(part)
        self.move_snake()

    def create_food(self):
        x = random.randint(0, self.width - 10)
        y = random.randint(0, self.height - 10)
        x -= x % 10
        y -= y % 10
        self.food = self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red", tags="food")

    def create_obstacles(self):
        self.obstacles = []
        for _ in range(self.level * 5):
            x = random.randint(0, self.width - 10)
            y = random.randint(0, self.height - 10)
            x -= x % 10
            y -= y % 10
            obstacle = self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="gray", tags="obstacle")
            self.obstacles.append(obstacle)

    def move_snake(self):
        if self.paused or not self.game_running:
            return

        head_x, head_y = self.snake_segments[0]
        new_head = (head_x + self.move_x, head_y + self.move_y)

        if new_head[0] < 0:
            new_head = (self.width - 10, new_head[1])
        elif new_head[0] >= self.width:
            new_head = (0, new_head[1])
        elif new_head[1] < 0:
            new_head = (new_head[0], self.height - 10)
        elif new_head[1] >= self.height:
            new_head = (new_head[0], 0)

        self.snake_segments = [new_head] + self.snake_segments[:-1]

        for i, segment in enumerate(self.snake_segments):
            self.canvas.coords(self.snake[i], segment[0], segment[1], segment[0] + 10, segment[1] + 10)

        self.check_collision()

        self.master.after(self.speed, self.move_snake)

    def change_direction(self, event):
        key = event.keysym
        if key == "Left" and self.move_x == 0:
            self.move_x = -10
            self.move_y = 0
        elif key == "Right" and self.move_x == 0:
            self.move_x = 10
            self.move_y = 0
        elif key == "Up" and self.move_y == 0:
            self.move_x = 0
            self.move_y = -10
        elif key == "Down" and self.move_y == 0:
            self.move_x = 0
            self.move_y = 10
        elif key == "space":
            self.toggle_pause()

    def check_collision(self):
        head_coords = self.canvas.coords(self.snake[0])
        food_coords = self.canvas.coords("food")

        if head_coords == food_coords:
            self.score += 1
            self.update_score_display()
            self.canvas.delete("food")
            self.create_food()
            self.snake_segments.append(self.snake_segments[-1])
            part = self.canvas.create_rectangle(self.snake_segments[-1][0], self.snake_segments[-1][1],
                                                self.snake_segments[-1][0] + 10, self.snake_segments[-1][1] + 10,
                                                fill="green")
            self.snake.append(part)
            self.speed = max(50, 100 - self.score * 2)

            if self.score % 5 == 0:
                self.level += 1
                self.create_obstacles()


        if head_coords in [self.canvas.coords(segment) for segment in self.snake[1:]]:
            self.game_over()

        for obstacle in self.obstacles:
            if head_coords == self.canvas.coords(obstacle):
                self.game_over()


    def update_score_display(self):
        self.canvas.delete("score_text")
        score_text = f"Score: {self.score}  Level: {self.level}"
        self.canvas.create_text(10, 10, text=score_text, fill="white", anchor="nw", tags="score_text")

    def game_over(self):
        self.save_score()
        self.game_running = False
        self.canvas.delete("all")
        self.canvas.create_text(self.width / 2, self.height / 2, text="Game Over", fill="white", font=("Arial", 30))
        self.canvas.create_text(self.width / 2, (self.height / 2) + 40, text=f"Score: {self.score}", fill="white",
                                font=("Arial", 20))

        # Display the snake image with "PY" and "ON" labels
        self.snake_image = Image.open(r"C:\Users\nihal\OneDrive\Desktop\image8.ico")
        self.snake_image = self.snake_image.resize((150, 150), Image.LANCZOS)
        self.snake_photo = ImageTk.PhotoImage(self.snake_image)
        self.snake_label = tk.Label(self.master, image=self.snake_photo, bg="black")
        self.snake_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.show_scores_button()
        self.show_new_game_button()
        self.show_exit_button()

    def show_scores(self):

        scores = self.load_scores()
        top_scores = scores[:3]
        scores_text = "\n".join([f"{i + 1}. {score}" for i, score in enumerate(top_scores)])
        self.canvas.delete("all")
        self.canvas.create_text(self.width / 2, 50, text="High Scores", fill="white", font=("Arial", 30))
        self.canvas.create_text(self.width / 2, 150, text=scores_text, fill="white", font=("Arial", 20))
        self.show_back_button()




    def show_scores_button(self):

        scores_btn = tk.Button(self.master, text="Scores", command=self.show_scores)
        self.canvas.create_window(self.width / 2 - 70, (self.height / 2) + 120, window=scores_btn)

    def show_new_game_button(self):
        new_game_btn = tk.Button(self.master, text="New Game", command=self.new_game)
        self.canvas.create_window(self.width / 2 + 70, (self.height / 2) + 120, window=new_game_btn)

    def show_exit_button(self):
        exit_btn = tk.Button(self.master, text="Exit", command=self.exit_game)
        self.canvas.create_window(self.width / 2, (self.height / 2) + 180, window=exit_btn)

    def new_game(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Reset game state variables
        self.score = 0
        self.level = 1
        self.speed = 100
        self.game_running = True
       # self.
        # Remove unnecessary widgets if they exist
        if self.snake_label:
            self.snake_label.destroy()

        # Create new game elements
        self.create_snake()
        self.create_food()
        self.create_obstacles()
        self.update_score_display()

    def show_scores(self):
        scores = self.load_scores()
        top_scores = scores[:3]
        scores_text = "\n".join([f"{i + 1}. {score}" for i, score in enumerate(top_scores)])

        # Clear the canvas
        self.canvas.delete("all")

        # Calculate positions relative to the canvas size
        text_y = self.height // 2 + 3  # Adjust this value as needed to move text downwards

        # Display high scores text
        self.canvas.create_text(self.width / 2, text_y, text="High Scores", fill="white", font=("Arial", 30))

        # Display scores
        self.canvas.create_text(self.width / 2, text_y + 127, text=scores_text, fill="white", font=("Arial", 20))

        # Show back button
        self.show_back_button()

    def show_back_button(self):
        button_height = 50  # Adjust the height of the button as needed

        # Calculate the vertical position for the button at the bottom of the screen
        position_y = self.height - button_height - 20  # Adjust the offset as needed

        # Create the Back button
        back_btn = tk.Button(self.master, text="Back", command=self.game_over)
        self.canvas.create_window(self.width / 2, position_y, window=back_btn)

    def save_score(self):
        scores = self.load_scores()
        scores.append(self.score)
        scores = sorted(scores, reverse=True)[:10]
        with open("scores.txt", "w") as f:
            for score in scores:
                f.write(f"{score}\n")

    def load_scores(self):
        if os.path.exists("scores.txt"):
            with open("scores.txt", "r") as f:
                scores = [int(line.strip()) for line in f]
        else:
            scores = []
        return scores

    def exit_game(self):
        self.master.destroy()

    def toggle_pause(self):
        self.paused = not self.paused
        if not self.paused and self.game_running:
            self.move_snake()

def main():
    root = tk.Tk()
    root.title("Snake Game")
    game = SnakeGame(root)
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()

