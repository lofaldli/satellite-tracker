# satellite-tracker

a simple satellite tracker inspired by [gpredict][1] written in python (2.7)

![screenshot](./images/screenshot.png "screenshot")

it uses NORAD two line elements (TLE) from [celestrack.com][2] 
and [python-sgp4][3] to predict satellite positions. 

[pygame][4] is used to display the map and [arrow][5] is used for time keeping

to run:

        python -m tracker

## installation

        sudo apt install python-pygame
        pip install -r requirements.txt

## TODO

- replace pygame with qt for gui
- 3d view
- keep looking up
	
[1]: http://gpredict.oz9aec.net/
[2]: http://celestrak.com/SpaceTrack/
[3]: https://pypi.python.org/pypi/sgp4/
[4]: http://pygame.org
[5]: https://github.com/crsmithdev/arrow

