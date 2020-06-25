"""
This is a detailed example using almost every command of the API
"""


import telebot
from telebot import types


import os
import os.path

from StyleTransfer import *
from FileLock import *

from DeERace import *


TOKEN = ''

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands. And working bot mode',
    'changeWorkMode'    : 'Change work mode. If default mode = Style Transfer',
    'deleteStyleImage'    : 'Clear style image. After this command you need upload new image',
    'showStyleImagesGallery'    : 'Show default style images. Just forward it to me',
    'showFaceImagesGallery'    : 'Show default face images. Just forward it to me',
    'showStartGuide'    : 'Show start guide',
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('Mickey', 'Minnie')

imageSelectBotMode = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelectBotMode.add('Style Transfer', 'DeERace mode')


hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard



#//////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////<Style Transfer>//////////////////////////////////////////////
def delete_style_photo(message):
    project_dir_path = "/tmp/TeleBotProject/files_folder/deerace/"
    user_dir_path = project_dir_path + str(message.from_user.id) + "/"

    if os.path.isfile(user_dir_path + "style_path.txt") == True:
        os.remove(user_dir_path + "style_path.txt")

def is_we_have_style_photo(message):
    project_dir_path = "/tmp/TeleBotProject/files_folder/deerace/"
    user_dir_path = project_dir_path + str(message.from_user.id) + "/"

    if os.path.isfile(user_dir_path + "style_path.txt") == True:
        return True
    return False


def make_style_transfer(message):
    project_dir_path = "/tmp/TeleBotProject/files_folder/deerace/"
    user_dir_path = project_dir_path + str(message.from_user.id) + "/"
    try:
        if os.path.isdir(project_dir_path) == False:
            mode = 0o755
            os.makedirs(project_dir_path, mode)

        if os.path.isdir(user_dir_path) == False:
            mode = 0o755
            os.makedirs(user_dir_path, mode) # dicrectory for current user

    except OSError:
        print("Creation of the directory %s failed" % user_dir_path)
    else:
        print("Successfully created the directory %s" % user_dir_path)

    print(message.photo[-1])

    try:
        cid = message.chat.id

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        is_content_photo = False
        downloaded_file_path = ''
        if os.path.isfile(user_dir_path + "style_path.txt") == False:
            downloaded_file_path = user_dir_path + "style_" + message.photo[-1].file_id + ".jfif"
        else:
            downloaded_file_path = user_dir_path + "content_" + message.photo[-1].file_id + ".jfif"
            is_content_photo = True

        print("downloaded_file_path = ", downloaded_file_path)
        with open(downloaded_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

            if is_content_photo == True:
                style_image_file_path = "" # path to style photo
                style_path_file_handler = open(user_dir_path + "style_path.txt", "r")
                style_image_file_path = style_path_file_handler.readline().strip()

                ##############################################################
                #### Better create with exception throw, but i'm so lazy :(####
                if style_image_file_path == None or len(style_image_file_path) == 0:
                    bot.reply_to(message, ":ERROR: Problem with STYLE photo.\n" +
                                          "Please use command /deleteStyleImage and upload STYLE photo again")
                    return
                elif os.path.isfile(style_image_file_path) == False:
                    bot.reply_to(message, ":ERROR: Can't find file with style image path.\n" +
                                 "Please use command /deleteStyleImage and upload STYLE photo again")
                    return
                #### Better create with exception throw, but i'm so lazy :(####
                ##############################################################


                bot.reply_to(message,
                             "*CONTENT PHOTO GETTED*\n\n" +
                             "I get CONTENT PHOTO, now wait, i make image and send it to you\n\n" +
                             "*MAKE STEP->* Wait i make stylize and send photo to you ",
                             parse_mode='Markdown')

                #bot.reply_to(message, "I get CONTENT PHOTO, now wait, i make image and send it to you")
                # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
                bot.send_chat_action(message.chat.id, 'typing')


                protected_file_path = os.path.join(project_dir_path, "lock_file.tmp")
                print("Protecting file: {}".format(protected_file_path))
                file_lock_handlers = FileLock(protected_file_path)

                with file_lock_handlers:
                    with open(protected_file_path, "a") as file_handler:
                        #object_style_transfer_facade = StyleTransferFacade(style_image_path=user_dir_path + "style.jfif",
                        #                                                   content_image_path=downloaded_file_path)
                        object_style_transfer_facade = StyleTransferFacade(style_image_path=style_image_file_path,
                                                                           content_image_path=downloaded_file_path)


                        object_style_transfer_facade.transfer_style(out_image_path=user_dir_path + "out_image.jpg")
                        del object_style_transfer_facade

                        bot.send_photo(message.chat.id, open(user_dir_path + "out_image.jpg", 'rb'),
                                       reply_markup=hideBoard,
                                       reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent
                        print("bot.send_photo")
                        file_handler.flush()
            else:
                with open(user_dir_path + "style_path.txt", 'w') as style_path_file_handler:
                    style_path_file_handler.write(downloaded_file_path)
                bot.reply_to(message,
                             "*STYLE PHOTO GETTED*\n\n" +
                             "I get STYLE photo, now i need CONTENT PHOTO\n\n" +
                             "*MAKE STEP->*Please send me one more photo, witch i will stylize",
                             parse_mode='Markdown')


            #bot.reply_to(message, "WTF is this?\nhttps://www.youtube.com/watch?v=78_W7-3oJD8")
            print("File uploaded path = ", downloaded_file_path)
    except Exception as e:
        bot.reply_to(message, e)
#/////////////////////////////////////////</Style Transfer>////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////




#//////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////<DeERace>////////////////////////////////////////////////////
def make_photo_deerace(message):
    project_dir_path = "/tmp/TeleBotProject/files_folder/deerace/"
    user_dir_path = project_dir_path + str(message.from_user.id) + "/"
    try:
        if os.path.isdir(project_dir_path) == False:
            mode = 0o755
            os.makedirs(project_dir_path, mode)

        if os.path.isdir(user_dir_path) == False:
            mode = 0o755
            os.makedirs(user_dir_path, mode)  # dicrectory for current user
            os.makedirs(user_dir_path + "deerace/datasets/", mode)  # dicrectory for current user
            os.makedirs(user_dir_path + "deerace/results/", mode)  # dicrectory for current user


    except OSError:
        print("Creation of the directory %s failed" % user_dir_path)
    else:
        print("Successfully created the directory %s" % user_dir_path)

    print(message.photo[-1])

    try:
        cid = message.chat.id

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        photo_name = ""
        photo_name = "deerace_" + message.photo[-1].file_id + ".jfif"

        downloaded_file_path = ''
        downloaded_file_path = user_dir_path + photo_name


        print("downloaded_file_path = ", downloaded_file_path)
        with open(downloaded_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

            bot.reply_to(message, "I get photo for DeERace, wait a minute i processing them...")
            # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
            bot.send_chat_action(message.chat.id, 'typing')

            protected_file_path = os.path.join(project_dir_path, "lock_file.tmp")
            print("Protecting file: {}".format(protected_file_path))
            file_lock_handlers = FileLock(protected_file_path)

            with file_lock_handlers:
                with open(protected_file_path, "a") as file_handler:
                    deerace_object = DeERace(images_with_photo_path=downloaded_file_path, photo_name=photo_name, user_dir_path=user_dir_path)
                    face_find_count, list_of_file_paths_with_faces = deerace_object.find_face_and_processing()
                    if face_find_count == 0:
                        bot.reply_to(message, "Wait wait wait. I don't see faces in this photo! \n" +
                                     "Please send me photo with faces")
                        return
                    else:
                        bot.reply_to(message, "Ok i see " + str(face_find_count) + " faces.\n" +
                                     "When i prosecced all faces, i send result to you")

                        for dict_from_list in list_of_file_paths_with_faces:
                            for keys_from_dict in dict_from_list.keys():
                                bot.send_photo(message.chat.id, open(dict_from_list[keys_from_dict]['real'], 'rb'),
                                               caption="Real face",
                                               reply_markup=hideBoard,
                                               reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent
                                bot.send_photo(message.chat.id, open(dict_from_list[keys_from_dict]['fake'], 'rb'),
                                               caption="Fake face",
                                               reply_markup=hideBoard,
                                               reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent

                                print(dict_from_list[keys_from_dict]['real'])
                                print(dict_from_list[keys_from_dict]['fake'])
                                print()

                    file_handler.flush()
    except Exception as e:
        bot.reply_to(message, e)
#/////////////////////////////////////////</DeERace>//////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////



# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


def show_style_images_gallery(message):
    bot.send_photo(message.chat.id, open("ImagesForDeerace/style1.jpg", 'rb'),
                   caption="You can forward photo back, i use it as STYLE photo",
                   reply_markup=hideBoard,
                   reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent

    bot.send_photo(message.chat.id, open("ImagesForDeerace/style2.jpg", 'rb'),
                   caption="You can forward photo back, i use it as STYLE photo",
                   reply_markup=hideBoard,
                   reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent

    bot.send_photo(message.chat.id, open("ImagesForDeerace/style3.jpg", 'rb'),
                   caption="You can forward photo back, i use it as STYLE photo",
                   reply_markup=hideBoard,
                   reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent

def show_face_images_gallery(message):
    bot.send_photo(message.chat.id, open("ImagesForDeerace/dimon1.png", 'rb'),
                   reply_markup=hideBoard,
                   reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent

    bot.send_photo(message.chat.id, open("ImagesForDeerace/volodin-1.png", 'rb'),
                   reply_markup=hideBoard,
                   reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent

    bot.send_photo(message.chat.id, open("ImagesForDeerace/volodin-2.png", 'rb'),
                   reply_markup=hideBoard,
                   reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent

    bot.send_photo(message.chat.id, open("ImagesForDeerace/putin-2.jpg", 'rb'),
                   reply_markup=hideBoard,
                   reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent

    bot.send_photo(message.chat.id, open("ImagesForDeerace/migalkoff.jpg", 'rb'),
                   reply_markup=hideBoard,
                   reply_to_message_id=message.message_id)  # send file and hide keyboard, after image is sent


def bot_mode_id(message):
    cid = message.chat.id
    mode_setting_id = str(str(cid) + "-" + "mode") # In witch mode we are working

    if mode_setting_id in userStep.keys():
        if userStep[mode_setting_id] == 0:
            return 0 #make_style_transfer(message)
        elif userStep[mode_setting_id] == 1:
            return 1 #make_photo_deerace(message)
    else:
        return 0 #make_style_transfer(message)


def generate_start_guide():
    strart_guide_text = ""

    strart_guide_text += "*--------------Start Guide--------------*\n"
    strart_guide_text += "*Style Transfer mode* - _Default mode_\n"
    strart_guide_text += "*1* Send me STYLE image (chose send as photo). If you don't have style photo then use command /showStyleImagesGallery and forward any of given image\n"
    strart_guide_text += "*2* Send me any image, after that i transfer style from STYLE image, to you content image\n"
    strart_guide_text += "*3* Wait, and enjoy results.\n"
    strart_guide_text += "\n"
    strart_guide_text += "*DeERace image mode*\n"
    strart_guide_text += "*1* Use command /changeWorkMode\n"
    strart_guide_text += "*2* Push DeERace buttom\n"
    strart_guide_text += "*3* Send image with face or faces (chose as photo), or you can forward it to me from this, or another chat. "
    strart_guide_text += "You can forward one of standart faces use /showFaceImagesGallery\n"
    strart_guide_text += "*4* Wait, and enjoy DeERace photo result\n"

    strart_guide_text += "\n\n"
    strart_guide_text += "Write or push /help command to see all avalible commands"

    return strart_guide_text

# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command

        # bot.send_message(cid, "Hello, stranger, let me scan you...")
        # bot.send_message(cid, "Scanning complete, I know you now")

        command_help(m)  # show the new user the help page
        guide_text = generate_start_guide()
        bot.send_message(cid, guide_text, parse_mode='Markdown')
    else:
        bot.send_message(cid, "I already know you, no need for me to scan you again!")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = ""
    if bot_mode_id(m) == 0:
        help_text += "*-Working in Style Transfer mode-* \n"
        if is_we_have_style_photo(m) == True:
            help_text += "*Style photo set* \n"
            help_text += "*Make STEP->* Please send/forward me CONTENT photo\n"
        else:
            help_text += "*Style photo NOT set* \n"
            help_text += "*Make STEP->* Please send/forward me STYLE photo\n"
    else:
        help_text += "*-Working in DeERace mode-* \n"
        help_text += "*Make STEP->* Please send/forward me Photo with face\n"

    help_text += "\n"
    help_text += "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text, parse_mode='Markdown')  # send the generated help page


# chat_action example (not a good one...)
@bot.message_handler(commands=['deleteStyleImage'])
def command_delete_style_image(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)

    delete_style_photo(m)

    bot.reply_to(m,
                 "*DELETED STYLE PHOTO*\n\n" +
                 "I delete STYLE image. Next upload image i use as STYLE image\n\n" +
                 "*MAKE STEP->* Send or forward STYLE photo. Or use /showStyleImagesGallery and forward image to me...",
                 parse_mode='Markdown')


# chat_action example (not a good one...)
@bot.message_handler(commands=['showStyleImagesGallery'])
def command_show_style_images_gallery(m):
    show_style_images_gallery(m)

# chat_action example (not a good one...)
@bot.message_handler(commands=['showFaceImagesGallery'])
def command_show_face_images_gallery(m):
    show_face_images_gallery(m)



# chat_action example (not a good one...)
@bot.message_handler(commands=['showStartGuide'])
def command_show_start_guide(message):
    status_text = ""
    if bot_mode_id(message) == 0:
        status_text += "*-Working in Style Transfer mode-* \n"
        if is_we_have_style_photo(message) == True:
            status_text += "*Style photo set* \n"
            status_text += "*Make STEP->* Please send/forward me CONTENT photo\n"
        else:
            status_text += "*Style photo NOT set* \n"
            status_text += "*Make STEP->* Please send/forward me STYLE photo\n"
    else:
        status_text += "*-Working in DeERace mode-* \n"
        status_text += "*Make STEP->* Please send/forward me Photo with face\n"

    guide_text = status_text + "\n\n"
    guide_text += generate_start_guide()
    bot.reply_to(message, guide_text, parse_mode='Markdown')


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    print("handle_docs_photo")
    print(message)
    print(message.from_user.id)
    print(message.from_user.first_name)
    print(message.from_user.username)

    print(userStep)
    cid = message.chat.id
    mode_setting_id = str(str(cid) + "-" + "mode") # In witch mode we are working

    if mode_setting_id in userStep.keys():
        if userStep[mode_setting_id] == 0:
            make_style_transfer(message)
        elif userStep[mode_setting_id] == 1:
            make_photo_deerace(message)
    else:
        make_style_transfer(message)



# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['changeWorkMode'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Please chose ", reply_markup=imageSelectBotMode)  # show the keyboard
    userStep[cid] = 3  # set the user to the next step (expecting a reply in the listener now)


# if the user has issued the "/getImage" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)
def msg_image_select(message):
    cid = message.chat.id
    text = message.text
    mode_setting_id = str(str(cid) + "-" + "mode")  # In witch mode we are working

    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')
    if text == 'Style Transfer':  # send the appropriate image based on the reply to the "/getImage" command
        userStep[cid] = 0  # reset the users step back to 0
        userStep[mode_setting_id] = 0  # Mode is style transfer

        delete_style_photo(message) # Show Default style

        show_style_images_gallery(message)

        bot.send_message(cid, "*Style Transfer mode is ON*\n\n" +
                         "Now i will be work in Style Transfer mode. Please send me 2 photo\n" +
                         "1 - Style photo. \n" +
                         "2 - Content photo. \n" +
                         "Please don't send 2 photo in one message. Send me 2 separate photo by 2 messages\n" +
                         "You can *forward one of above photo for me* as STYLE photo\n\n" +
                         "*MAKE STEP->* Send or forward me STYLE photo",
                         reply_to_message_id=message.message_id, reply_markup=hideBoard,
                         parse_mode='Markdown')
    elif text == 'DeERace mode':
        userStep[cid] = 0
        userStep[mode_setting_id] = 1  # Mode is style transfer

        show_face_images_gallery(message) # Show Default face for DeERace

        bot.send_message(cid, "*DeERace mode is ON*\n\n" +
                         "Now i will be work in DeERace mode.\n" +
                         "Please send me photo with peoples faces.\n" +
                         "Or you can just *forward one of above photo to me*\n\n" +
                         "*MAKE STEP->* Send or forward me photo with face or faces",
                         reply_to_message_id=message.message_id, reply_markup=hideBoard,
                         parse_mode='Markdown')
    else:
        bot.send_message(cid, "Please, use the predefined keyboard!")
        bot.send_message(cid, "Please try again")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "I love you too!")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

bot.polling()
