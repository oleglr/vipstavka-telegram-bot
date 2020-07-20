from aiogram import types


keyboards = {

}

buttons = {

}


class UpdateKeyboard():

    def __init__(self, keyboards, buttons):
        """Инициализация словарей для клавиатур и кнопок"""
        
        self.keyboards = keyboards
        self.buttons = buttons
    
    def start_keyboard(self):
        """Создаем стартовую клавиатуру"""
        
        start_keyb = keyboards['start_keyboard'] = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        
        start_keyb.row("Я оплатил💰")
        start_keyb.row("Связь с оператором📲") 

        return start_keyb
    
    def admin_general_keyboard(self):
        """Создаем админ клавиатуру"""

        admin_keyb = keyboards['admin_keyboard'] = types.InlineKeyboardMarkup()
        
        admin_keyb.add(types.InlineKeyboardButton(text="Создать рассылку", callback_data="new_malling"))
        admin_keyb.add(types.InlineKeyboardButton(text="История действий", callback_data="action_history"))
        admin_keyb.add(types.InlineKeyboardButton(text="Добавить активным 1 день", callback_data="add_all_1_day"))

        return admin_keyb
    

    def add_days_button_for_user(self, user):
        """Создаем админ клавиатуру для добавления дней пользователю"""

        self.user = user

        add_days_keyboard = keyboards[f'add_days_{self.user}'] = types.InlineKeyboardMarkup(row_width=5)

        self.buttons[f'buttons_{self.user}'] = []

        for i in range(1, 31):
            self.buttons[f'buttons_{self.user}'].append(types.InlineKeyboardButton(text=str(i), callback_data=f"add_days_{self.user}_{str(i)}"))
        
        self.buttons[f"buttons_{self.user}"].append(types.InlineKeyboardButton(text="Отмена", callback_data=f"decline_{self.user}"))

        b = self.buttons[f"buttons_{self.user}"]
        
        add_days_keyboard.add(b[0], b[1], b[2], b[3], b[4])
        add_days_keyboard.add(b[5], b[6], b[7], b[8], b[9])
        add_days_keyboard.add(b[10], b[11], b[12], b[13], b[14])
        add_days_keyboard.add(b[15], b[16], b[17], b[18], b[19])
        add_days_keyboard.add(b[20], b[21], b[22], b[23], b[24])
        add_days_keyboard.add(b[25], b[26], b[27], b[28], b[29])
        add_days_keyboard.add(b[30])

        return add_days_keyboard

    
    def create_invite_link(self, user, link):
        """Создаем кнопку с ссылкой на закрытый канал"""

        self.user = user
        self.link = link

        link_keyb = keyboards[f"link_{self.user}"] = types.InlineKeyboardMarkup()
        link_keyb.add(types.InlineKeyboardButton(text="Перейти в закрытый канал", url = self.link))

        return link_keyb




