# Day 2 - Room 404
## Room: <https://tryhackme.com/room/hh-room404-804573bf>

Hello Hackers!

Welcome to Day 2 of the TryHackMe Hacker Holidays 2026 writeups.

This challenge involves enumerating a web server and recovering information from an exposed Git repository.

The instructions mention that port `8080` is open, so let’s begin by scanning the target.

```bash
nmap -p- 10.49.137.197
```

The scan confirms that port `8080` is available. Since this is a web service, we can enumerate its directories using a tool such as Gobuster:

```bash
gobuster dir -u http://10.49.137.197:8080 -w /usr/share/wordlists/dirb/common.txt
```

The enumeration reveals a `.git` directory.

An exposed `.git` directory can allow us to download the application’s Git repository and recover files that were not intended to be publicly accessible.

We can use `git-dumper` to reconstruct the repository locally:

```bash
git-dumper http://10.49.137.197:8080/.git ./git-dumped
```

After the repository has been downloaded, we can inspect its contents:

```bash
cd git-dumped
ls
```

The flag is stored in the `README` file:

```bash
cat README
```

This reveals the flag:

> `THM{...}`

The key lesson is that accidentally exposing `.git` can leak source code, commit history, configuration files, and sensitive information.

Happy Hacking!
