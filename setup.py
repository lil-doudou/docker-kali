import os
from shutil import which
import subprocess
from colorama import Fore
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

class Loader:
    def __init__(self, desc="Loading...", end="", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

def bashrc_config():
    print()

def docker_install():
    with Loader((Fore.LIGHTYELLOW_EX + "[..] ")+(Fore.RESET + "Docker installation")):
        subprocess.run(['apt-get', 'update'], stdout=open(os.devnull,'wb'))
        subprocess.run(['apt-get', 'install', '-y', 'docker.io'], stdout=open(os.devnull,'wb'))
    print((Fore.LIGHTGREEN_EX + "[+] ")+(Fore.RESET + "Docker.io is installed"))

def docker_image_gen():
    with Loader((Fore.LIGHTYELLOW_EX + "[..]")+(Fore.RESET + "Kali docker image generation")):
        subprocess.run(['docker', 'build', '-t', 'docker_kali', './dockerfile/'], stdout=open(os.devnull))
    print((Fore.LIGHTGREEN_EX + "[+] ")+(Fore.RESET + "Kali Docker image is created"))


def env_check():
    if os.getuid() != 0:
        print((Fore.LIGHTRED_EX + "[!] ERROR : run the setup with root privilege"))
        exit(1)
    if which("docker") is None:
        print((Fore.LIGHTBLUE_EX + "[info] ")+(Fore.RESET + "Docker is not installed"))
        print((Fore.LIGHTYELLOW_EX + "[?] ")+(Fore.RESET + "Do you want to install Docker with this script ? [y/n]"))
        validation = input("> ")
        if validation == "y":
            docker_install()
            pass
        elif validation == "n":
            print(Fore.LIGHTRED_EX + "[x] This script need Docker.io. Install Docker.io before use Kali in Docker.")
            exit(2)
        else:
            print((Fore.LIGHTRED_EX + "[!] Syntax error")+ Fore.RESET)
            exit(255)
    print((Fore.LIGHTGREEN_EX + "[+] ")+(Fore.RESET + "Environement check done"))

def env_install():
    with Loader((Fore.LIGHTYELLOW_EX + "[..] ")+(Fore.RESET + "Install Docker Kali")):
        subprocess.run(['docker', 'pull', 'kalilinux/kali-rolling'], stdout=open(os.devnull,'wb'))
    print((Fore.LIGHTGREEN_EX + "[+] ")+(Fore.RESET + "Docker kali is downloaded"))

    print((Fore.LIGHTYELLOW_EX + "[?] ")+(Fore.RESET + "Do you want to configure aliases in bashrc ? [y/n]"))
    validation = input("> ")
    if validation == "y":
        bashrc_config()
        pass
    elif validation == "n":
        print((Fore.LIGHTRED_EX + "[x] ")+ (Fore.RESET + "aliases is not configured in bashrc"))
        pass
    else:
        print((Fore.LIGHTRED_EX + "[!] Syntax error")+ Fore.RESET)
        exit(255)




def main():
    print((Fore.LIGHTGREEN_EX + ">>> Start Install <<<")+Fore.RESET)
    env_check()
    docker_image_gen()
    env_install()


main()