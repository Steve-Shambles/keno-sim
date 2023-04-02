# keno-sim
A simulation of the on-line casino game keno using Tkinter

keno Simulator V1
By Steve Shambles (c) April 2023

Source code is under MIT Licence.
This program is Freeware.

This program is a simulation of an online Keno game that I 
sometimes play for real money.

I wrote this to try out betting strategies 
and compare results to see how the online game matched up
since it claims to be 100% random.

I was dubious, but not so much now, also they have no need
to cheat as the odds are so far in their favour :-(


Instructions:

Keno is a very simple game. the player chooses the amount 
they want to bet, how many numbers to pick from 3 to 15 picks
from the grid of 80 numbers,
and then the computer picks out 20 random numbers from 1 to 80.

You want as many of your numbers matching with the computer picks
as possible to win a prize.

The payouts are listed in the right side panel in the game.


Step by Step:

Select your stake.
Click on 3 to 15 numbered boxes
or use the random drop-down menu
Select game speed
and then click "Play"

Click "New Game" or "Repeat Last Bet"
buttons to play another game

There is a "High Score" feature that saves your highest bank total
to your local drive so you always have a target to try and improve on.


This game is random. RTP is approximately 95%-96%
Steve Shambles.

For Python programmers:

Requirements:
Pip3 install sounddevice
pip3 install soundfile
pip3 install Pillow

I wrote this program on a Windows 7 PC using Python V3.67,
but I see no reason why it should not work on any Windows or
Linux machine, though they remain untested.

To make your own executable:
pip3 pyinstaller
then: 

pyinstaller  Keno_V1.py -n keno_v1 --windowed --onefile

change "Keno_V1.py" to whatever the source file you 
are using is named if different of course.


