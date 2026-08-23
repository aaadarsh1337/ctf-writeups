# Day 4 - Packed Light
## Room: <https://tryhackme.com/room/hh-packedlight-02e5330c>

Hello Hackers!

Welcome to Day 4 of the TryHackMe Hacker Holidays 2026 writeups.

This challenge is a network forensics investigation involving a packet capture and a covert data-exfiltration channel.

Opening the capture in Wireshark, we can inspect the HTTP traffic and notice a suspicious request for

Following the HTTP stream reveals a Python script that behaves like a keylogger. The script records keystrokes and sends them to a remote server through HTTP requests.

The captured keystrokes are hidden inside a cookie named:

> `hotel_sess_state`

The cookie values are Base64 encoded and XOR encrypted. The attached script can be used to extract the cookie values from the capture, decode them, and reconstruct the original message.

The traffic can be isolated in Wireshark using:

```text
ip.addr == 34.41.103.191 && http && http.request.method == "GET"
```

The attached script processes each cookie individually, reverses the Base64 encoding and XOR encryption, and joins the recovered characters in the correct order.

Running the attached script reveals the flag:

> `THM{...}`

The main lesson is that attackers can hide stolen data inside normal-looking HTTP headers and cookies. Unusual request timing, suspicious downloaded scripts, and very short cookie values can help identify this type of covert channel.

Happy Hacking!
