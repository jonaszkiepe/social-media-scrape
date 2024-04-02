from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep

XPATHS = {
    "cookie": "/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]",
    "email": '//*[@id="loginForm"]/div/div[1]/div/label/input',
    "password": '//*[@id="loginForm"]/div/div[2]/div/label/input[1]',
    "sign_in": '//*[@id="loginForm"]/div/div[3]',
    "profile": '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a/div',
    "following_count": '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span',
    "account": '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span',
    "reset": '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/h1/div',
    "time": '/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[1]/li/div/div/div[2]/div[2]/span/time',
    "post": '//div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]/div/div[1]/div[1]',
    "image": '//div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div//img',
    "description": '//div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[1]/li/div/div/div[2]/div[1]/h1'
}

options = ChromeOptions()
options.add_experimental_option("detach", True)
chrome = Chrome(options=options)


def main():
    chrome.get("https://instagram.com")

    log_in()

    posts = []

    try:
        posts = get_posts()
    except FileNotFoundError:
        names = get_accounts()
        with open("./accounts/instagram.txt", "w") as f:
            f.writelines(names)
        posts = get_posts()
    except Exception as e:
        raise e
    finally:
        for post in posts:
            with open(f"./accounts/posts/{post["name"]}.txt", "w") as f:
                f.write("img: " + post["img"] + "\n\n")
                if "description" in post:
                    f.write("description: " + post["description"] + "\n\n")
                f.write("\n")

    chrome.quit()


def find(xpath):
    return chrome.find_element(By.XPATH, xpath)


def get_posts():
    posts = []
    with open("./accounts/instagram.txt", "r") as f:
        names = f.readlines()
        for name in names:
            link = f"https://instagram.com/{name}"
            chrome.get(link)
            sleep(7)
            for i in range(1, 4):
                find(XPATHS["post"][:-2] + str(i) + "]").click()
                new_post = {
                        "name": name,
                        "img": find(XPATHS["image"]).get_attribute("src")
                        }
                try:
                    new_post["description"] = find(XPATHS["description"]).text
                except:
                    print("no description")
                posts.append(new_post)
                sleep(3)
                chrome.back()
                sleep(3)
    return posts


def log_in():

    try:
        with open("./private/instagram_credentials.txt", "r") as f:
            credentials = f.readlines()
    except FileNotFoundError:
        raise Exception("create credentials file (readme)")

    sleep(8)
    find(XPATHS["cookie"]).click() 
    sleep(3)
    find(XPATHS["email"]).send_keys(credentials[0])
    find(XPATHS["password"]).send_keys(credentials[1])
    sleep(1)
    find(XPATHS["sign_in"]).click()
    sleep(8)


def get_accounts():
    find("profile").click()
    sleep(8)
    account_count = find(XPATHS["following_count"])
    account_count.click()
    sleep(5)
    names = []
    for i in range(1, int(account_count.text) + 1):
        names.append(chrome.find_element(By.XPATH, XPATHS["account"][:-55] + str(i) + XPATHS["account"][-55:]).text + "\n")
    return names

main()
