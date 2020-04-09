# msah: mopidy-spotify authentication helper

A tool for managing your mopidy.conf spotify authentication automatically through a controlled browser instance.

## Gettings started

So you want to use msah yourself? Please go ahead. I promise nothing, but I believe this is how you get it up and running. If not, please do submit a bug report or an issue. We can surely work things out.

### Prequisities

First you are going to be needing the source files, so clone this repository.

```shell
$ git clone https://github.com/JanneSalokoski/msah.git
$ cd msah
```

Then you need some packages:
* python3 (no idea if python2 would also work, but I am going to assume no)
* pip (it probably comes with python, but you do need it)
* firefox (you need to have _firefox_, not for example firefox-developer-edition)
* geckodriver

These should be available from your package manager. On Arch you may run:

```shell
# pacman -S python3 pip firefox geckodriver
```

I also use some python libraries that you have to install:
* argparse
* selenium
* elevate

We installed pip to make this easy, just run:

```shell
$ pip install argparse selenium elevate
```

And you should be ready on to installing msah on your machine.


### Installing

Since everything is just python and a shell script, no compiling is needed. Just update config.py with your credentials and the correct path for your mopidy config file. It probably will be in /etc/mopidy/mopidy.conf, unless you are running mopidy from your user and not as a service.

Also make sure you have the rights to execute these scripts. Before trying to edit your mopidy.conf the script elevates its privileges to root, but for everything else we are running with your rights.

## Deployment

You can just run:

```shell
$ ./msah.sh
```

That should open up a browser window, automatically authenticate mopidy on spotify, ask for root password to gain access to mopidy.conf, updates your configuration and restart mopidy service.

I personally call _msah.sh_ from my window manager autostart, running it on alacritty (terminal) with -e flag to execute the command. You might not want to do that, but I think it's nice to get automatically authorized on every startup. You do you, I don't really care.

## Author

Janne Salokoski

## Licence

This software is licensed under the BSD License 2.0. See LICENSE.md for further details.

## Acknowledgments

Thanks for the people at mopidy, mopidy-spotify, spotify, selenium and firefox. Their hard work and dedication have produced these amazing tools for me. The only job left for me was to automate stringing together the work of others, and for that I am grateful. Thank you!
