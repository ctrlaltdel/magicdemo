# Magic Demo

Give shell demos with style.

This is based on an original idea from Damian Conway's [Presentation Aikido](http://damian.conway.org/Courses/PresAikido.html).

# Usage

Create a shell script with the command you want to run and use the `#!./magicdemo.py` shebang.

It will listen to key presses and fake keyboard input. Use <TAB> to complete the current line and <ENTER> to run the command.

Ctrl-c will get you out of the current script.

# Bugs

1. An error is displayed at startup (and then hidden by running `clear`).

```
bash: cannot set terminal process group (-1): Inappropriate ioctl for device
bash: no job control in this shell
```