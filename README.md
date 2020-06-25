# <p align="center">DeERaceTelegramBot</p>

<p align="center">DeERace Telegram Bot - final project of MIPT DLS part 1</p>

## Links

#### Links to bot:
 * [DeERace Telegram bot;](http://t.me/DeERace_bot)
 * Telegram user name: **@DeERace_bot** 

#### Based on Libs:
  * [pyTelegramBotAPI;](https://github.com/eternnoir/pyTelegramBotAPI)
  * [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
  * [Style transfer;](https://colab.research.google.com/drive/1-X4Q3LkPBLZrQZuLoBj4uA7xP0Hpj8mU)
    * [Neural-Style;](https://arxiv.org/abs/1508.06576)
    * [Author: Alexis Jacq;](https://alexis-jacq.github.io)
    * [Translate: Zueva Nadya;](https://github.com/nestyme)
  * [face_recognition;](https://github.com/ageitgey/face_recognition)
  * [FileLock lazyflow.](https://ilastik.github.io/lazyflow/_modules/lazyflow/utility/fileLock.html)
  
#### MIPT links:
  * [MIPT official site;](https://mipt.ru)
  * [MIPT Stepik DLS course](https://stepik.org/course/65388)

## Start Telegram Bot in you server
Steps:
1. It you wont start Bot by youself. Install all all requerements fro library above;
2. Registrate telegram bot in @BotFather telegram channel;
3. Copy given token and insert in file name `main_deerace_bot.py` in this line `TOKEN = '**INSERT TOKEN HERE**'`;
4. Make forlder `DeeraceBotWorkDir` as working folder;
5. Start `main_deerace_bot.py` file.


## Start Bot User Guide
### Style Transfer mode - _Default mode_
1. Send me STYLE image (chose send as photo). If you don't have style photo then use command `/showStyleImagesGallery` and forward any of given image
2. Send me any image, after that i transfer style from STYLE image, to you content image
3. Wait, and enjoy results.



### DeERace image mode
1. Use command `/changeWorkMode`
2. Push DeERace buttom
3. Send image with face or faces (chose as photo), or you can forward it to me from this, or another chat. You can forward one of standart faces use `/showFaceImagesGallery`
4. Wait, and enjoy DeERace photo result

Write or push `/help` command to see all avalible commands


### Available command
The following commands are available: 
* `/start`: Get used to the bot
* `/help`: Gives you information about the available commands. And working bot mode
* `/changeWorkMode`: Change work mode. If default mode = Style Transfer
* `/deleteStyleImage`: Clear style image. After this command you need upload new image
* `/showStyleImagesGallery`: Show default style images. Just forward it to me
* `/showFaceImagesGallery`: Show default face images. Just forward it to me
* `/showStartGuide`: Show start guide
