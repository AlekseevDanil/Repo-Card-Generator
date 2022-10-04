# -*- coding: utf-8 -*-
# Created by Danil Alekseev on 22.09.2022.
from beautifulrepo.generator import CardGenerator
import sys


if __name__ == "__main__":
    # A working example of generating an image using the CardGenerator class
    config_filepath = None if not sys.argv[1:] else sys.argv[-1]

    if config_filepath:
        # With using config.yml
        cg = CardGenerator(config_filepath=config_filepath)
        cg.create()
        cg.save()
    else:
        # Without using config.yml
        cg = CardGenerator()
        cg.create(shape=(1280, 640), repository_name="Your repository name", repository_author="Your profile name")
        cg.save(save_path="beautifulrepo/assets/imgs/repo_card.jpg", show=True)
