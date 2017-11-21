#!/bin/sh

date

/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/news/spyder-komiinform.py
# /home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/news/spyder-bnkomi.py
# /home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/news/spyder-komikz.py
# /home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/news/spyder-komionline.py

/home/spravka/projects/spravka11/env/bin/python3 /home/spravka/projects/spravka11/spravka11/parsing/news/import_db_into_db.py

date