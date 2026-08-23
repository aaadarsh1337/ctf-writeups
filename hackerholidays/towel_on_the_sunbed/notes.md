# Day 8 - Towel on the Sunbed
## Room: <https://tryhackme.com/room/hh-towelonthesunbed-61271709>

Hello Hackers!

Welcome to Day 8 of the TryHackMe Hacker Holidays 2026 writeups.

The initial hints suggest that the application has a time-based check, but the clock is not the only protection in place:

> `The app disagrees, politely, once every 24 hours. Somewhere between his request and the server's clock, there's a gap wide enough to walk a whale through.`

> `bro really thinks the clock is the only thing checking him`

During the initial reconnaissance, we try to create an account using:

```text
guest:guest123
```

The application reports that the username is already taken, confirming that `guest` is an existing user.

We create another account using:

```text
guest123:guest123
```

Inspecting the JavaScript source code and reviewing the hints reveals an API endpoint:

> `/dashboard/api/me`

The session ID can be URL decoded to:

> `s:skYb365MDbbq61daNdLz58uXnlC-CYvT.KursacNrnLBveu+edLpw+4GMN6Z/C+GDRSHWfj+J8uY`

Reading the hints again reveals:

> `3 Requests at a time --> 150 points --> Vault unlocked`

The JavaScript shows that the vault status is checked through the `/api/me` endpoint.

We intercept the claim request and send it to Burp Suite Repeater. Duplicate the request twice so that there are three identical requests in total.

Group the three requests together and send them in parallel. Then turn off interception.

The three requests are processed together before the application’s defence mechanism can prevent the duplicate claims. This allows three rewards to be claimed at once, increasing the balance to 150 points.

The vault is now unlocked and contains the flag:

> `THM{...}`

Happy Hacking!
