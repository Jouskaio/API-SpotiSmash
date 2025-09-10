# API-SpotiSmash

Find your spotify soulmate using IA (project abandoned because of data storage issue)

For personal usage I kept this project to regularly clean my liked songs. 
It works by crawling every liked song I've got and see if they belong to another playlist. If not, they are added to a "Watch Later" playlist. It allows me to organize my music by playlist.
To run it, you need to create a .env file with your spotify credentials and make sure to run the /callback route (for spotify grants) before the /user/me/clean one.

