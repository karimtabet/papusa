# Notes on working and developing Papusa

## Getting pdb to run with docker.

The options for `stdin_open` & `tty` have been set in the web image in the docker-compose.yml.
This allows us to attach to the container using the command `docker attach papusa_web`.
From this we can see live output from gunicorn plus if the project drops in to
a debugger shell, we can access it here.

note: the -t 3600 flag is passed to gunicorn so it takes longer to time out.
Without it we would loose the pdb shell quickly when the connection timed out.

