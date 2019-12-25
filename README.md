# trading_bot

If you want to keep your systems clean, and easily make sure we have same python versions and library versions, use docker.
This isn't necessary, but makes it easier to avoid dependency/version problems. If you have the same version of python on your computer, the libraries will be the same versions so this probably isn't necessary.

1. Install docker desktop.
2. `docker pull sesank/trading_bot` --> downloads python3.7, TensorFlow, Pandas, BS4, etc.
3. `docker run --rm -v /path/to/project/directory:/home/ sesank/trading_bot:latest python /home/main.py`


<p> `-v` flag mounts host folders into container </p>
<p> You can make your own docker containers from existing ones if you want to try out different libraries </p>
