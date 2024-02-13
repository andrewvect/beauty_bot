from beauty_bot.app.app_tools.services import generate_key


def save_image_and_get_path(message, bot) -> str:
    photo = message.photo[-1]
    file_id = photo.file_id

    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    downloaded_file = bot.download_file(file_path)

    file_name = generate_key(7)

    with open(f'beauty_bot/app/photos/{file_name}.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    return file_name + '.jpg'