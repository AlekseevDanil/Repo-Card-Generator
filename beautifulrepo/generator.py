# -*- coding: utf-8 -*-
# Created by Danil Alekseev on 22.09.2022.

from PIL import Image, ImageFont, ImageDraw
from pilmoji import Pilmoji
from loguru import logger
import yaml
import random
import os


class CardGenerator:
    """
    Repository image card generation class.

    Init Params:
        :param config_filepath: (optional, type: str) - path to configuration file. [!] Mandatory config.yml name.
    """

    @logger.catch
    def __init__(self, config_filepath=None):
        # Validation
        if config_filepath and config_filepath[-10:] != "config.yml":
            mes = "The config file should be named yes \"config.yml\". Specify a valid path."
            raise ValueError(mes)

        # Getting parameters
        self.configs = None
        if config_filepath:
            with open(config_filepath, "r") as config_file:
                self.configs = yaml.load(config_file, Loader=yaml.FullLoader)
            logger.warning(f"Path to config file found")
        else:
            logger.warning(f"If you do not use the config file in the methods, "
                           f"specify all the necessary parameters")
        self.image = None

    @logger.catch
    def create(self, shape=None,
               repository_name=None,
               repository_author=None,
               font_path="/assets/fonts/OpenSans-Medium.ttf",
               avatar_path="/assets/imgs/github.png",
               background_path="/assets/imgs/background.png",
               emoji="/assets/emoji.txt"):
        """
        Image generating function. Returns the class image.
        Does not save the result, does not show the result.

        Params:
            :param shape: (required if config.yml not exist, type: typle) - parameter indicating the size of
        the future image: (recommended: (1280, 640) )
            :param repository_name: (required if config.yml not exist, type: str) - the name of your repository
            :param repository_author: (required if config.yml not exist, type: str) - your name
            :param font_path: (optional, type: str) - path to font
            :param avatar_path: (optional, type: str) - path to the image (a square image is recommended,
        otherwise it will stretch into a square on its own)
            :param background_path: (optional, type: str) - path to background image
            :param emoji: (optional, type: str) - path to txt file with emoji inside (it is recommended to change
        the file itself, not the path)
        """

        logger.warning(f"Recommended image size: (1280, 640)")
        dir = os.path.dirname(os.path.realpath(__file__))
        font_path = dir + font_path
        avatar_path = dir + avatar_path
        emoji = dir + emoji
        background_path = dir + background_path
        # Validation
        if not self.configs:
            if not shape or not repository_name or not repository_author:
                mes = "If there is no config file, you need to specify all the parameters"
                raise ValueError(mes)

            width, height = shape
        else:
            width = self.configs["image"]["shape"]["width"]
            height = self.configs["image"]["shape"]["height"]
            repository_name = self.configs["content"]["repository_name"]
            repository_author = self.configs["content"]["repository_author"]
            font_path = self.configs["content"]["font_path"] if "font_path" in self.configs["content"] else font_path
            avatar_path = self.configs["content"]["avatar_path"] if "avatar_path" in self.configs["content"] else avatar_path
        if width < 1 or height < 1:
            mes = "Height and width values must be > 1"
            raise ValueError(mes)

        # Generating a card
        logger.debug(f"Repo card generation in progress")

        background = Image.open(background_path).resize([width, height])
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype(font_path, 60)

        # Choose random emoji and draw on the image
        with Pilmoji(background) as pilmoji:
            with open(emoji, "r") as file:
                file = file.read().split()
                random_emoji = random.choices(list(file), k=4)
                emoji_text = "  ".join(random_emoji)

            pilmoji.text(xy=((width//2)-160, 90), text=emoji_text,
                         fill=(0, 0, 0), font=font, anchor="ms")

        # Write text on the image
        draw.text(xy=(width // 2, (height-100) // 2),
                  text=repository_name, fill=(255, 255, 255), font=font, anchor="ms")
        draw.text(xy=(width // 2, (height+50) // 2),
                  text=f"created by {repository_author}", fill=(255, 255, 255), font=font, anchor="ms")

        # Adding avatar on image
        avatar = Image.open(avatar_path, "r")
        avatar_side = width // 7
        avatar = avatar.resize([avatar_side, avatar_side])
        background.paste(avatar, (width // 2-(avatar_side//2), (height+150)//2))

        self.image = background.convert('RGB')
        logger.debug(f"Success!")

    @logger.catch
    def save(self, save_path=None, show=False):
        """
        Function to save generated image, use strictly after image generation.

        Params:
            :param save_path: (default value if config.yml exist: None) - path to save image.
        Type String. Be sure to include a filename
            :param show: (default value: False) - parameter that allows you to display
        the image display window after saving
        """

        # Validation
        if not self.image:
            mes = "Please use this method after card generation (CardGenerator -> create -> save)"
            raise ValueError(mes)
        if not self.configs and not save_path:
            mes = "Mandatory parameter \"save_path=...\" if there is no config file"
            raise ValueError(mes)

        # Saving the image
        if not save_path:
            save_path = self.configs["image"]["save_path"]
        logger.debug(f"The repo card is saved to \"{save_path}\"")
        self.image.save(save_path)
        logger.debug(f"Success!")

        # Shows the image in a window after saving
        if show or (self.configs and self.configs["image"]["show"]):
            self.image.show(title=save_path)
