from beauty_bot.extantions import bot


def delete_previous_messages(func):
    def wrapped(*args, **kwargs):

        if hasattr(args[0], 'message'):
            message = args[0].message
        else:
            message = args[0]

        count = 0
        while True:
            try:
                bot.delete_message(message.chat.id, message.id - count)
                count += 1
            except Exception:
                break

        return func(*args, **kwargs)

    return wrapped
