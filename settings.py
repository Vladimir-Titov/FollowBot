import envparse

envparse.env.read_envfile('.env')

TOKEN = envparse.env.str('TOKEN', default=None)
dsn = envparse.env.str('dsn', default=None)
ADMIN_ID = envparse.env.int('ADMIN_ID', default=None)
