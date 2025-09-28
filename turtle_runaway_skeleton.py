# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random, time

limit = 350
score = 0

def keep_inside(t):
    x, y = t.pos()
    if x > limit: t.setx(limit)
    if x < -limit: t.setx(-limit)
    if y > limit: t.sety(limit)
    if y < -limit: t.sety(-limit)

def update_time():
    global score
    elapsed = int(time.time() - start_time)

    if game.is_catched():
        score += 1
    time_label.config(text=f"시간: {elapsed}초")
    score_label.config(text=f"점수: {score}점")
    root.after(500, update_time)

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.score = 0
        self.start_time = 0
        self.score = 0

        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('black')
        self.runner.turtlesize(stretch_wid=2, stretch_len=2, outline=2)
        self.runner.speed(0)
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('green')
        self.chaser.turtlesize(stretch_wid=4, stretch_len=4, outline=4)
        self.chaser.speed(0)
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=1):
        self.drawer.clear()
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        is_catched = self.is_catched()
        self.drawer.penup()
        self.drawer.undo()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'')
        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=50, step_turn=90):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=20, step_turn=90):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 4)
        if mode <= 2:
            self.forward(self.step_move)
            keep_inside(self)
        elif mode == 3:
            self.left(self.step_turn)
        elif mode == 4:
            self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    time_label = tk.Label(root, font=("Arial", 16))
    time_label.pack()
    score_label = tk.Label(root, font=("Arial", 16))
    score_label.pack()
    start_time = time.time()

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    update_time()
    screen.mainloop()
