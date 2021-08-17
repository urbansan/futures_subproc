## Shell multiprocess

A script which runs shell commands in parallel. Commands are being fed from a file.

Install:

```$: python3 -m pip install shell-multiprocess```

Run:

```
$: multiprocess -h
usage: multiprocess [-h] [-s] [-l] filename processes

Script which reads a file with shell commands and runs them in parallel
processes.

positional arguments:
  filename           Filename with commands
  processes          Amount of parallel processes

optional arguments:
  -h, --help         show this help message and exit
  -s, --soft-kill    Sends SIGINT signal to subprocesses instead of SIGKILL
                     during cleanup after CTRL-C
  -l, --log-to-file  Send multiprocess sumup to file with name
                     'multiprocess_{pid}.log'. Log is being update each time
                     an event occurs and can be viewed to monitor progress.
```

Create a command file:

```
$: cat > cmd.list
sleep 1 && sleep2 && echo finished_1_2
sleep 3 && echo finished_3  # finish with CTRL+D
```

Run it in parallel - both lines should finish at the same time:
```
multiprocess cmd.list 2
finished_3
finished_1_2
status      |        start        |         end         |       elapsed       | command
----------- | ------------------- | ------------------- | ------------------- | -------
done        | 2021-08-17 22:28:12 | 2021-08-17 22:28:15 |   0:00:03.003935    | sleep 1 && sleep 2 && echo finished_1_2
done        | 2021-08-17 22:28:12 | 2021-08-17 22:28:15 |   0:00:03.000876    | sleep 3 && echo finished_3
```
