from utils import main_keybord
    
    # приветсвие
def greet_user(update, context):
    text = 'Привет, пользователь! Выбирай сайт'
    # print(text)
    update.message.reply_text(text, reply_markup=main_keybord())