#!/bin/sh

date

/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/afisha/parsing-films.py

/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/afisha/afisha-maxi.py
#/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/afisha/afisha-mori.py
/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/afisha/afisha-rublic.py

/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/afisha/afisha-dramakomi.py
/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/afisha/afisha-filarmonia.py
/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/afisha/afisha-komiopera.py

/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/afisha/convert_seans_to_events.py

date