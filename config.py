from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

DB_NAME = env('DB_NAME')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')

ADMINS = ['398206038']
