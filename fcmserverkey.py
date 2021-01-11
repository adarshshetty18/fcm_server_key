#!/usr/bin/python3
import subprocess
import requests
import json
import os
import sys
import traceback
from shutil import which
from colorama import Fore

url = 'https://fcm.googleapis.com/fcm/send'
body = {"registration_ids": ["ABC"]}
headers = {"content-type": 'application/json'}


# Checking If apktool is installed
def check_apktool():
    try:
        if which("apktool"):
            return True
        else:
            return False
    except Exception as e:
        print(Fore.RED + f"[!] Error in checking apktool: {e}")


# Decompiling the apk
def decompile_apk(apk_file):
    try:
        print(Fore.BLUE + f"[+] Decompiling {apk_file}!")
        os.popen(f"apktool d {apk_file}").read()
        print(Fore.BLUE + "[+] Apk decompiled!")
        return apk.split(".")[0]
    except Exception as e:
        print(Fore.RED + f"[!] Error in decompiling apk: {e}")


# Extracting the keys using both regex
def extract_keys(_out_dir):
    try:
        output1 = subprocess.getoutput(f'grep -ProIR "AIzaSy[0-9A-Za-z_-]{{33}}" {_out_dir}')
        output2 = subprocess.getoutput(f'grep -ProIR "AAAA[A-Za-z0-9_-]{{7}}:[A-Za-z0-9_-]{{140}}" {_out_dir}')

        res = []
        if output1:
            res1 = output1.splitlines()
            res.extend(res1)
        if output2:
            res2 = output2.splitlines()
            res.extend(res2)

        if not res:
            print(Fore.RED + "[-] No tokens found")
            exit()

        keys = [i.split(":")[1] for i in res]
        print(Fore.BLUE + f"[+] Found some tokens: {', '.join(keys)}")
        return list(set(keys))
    except Exception as e:
        print(Fore.RED + f"[!] Error in extracting keys: {e}")


# Validating the server keys
def validate_keys(key):
    try:
        headers["Authorization"] = f"key={key}"
        r = requests.post(url, data=json.dumps(body), headers=headers)
        if r.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(Fore.RED + f"[!] Error in validating keys: {e}")


if __name__ == "__main__":
    try:
        if not check_apktool():
            print(Fore.RED + "[!] Install apktool for decompiling the apk!")
            exit()
        apk = sys.argv[1]
        out_dir = decompile_apk(apk)
        server_keys = extract_keys(out_dir)
        for server_key in server_keys:
            if validate_keys(server_key):
                print(Fore.GREEN + f"[+] {server_key} is a valid server key")
            else:
                print(Fore.RED + f"[-] {server_key} is not a valid server key")
        print(Fore.BLUE + f"[+] Finished!")
    except:
        print(traceback.format_exc())
