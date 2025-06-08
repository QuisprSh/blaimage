# blaimage 🦈

THIS IS JUST SOMETHING I MADE ON A WHIM, PLEASE USE https://wamellow.com/
cause there bot is better and has more features and is installable on both guilds and user

a user-installable bot that adds `/blahaj`. use it to get a random blahaj image or see how many there are on the selected server.

## usage

```
/blahaj action:\[image|stats]
````

- `image`: gets a random blahaj pic 🦈
- `stats`: tells you how many blahaj pics there are

## install
1. **clone repo**
```bash
git clone https://github.com/QuisprSh/blaimage.git
```
2. **install requirements**
```bash
pip install -r requirements.txt
```
3. **rename sample.env to .env**
4. **fill out .env with needed info**
5. **run register.py**
6. **launch with uvicorn**
```bash
uvicorn main:app --port 3000
```
7. **use ngrok to tunnel**
```bash
ngrok http --url=<NGROK-STATIC-URL> 3000
```
8. **add your static url to interaction endpoint url**
```
<NGROK-STATIC-URL>/interactions
```
10. **set install options**
![image](https://github.com/user-attachments/assets/877ee646-1fe5-4188-b8ba-ea65f3c15a3b)
11. **add app to your account**
```
https://discord.com/oauth2/authorize?client_id=<APP_ID>&integration_type=1&scope=applications.commands
```
