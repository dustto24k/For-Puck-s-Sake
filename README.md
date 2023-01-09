<div align ="center">

# For Puck's Sake

### Project 4: Interactive Drawing & Animation

[@dustto24k](https://github.com/dustto24k)'s personal final proj of
'MAS2011_WINTER' (2022.12.22 - 2023.1.11.)

</div>

## Description

### <i>Air Hockey... but it's Pinball</i>
Keep your pin-puck from falling into holes, using a mouse-operated striker. Meanwhile, you might consider hitting your pin-puck with other red pucks, so you can beat your own highscores from previous plays. But be careful, everytime a puck gets hit, it gets faster and you might miss your next strike! btw the title... doesn't mean anything in specific.
- Every time your pin-puck collide with other pucks, score is raised. Default value of 3, but it multiplies twice every 10 seconds. So the more you survive, the higher score you could get.
- Or you can choose to get more collisions in small amount of time, that's one part of strategy.
- Using walls can be a helpful strategy as well, as they reduce the pucks' speed when it collides into it.

### Features

Simple Mouse-only control

- It's even lesser than 4 arrow keys -- control only using mouse.

Arcade-like Sound Effects

- Game starts with an 'insert coin' sound effect, to give an arcade vibe.
- Every time the pin-puck collides with other pucks (and score raises), a pachinko-like sound is made. Somewhat similiar to how the pinball machines originally sound like.
- When it's a Game Over, jackpot sound effect plays. No other reasons, just the vibe u know.
- BGM: Pila Pala Paradise (no idea what that means, but sure sounds like arcade game BGMs.)

Show Final Score & Time Survived + Highscore Leaderboard

- Records time right after game has started, and ends when game overs. Shows the time survived, right away at Game Over screen.
- On the initial screen, highscores from previous plays are shown in high-to-low order.

## DevLog

### Checklist

- [x] Simple Mouse-only control
- [x] Neat Background + Object Image
- [x] Arcade-like Sound Effects
- [x] Show Final Score & Time Survived
- [x] Highscore Leaderboard
- [x] Offers Replay
- [x] No Framedrops
- [x] No Collision Bugs
