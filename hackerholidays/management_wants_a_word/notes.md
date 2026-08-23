# Day 14 - Management Wants a Word
## Room: <https://tryhackme.com/room/hh-managementwantsaword-6bf3cc41>

Hello Hackers!

Welcome to Day 14 of the TryHackMe Hacker Holidays 2026 writeups.

This final challenge involved investigating a large forensic archive and following the clues left behind on Vera’s machine.

The initial hints suggested that we needed to find several scattered artifacts and determine how they connected:

> `Hunt down the artifacts scattered across her machine and figure out how they fit together. Somewhere in that trail is a password she never meant to leave behind. Follow it, and it'll open a door to something she was keeping very quiet.`

> `Some things aren't as locked away as she thought`

Another clue mentioned that a browser could remember information without the user explicitly sharing it:

> `ok so apparently a browser will remember things for you that you never told anyone else 💀 not every hidden file needs a password cracker, some of them just need a really good memory also why did Patch tell me this version number 1.26.29 idk what it means :( #HackerHolidays`

The challenge contained a large ZIP file. After extracting it, we found several interesting files and notes.

The version number `1.26.29` pointed toward VeraCrypt. The name `VERA`crypt also appeared to reinforce this clue.

The main browser artefacts were located in:

```text
/TryHackMeHackerHolidays/Day14/management-wants-a-word-forensics-hh-day-14/KAPE/C/Users/vera/AppData/Local/Google/Chrome For Testing/User Data/Default
```

There was also a backup file in Vera’s Documents directory.

We first examined the files in:

```text
C/Windows/System32/config
```

Using the SAM, SYSTEM, and SECURITY registry hives, we ran:

```bash
impacket-secretsdump -sam SAM -system SYSTEM -security SECURITY LOCAL
```

The output revealed a default password:

```text
DefaultPassword (Unknown User):minivera
```

The dumped password was:

```text
minivera
```

The output also showed that Vera’s user account shared the same NTLM hash as the Administrator account, but the default password was the useful discovery for the next stage.

Next, we investigated the DPAPI files in:

```text
C/Users/vera/AppData/Roaming/Microsoft/Protect/S-1-5-21-2529683458-431225740-1723070931-1000
```

We used the discovered password to decrypt the DPAPI master key:

```bash
impacket-dpapi masterkey -file c90719ef-5b98-474e-b934-136d606a702a -sid S-1-5-21-2529683458-431225740-1723070931-1000
```

The master key was successfully decrypted using the user key.

This allowed us to decrypt Chrome’s saved passwords. We examined the Chrome Local State file at:

```text
C/Users/vera/AppData/Local/Google/Chrome For Testing/User Data/Local State
```

The file contained an encrypted key. We then examined the Chrome login database using SQLite:

```text
.tables
select hex(password_value) from logins
```

This returned an encrypted password value:

```text
763130C88A72A64F35F63E883EA0A7F64A6870E46B0BBB469A756EDA88B7E324C3E1C51015AA6FD8D65AC48961E1EA324CE1707807FEB3D7
```

After decrypting the saved Chrome password, we obtained:

```text
Wh4t1sV3raD0inG0nTh1sH0st
```

This password allowed us to open Vera’s VeraCrypt backup file.

We opened the backup using:

```bash
sudo cryptsetup open --type tcrypt --veracrypt "C/Users/vera/Documents/backup" veracontainer
```

We then created a mount directory and mounted the container as read-only:

```bash
sudo mkdir -p /mnt/veradata && sudo mount -o ro /dev/mapper/veracontainer /mnt/vera
```

After mounting the VeraCrypt container, we found a PDF file containing the flag.

The flag was:

> `THM{...}`

This was a really fun set of challenges, and I’ll see you guys again someday with something new.
Till then,

Happy Hacking!
