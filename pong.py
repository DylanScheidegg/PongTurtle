import os
import random
import sys
import turtle
import winsound
import pygame
import webcolors


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


pygame.mixer.init()
anthem = resource_path("anthem.mp3")
pygame.mixer.music.load(anthem)
pygame.mixer.music.play(50, 0.0)

newWin = turtle.Screen()
newWin.title("Pong")
newWin.bgcolor("black")
width = 1280
height = 720
newWin.setup(width, height)
newWin.tracer(0)

# Player 1
player1 = turtle.Turtle()
player1.speed(0)
player1.shape("square")
player1.shapesize(stretch_wid=10, stretch_len=1)
player1.color("white")
player1.penup()
player1.goto(-width // 2 + 25, 0)

# Player 2
player2 = turtle.Turtle()
player2.speed(0)
player2.shape("square")
player2.shapesize(stretch_wid=10, stretch_len=1)
player2.color("white")
player2.penup()
player2.goto(width // 2 - 25, 0)

# Pong
pong = turtle.Turtle()
pong.speed(0)
pong.shape("circle")
pong.color("white")
pong.penup()
pong.goto(0, 0)
pong_x = -1
pong_y = 1
pong_fake = 100
pong_muliplier = 0.05


def player1_up():
    y = player1.ycor()
    if y < height / 2:
        y += 20
        player1.sety(y)
    else:
        player1.sety((height / 2) + 1)


def player1_down():
    y = player1.ycor()
    if y > -height / 2:
        y -= 20
        player1.sety(y)
    else:
        player1.sety((-height / 2) + 1)


def rand_pong_direction_x(x):
    rand = random.randint(0, 1)
    if rand == 0:
        x *= -1
    else:
        x *= 1
    return x


def rand_pong_direction_y(y):
    rand = random.randint(0, 1)
    if rand == 0:
        y *= 1
    else:
        y *= -1
    return y


# Initialize Scores
play1_score = 0
play2_score = 0

score = turtle.Turtle()
score.speed(0)
score.shape("square")
score.color("white")
score.penup()
score.hideturtle()
score.goto(0, height // 2 - 25)
score.write("Player A: 0  Player B: 0  Speed: 0.000 (W S to move)", align="center", font=("Courier", 12, "normal"))

speed = turtle.Turtle()
speed.speed(0)
speed.shape("square")
speed.color("white")
speed.penup()
speed.hideturtle()
speed.goto(0, height // 2 - 50)
speed.write("Speed: 0.000", align="center", font=("Courier", 10, "normal"))

# Player1 Movements
newWin.listen()
newWin.onkeypress(player1_up, "w")
newWin.onkeypress(player1_down, "s")

# Main game
time = 0
while True:
    time += 1

    # Player Score Checking to Quit the game
    if play1_score == 10 or play2_score == 10:
        print("Player1 Score: " + str(play1_score) + "\nPlayer2 Score: " + str(play2_score))
        quit()

    # Pong Y Borders
    if pong.ycor() >= height // 2 - 10:
        pong_y *= -1
    elif pong.ycor() <= -height // 2 + 20:
        pong_y *= -1

    # Pong X Borders
    if pong.xcor() >= width // 2:
        pong.goto(0, 0)
        play1_score += 1
        score.clear()
        score.write("Player 1: {}  Player 2: {}".
                    format(play1_score, play2_score), align="center", font=("Courier", 12, "normal"))
    elif pong.xcor() <= -width // 2:
        pong.goto(0, 0)
        play2_score += 1
        score.clear()
        score.write("Player 1: {}  Player 2: {}".
                    format(play1_score, play2_score), align="center", font=("Courier", 12, "normal"))

    # Update Player2 movements
    play2_y = player2.ycor()
    if play2_y < height // 2 or play2_y > -height // 2:
        player2.sety(pong_fake)
    elif play2_y > height:
        player2.sety(height - 1)
    elif play2_y < -height // 2:
        player2.sety(-height + 1)

    """
    play1_y = player1.ycor()
    if play1_y < height // 2 or play1_y > -height // 2:
        player1.sety(pong.ycor())
    elif play2_y > height:
        player1.sety(height - 1)
    elif play2_y < -height // 2:
        player1.sety(-height + 1)
    """

    # Checking if players and pong connected
    #  stretch of 5 means 5*20 and stretch of 1 means 1*20 means a jump in pixels by factor of 20
    #  [     ]
    #  [     ]
    #  [  *  ] original point
    #  [     ]
    #  [     ]
    if player1.xcor() - 10 <= pong.xcor() <= player1.xcor() + 10 and player1.ycor() - 100 <= pong.ycor() <= player1.\
            ycor() + 100:
        pong.setx(-width // 2 + 45)
        pong_x *= -1
        print(player1.xcor(), player1.ycor())
        winsound.PlaySound("Balloon.wav", winsound.SND_ASYNC)
    elif player2.xcor() - 10 <= pong.xcor() <= player2.xcor() + 10 and player2.ycor() - 100 <= pong.ycor() <= player2.\
            ycor() + 100:
        pong.setx(width // 2 - 45)
        pong_x *= -1
        print(player2.xcor(), player2.ycor())
        winsound.PlaySound("Balloon.wav", winsound.SND_ASYNC)

    if time % 1000 == 0:
        pong_muliplier += 0.05
        speed.clear()
        speed.write("Speed: {}".
                    format(pong_muliplier), align="center", font=("Courier", 10, "normal"))
    elif time % 150 == 0:
        pong_fake = pong.ycor()

    print(pong_muliplier)
    # Move pong
    pong.sety(pong.ycor() + pong_y * pong_muliplier)
    pong.setx(pong.xcor() + pong_x * pong_muliplier)

    score.color(webcolors.rgb_to_hex((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
    # Refresh Game
    newWin.update()
