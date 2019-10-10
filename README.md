# ownlittleworld
test task

**to run**
- `git glone`
- `docker-compose up -d`

**to check**
- navigate to localhost:8888, do some actions
- to schedule activity demo bot, enter docker container with backend app and execute `python manage.py createsuperuser`
- then acquire token at `/accounts/login/`
- send a post request to  `/demo/bot/` with specified config
- navigate to `/posts/` and see the results of fake activity
