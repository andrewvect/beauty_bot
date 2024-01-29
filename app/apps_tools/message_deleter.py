import traceback

from beauty_bot.extantions import bot


def delete_previous_messages(func):
    def wrapped(*args, **kwargs):
        call = args[0]
        count = 0
        while True:
            try:
                bot.delete_message(call.message.chat.id, call.message.id - count)
                count += 1
            except Exception:
                break

        return func(*args, **kwargs)

    return wrapped
