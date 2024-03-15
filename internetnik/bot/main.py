from config import bot_load_config
config = bot_load_config('.env')

bot_token = config.tg_bot.token         # Сохраняем токен в переменную bot_token
superadmin = config.tg_bot.admin_ids[0]   # Сохраняем ID админа в переменную superadmin

