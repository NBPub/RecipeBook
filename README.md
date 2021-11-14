# RecipeBook
Python web-app (Flask) to browse Nextcloud Cookbook recipes on the local network. Designed for use with E-Ink screens.

## Overview

I created this to access recipes from [Nextcloud Cookbook](https://apps.nextcloud.com/apps/cookbook) and easily view them on Kindle's web browser whilst cooking. The view is designed for such screens, and is not as nice as the actual app. Therefore, accessing your Nextcloud website with a mobile device or tablet would just as effectively provide kitchen access to Cookbook.

Please note that the web application is very basic and should not be run on untrusted networks. It is not designed to be exposed publicly.

The machine running the app should have access to the Nextcloud user data (directly or via network share). The data is supplied to the container using volume binding. See [LinuxServer.io](https://docs.linuxserver.io/) and [Docker](https://docs.docker.com/) for more information on Docker containers.

This is my first project using Flask and building Docker containers. Feedback is appreciated.

### Supported Architectures

Pulling from DockerHub should provide the correct image for your system. The application is built on the python-alpine base image. See [DockerHub Repository](https://hub.docker.com/r/nbpub/recipelook)

Images are available for the following architectures:

| Architecture | 
| :----: | 
| x86-64 |
| arm64 | 
| armhf |

## Application Setup

Install and run using docker, examples provided below.

Access main page at `<your-ip>:5000`. See below for changing port number.

## Usage

This container is designed to run on the same machine hosting Nextcloud data. The volume binding below is for the directory containing the recipes stored by Nextcloud Cookbook. Alternatively, the data can be copied to another location, and then that location can be bound to "/recipe_data".

If using the [LSIO NextCloud docker container](https://github.com/linuxserver/docker-nextcloud#usage), the folder may be in the following location:
```
<volume bound to NextCloud data "/data">/<user>/files/Recipes
```
Example configurations to build container are shown below. Environmental Variables are listed with default values and do not need to be specified. Healthcheck is optional.

### docker-compose

```yaml
---
version: "2"
services:
  recipe:
    image: nbpub/recipelook:latest
    container_name: recipebook
    volumes:
      - <path/to/recipes-folder>:/recipe_data:ro
    ports:
      - 5000:5000
    environment:
      - TZ=America/Los_Angeles
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
  -e TZ=America/Los_Angeles \
  -e PAGE_TITLE=Recipe Book \
  -e IMAGE_SIZE=Full \
  -e FONT_SMALL=30 \
  -e FONT_LARGE=36 \
  -p 5000:5000 \
  -v <path/to/recipes-folder>:/recipe_data:ro \
  --restart unless-stopped \
  nbpub/recipelook:latest
```

## Parameters

Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 5001:5000` would expose port `5000` from inside the container to be accessible from the host's IP on port `5001` outside the container.

| Parameter | Function |
| :----: | --- |
| `-p 5000` | Default Flask port. |
| `-e TZ=America/Los_Angeles` | Set timezone for logging using tzdata. |
| `-e PAGE_TITLE=Recipe Book` | Home page title. Displays on tab. |
| `-e IMAGE_SIZE=Full` | Default image size to load. Can be changed to `Thumbnails`. Recipe pages have a toggle button to switch between sizes. |
| `-e FONT_SMALL=30` | Default size for "small" sections: **Description** and **Reviews**. Can be changed to any `<integer>` to adjust web-page display. |
| `-e FONT_LARGE=36` | Default size for "large" sections: **Ingredients** and **Instructions**. Can be changed to any `<integer>` to adjust web-page display. |
| `-v /recipe_data` | Recipes in this folder are read and displayed on the homepage. A refresh button is provided to re-parse recipes in the volume. Read only option added for example "ro" |

## Screenshots

* Home Page, lists all recipes
![Home](/Screenshots_Kindle/homepage.png "Home Page")

* Filter Button
![Home](/Screenshots_Kindle/category_filter.png "Filter Button")

* Text Search, recipe titles only
![Home](/Screenshots_Kindle/searchbar.png "Search Bar")

* Recipe Page example, full-sized image
![Home](/Screenshots_Kindle/ex_full.png "Big Image")

* Recipe Page example, thumb-sized image
![Home](/Screenshots_Kindle/ex_thumb.png "Small Image")

* Recipe Page example, continued . . .
![Home](/Screenshots_Kindle/instructions.png "Instructions")

* Recipe Page example, continued . . .
![Home](/Screenshots_Kindle/reviews.png "Reviews")

## Upcoming

**Version 1.0** is released. If issues are found or enhancements dreamt, they will come here until pushed to a new version.

**Version 1.1:**
* Compatability with [Tandoor Recipes](https://github.com/TandoorRecipes/recipes)

**Maybe Later**
* wget instead of curl for healthchecks - does this provide smaller docker image?
* Add tests
* clean up CSS styling

