# RecipeBook
Python web-app (Flask) to browse Nextcloud Cookbook recipes on the local network. Designed for use with E-Ink screens.

## Overview

I created this to access recipes from [Nextcloud Cookbook](https://apps.nextcloud.com/apps/cookbook) and easily view them on Kindle's web browser. The view is designed for such screens, and is not as nice as the actual app. Therefore, accessing your Nextcloud website with a mobile device or tablet would just as effectively provide kitchen access to Cookbook. Note that the web application is very basic and should not be run on untrusted networks.

The machine running the app should have access to the Nextcloud user data (directly or via network share). The data is supplied to the container using volume binding. See [LinuxServer.io](https://docs.linuxserver.io/) and [Docker](https://docs.docker.com/) for more information on Docker containers.

This is my first project using Flask and building Docker containers. Feedback is appreciated.

## Application Setup

*after adding image to dokcerhub, provide access information*

Access main page at `<your-ip>:5000`. See below for changing port number.

## Usage
*To Do: Allow for timezone (tzdata) selection.*

This container is designed to run on the same machine hosting Nextcloud data. The volume binding below is for the directory containing the recipes stored by Nextcloud Cookbook. Alternatively, the data can be copied to another location, and then that location can be bound to "/recipe_data".

If using the [LSIO NextCloud docker container](https://github.com/linuxserver/docker-nextcloud#usage), the folder may be in the following location:
<volume bound to NextCloud data "/data">/<NextCloud user>/files/Recipes

Example configurations to build container are shown below. Environmental Variables are listed with default values and do not need to be specified. Healthcheck is optional.

### docker-compose

```yaml
---
version: "2"
services:
  recipe:
    image: recipes:latest
    container_name: recipebook
    volumes:
      - <path/to/recipes-folder>:/recipe_data
    ports:
      - 5000:5000
    environment:
      - PAGE_TITLE=Recipe Book
      - IMAGE_SIZE=Full
      - FONT_SMALL=30
      - FONT_LARGE=36
    healthcheck:
      test: curl -I --fail http://localhost:5000 || exit 1
      interval: 300s
      timeout: 10s
      start_period: 5s
    restart: unless-stopped
```

### docker cli ([click here for more info](https://docs.docker.com/engine/reference/commandline/cli/))

```bash
docker run -d \
  --name=recipebook \
  -e PAGE_TITLE=Recipe Book \
  -e IMAGE_SIZE=Full \
  -e FONT_SMALL=30 \
  -e FONT_LARGE=36 \
  -p 5000:5000 \
  -v <path/to/recipes-folder>:/recipe_data \
  --restart unless-stopped \
  <path to image or docker hub link, to be added>
```

## Parameters

Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 5001:5000` would expose port `5000` from inside the container to be accessible from the host's IP on port `5001` outside the container.

| Parameter | Function |
| :----: | --- |
| `-p 5000` | Default Flask port. |
| `-e PAGE_TITLE=Recipe Book` | Home page title. Displays on tab. |
| `-e IMAGE_SIZE=Full` | Default image size to load. Can be changed to "Thumbnails". Recipe pages have a toggle button to switch between sizes. |
| `-e FONT_SMALL=30` | Default size for "small" sections: Description and Reviews. Can be changed to any integer to adjust web-page display. |
| `-e FONT_Large=36` | Default size for "large" sections: Ingredients and Instructions. Can be changed to any integer to adjust web-page display. |
| `-v /recipe_data` | Recipes in this folder are read and displayed on the homepage. A refresh button is provided which will capture changes to volume. |
