from aiogram import Bot, Dispatcher, F
from aiogram.types import message, KeyboardButton, ReplyKeyboardMarkup,Message
from aiogram.filters import Command, CommandStart
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os
import asyncio
from service import *

load_dotenv()





tocen = os.getenv("TOKEN")


bot = Bot(token=tocen)
dp = Dispatcher()


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Add task")],
        [KeyboardButton(text="Reat task")],
        [KeyboardButton(text="Update tusk")],
        [KeyboardButton(text="Dalete task")],
    ],
    resize_keyboard=True,
)






@dp.message(CommandStart())
async def start_bot(message : Message):
    await message.answer(f"""
Привает {message.from_user.full_name} етот бот бро task meneger
Ты можеш создат свой таск обновит и удалит его с чего начнем?
""", reply_markup=main_kb)




@dp.message(Command("help"))
async def help_bot(message : Message):
    await message.answer(f"""
Привает {message.from_user.full_name} что привело тебе ко мне

Если хочеш создат свой таск пиши /add_task
Если хочеш прочитат свой таск пиши /read_task
Если хочеш изменит свой таск пиши /update_task
Если хочеш удалитъ свой таск пиши /delete_task
""")




class Add_task(StatesGroup):
    get_title = State()
    get_caption = State()
    get_due_day = State()



class Read_task(StatesGroup):
    get_task_id = State()



class update_task(StatesGroup):
    get_task_id = State()
    get_title = State()
    get_caption = State()
    get_due_day = State()




class dalete_task(StatesGroup):
    get_task_id = State()










@dp.message(F.text == "Add task")
@dp.message(Command("add_task"))
async def create(message: Message, state : FSMContext):
    await message.answer("Введите имя вашего таска")
    await state.set_state(Add_task.get_title)



@dp.message(Add_task.get_title)
async def get_titlee(messaga : Message , state : FSMContext):
    await state.update_data(title = messaga.text)
    await messaga.answer("Введите описание задачи: ")
    await state.set_state(Add_task.get_caption)



@dp.message(Add_task.get_caption)
async def add_captionn(message : Message, state : FSMContext):
    await state.update_data(caption = message.text)
    await message.answer("Введите дату выполнения: ")
    await state.set_state(Add_task.get_due_day)






@dp.message(Add_task.get_due_day)
async def add_due_date(mesage : Message , state : FSMContext):
    await state.update_data(due_date = mesage.text)
    data = await state.get_data()
    await create_task_by_id(data["title"], data["caption"], data["due_date"], mesage.from_user.id)
    await mesage.answer("Ваш таск успешно создан!!!")
    await state.clear()




    
@dp.message(F.text == "Reat task")
@dp.message(Command("read_task"))
async def read_your_task(message : Message, state : FSMContext):
    await message.answer("Введите id таска каторого хотите прочитатъ!!!")
    await state.set_state(Read_task.get_task_id)



@dp.message(Read_task.get_task_id)
async def show_me_my_task(message : Message, state : FSMContext):
    await state.update_data(task_id = int(message.text))
    data = await state.get_data()
    my_task = await for_for_read(data["task_id"], message.from_user.id)
    b1 = ""
    for i in my_task:
        b1 = f"""
===== Id {i["id"]} =====
Title: {i["title"]}
Caption: {i["caption"]}
Duration date: {i["due_date"]}
"""
    await message.answer(b1)
    await state.clear()














@dp.message(F.text == "Update tusk")
@dp.message(Command("update_task"))
async def change_task(message : Message, state : FSMContext):
    await message.answer("Введите id таска каторого хотите изменитъ: ")
    await state.set_state(update_task.get_task_id)




@dp.message(update_task.get_task_id)
async def get_task_id_for_update(message : Message , state : FSMContext):
    await state.update_data(task_id = int(message.text))
    await message.answer("Введите ваш title")
    await state.set_state(update_task.get_title)





@dp.message(update_task.get_title)
async def get_titile_for_uodating(message : Message, state : FSMContext):
    await state.update_data(title = message.text)
    await message.answer("Введите ваш caption: ")
    await state.set_state(update_task.get_caption)


@dp.message(update_task.get_caption)
async def get_caption_fro_updationg(message : Message, state : FSMContext):
    await state.update_data(caption = message.text)
    await message.answer("Введите ваш dueratipn date: ")
    await state.set_state(update_task.get_due_day)


@dp.message(update_task.get_due_day)
async def get_due_day_for_updation(message : Message, state : FSMContext):
    await state.update_data(due_date = message.text)
    data = await state.get_data()
    await update_table_by_id(data["title"], data["caption"], data["due_date"], data["task_id"], message.from_user.id)
    await message.answer("Task update sucessful")
    await state.clear()











@dp.message(F.text == "Dalete task")
@dp.message(Command("delete_task"))
async def drop_table_cascade(message : Message , state : FSMContext):
    await message.answer("Введите айди таска каторого хотите удалитъ: ")
    await state.set_state(dalete_task.get_task_id)



@dp.message(dalete_task.get_task_id)
async def for_for_fro_delete(message : Message , state : FSMContext):
    await state.update_data(task_id = int(message.text))
    data = await state.get_data()
    await drop_task(data["task_id"], message.from_user.id)
    await message.answer("Task delete sucessful")
    await state.clear()














async def  main():
    await create_table()
    print("Bot started!!!")
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())