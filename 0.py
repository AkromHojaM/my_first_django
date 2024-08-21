# image_ids1 = {

#     'anime1': 564,
#     'anime2': 565,
#     'anime3': 566}

# image_index = 0


@dp.callback_query(lambda cal: cal.data == 'anime2')
async def show_image1(call: types.CallbackQuery):
    global image_index1
    image_key1 = call.data
    if image_key1 in image_ids1:
        group_id = os.getenv('GROUP_ID')
        await call.bot.copy_message(
            chat_id=call.message.chat.id,
            from_chat_id=group_id,
            message_id=image_ids1[image_key1
],reply_markup=get_navigation_keyboard2()
        )
        await call.answer()  # Callback query'yi yanıtla


@dp.callback_query(lambda cal: cal.data in ['previouss', 'nextt'])
async def navigate_images(call: types.CallbackQuery):
    global image_index1
    if call.data == 'nextt':
        image_index1 = (image_index1 + 1) % len(image_ids1)
    elif call.data == 'previouss':
        image_index1 = (image_index1 - 1 + len(image_ids1)) % len(image_ids1)
        print(image_index1)

    image_key1 = list(image_ids1.keys())[image_index1]
    group_id = os.getenv('GROUP_ID')
    await call.bot.copy_message(
        chat_id=call.message.chat.id,
        from_chat_id=group_id,
        message_id=image_ids1[image_key1],
        reply_markup=get_navigation_keyboard2()
    )
    await call.answer()  # Callback query'yi yanıtla
