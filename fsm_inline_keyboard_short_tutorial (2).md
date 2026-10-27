# FSM and Inline Keyboard in Aiogram

## 1. FSM

FSM means Finite State Machine.

FSM is used when the bot needs to receive information from the user in several steps.

Example:

```text
/add
    |
    v
Enter title
    |
    v
Enter description
    |
    v
Save task
```

Without FSM, the bot does not know whether the user's message is a title, description, date, or something else.

In aiogram, we create states like this:

```python
from aiogram.fsm.state import State, StatesGroup


class AddTask(StatesGroup):
    title = State()
    description = State()
```

`AddTask.title` means:

```text
The bot is waiting for the task title.
```

`AddTask.description` means:

```text
The bot is waiting for the task description.
```

We work with FSM using `FSMContext`.

Important methods:

```python
await state.set_state(...)
```

Changes the current state.

```python
await state.update_data(...)
```

Temporarily saves information.

```python
data = await state.get_data()
```

Gets previously saved information.

```python
await state.clear()
```

Finishes the FSM process and clears temporary data.

---

## 2. Inline Keyboard

An inline keyboard is a keyboard displayed under a Telegram message.

Example:

```text
Task: Learn Python

[ Complete ] [ Update ]
```

We create it using:

```python
InlineKeyboardMarkup
InlineKeyboardButton
```

Example:

```python
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Complete",
                callback_data="complete:5"
            )
        ]
    ]
)
```

`text` is what the user sees:

```text
Complete
```

`callback_data` is what the bot receives:

```text
complete:5
```

Here:

```text
complete = action
5 = task ID
```

Inline buttons are handled with:

```python
@router.callback_query(...)
```

not with:

```python
@router.message(...)
```

---

# One Complete Example

Project structure:

```text
project/
│
├── main.py
├── states.py
├── keyboards.py
└── handlers.py
```

---

## `states.py`

```python
from aiogram.fsm.state import State, StatesGroup


class AddTask(StatesGroup):
    title = State()
    description = State()
```

---

## `keyboards.py`

```python
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def task_keyboard(task_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Complete",
                    callback_data=f"complete:{task_id}"
                )
            ]
        ]
    )

    return keyboard
```

If:

```python
task_id = 7
```

the callback data becomes:

```text
complete:7
```

---

## `handlers.py`

```python
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import task_keyboard
from states import AddTask


router = Router()


@router.message(Command("add"))
async def add_handler(
    message: Message,
    state: FSMContext
):
    await state.set_state(
        AddTask.title
    )

    await message.answer(
        "Enter task title:"
    )


@router.message(AddTask.title)
async def title_handler(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        title=message.text
    )

    await state.set_state(
        AddTask.description
    )

    await message.answer(
        "Enter task description:"
    )


@router.message(AddTask.description)
async def description_handler(
    message: Message,
    state: FSMContext
):
    data = await state.get_data()

    title = data["title"]
    description = message.text

    await state.clear()

    await message.answer(
        f"Task created\n\n"
        f"Title: {title}\n"
        f"Description: {description}",
        reply_markup=task_keyboard(1)
    )


@router.callback_query(
    F.data.startswith("complete:")
)
async def complete_handler(
    callback: CallbackQuery
):
    parts = callback.data.split(":")

    task_id = parts[1]

    await callback.message.answer(
        f"Task {task_id} completed."
    )

    await callback.answer()
```

---

## `main.py`

```python
import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import router


load_dotenv()


bot = Bot(
    token=os.getenv("BOT_TOKEN")
)

dp = Dispatcher()


async def main():
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```

---

# How This Example Works

User sends:

```text
/add
```

Bot sets:

```python
AddTask.title
```

User sends:

```text
Learn Python
```

Bot saves:

```python
title = "Learn Python"
```

and changes state to:

```python
AddTask.description
```

User sends:

```text
Learn FSM
```

Bot gets the saved title, creates the task message, clears FSM, and shows:

```text
Task created

Title: Learn Python
Description: Learn FSM

[ Complete ]
```

When the user presses `Complete`, Telegram sends:

```text
complete:1
```

The callback handler gets:

```python
task_id = "1"
```

and processes that task.

The main idea is:

```text
FSM
=
remember conversation steps

Inline Keyboard
=
send button actions
```
