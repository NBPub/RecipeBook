# RecipeBook
Python web-app (Flask) to browse [Nextcloud Cookbook](https://apps.nextcloud.com/apps/cookbook) recipes on the local network. Designed for use with E-Ink screens. 

For a version that works with [Tandoor](https://docs.tandoor.dev/), please navigate to [RecipeBook-Tandoor](https://github.com/NBPub/RecipeBook-Tandoor)

[Deploy with Docker](#application-setup) • [Local Build](#build-locally) • [Screenshots](#screenshots) • [Version History](#history)

## Overview

I created this to access recipes from [Nextcloud Cookbook](https://apps.nextcloud.com/apps/cookbook) and easily view them on Kindle's web browser whilst cooking. The view is designed for such screens, and is not as nice as the actual app. Therefore, accessing your Nextcloud website with a mobile device or tablet would just as effectively provide kitchen access to Cookbook.

Please note that the web application is very basic and should not be run on untrusted networks. It is not designed to be exposed publicly.

The machine running the app should have access to the Nextcloud user data (directly or via network share). 
The recipe data is supplied to the RecipeBook container by [volume binding](https://docs.docker.com/storage/bind-mounts/) the folder. 
See [LinuxServer.io](https://docs.linuxserver.io/) and [Docker](https://docs.docker.com/) for more information on Docker containers.

This is my first project using Flask and building Docker containers. Feedback is appreciated.


## Application Setup

Install and run using docker, examples provided below.

Access main page at `<your-ip>:5000`. See below for changing port number.

 
### Usage

This container is designed to run on the same machine hosting Nextcloud data. The volume binding below is for the directory containing the recipes stored by Nextcloud Cookbook. 
Alternatively, the data can be copied to another location, and then that location can be bound to `/code/recipe_data`

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
      - <path/to/recipes-folder>:/code/recipe_data
    ports:
      - 5000:5000
    environment:
      - TZ=America/Los_Angeles
      - PAGE_TITLE=Recipe Book
      - IMAGE_SIZE=Full
      - FONT_SMALL=30
      - FONT_LARGE=36
      - ENABLE_API=False	  
    healthcheck:
      test: wget --no-verbose --tries=1 --spider http://localhost:5000 || exit 1
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
  -e ENABLE_API=False \  
  -p 5000:5000 \
  -v <path/to/recipes-folder>:/code/recipe_data \
  --health-cmd wget --no-verbose --tries=1 --spider http://localhost/ || exit 1 \
  --health-interval 300s \
  --health-timeout 10s \
  --health-start-period 5s \
  --restart unless-stopped \
  nbpub/recipelook:latest
```

### Parameters

Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. 
For example, `-p 5001:5000` would expose port `5000` from inside the container to be accessible from the host's IP on port `5001` outside the container.

| Parameter | Function |
| :----: | --- |
| `-p 5000:5000` | Default Flask port. Internal port should not be changed. |
| `-e TZ=America/Los_Angeles` | Set timezone for logging using tzdata. |
| `-e PAGE_TITLE=Recipe Book` | Home page title. Displays on tab. |
| `-e IMAGE_SIZE=Full` | Default image size to load. Can be changed to `Thumbnails`. Recipe pages have a toggle button to switch between sizes. |
| `-e FONT_SMALL=30` | Default size for "small" sections: **Description** and **Reviews**. Can be changed to any `<integer>` to adjust web-page display. |
| `-e FONT_LARGE=36` | Default size for "large" sections: **Ingredients** and **Instructions**. Can be changed to any `<integer>` to adjust web-page display. |
| `-e ENABLE_API=False` | Set to `True` to add an endpoint at `<your-ip>:5000/api/info` to return system statistics (temperature, load, CPU and RAM usage) as JSON. |
| `-v /code/recipe_data` | Recipes in this folder are read and displayed on the homepage. A refresh button is provided to re-parse recipes in the volume. Set to **Read-only** with ":ro" |
  
### Supported Architectures

Images are available for the following architectures:

| Architecture |
| :----: | 
| x86-64 |
| arm64 | 
| armhf |

Pulling from DockerHub should provide the correct image for your system. 
The application is built on the python-alpine base image. Debian-based images are available by adding `debian-` before a tag.

| Tags | Description |
| :----: |  --- |
| *latest* | Images built with each commit |
| *v1.0*, *v1.1* | Stable releases, see [history](#history) below. |
| *tandoor* | Tandoor compatible `v1.0` image, *no Debian image* |

See [DockerHub Repository](https://hub.docker.com/r/nbpub/recipelook)

  
## History

**Version 1.0** | *[docker](https://hub.docker.com/layers/nbpub/recipelook/v1.0/images/sha256-56ba4a2077383e6c516ece5456e52320434d4706faea41566119f27626358a1d): `v1.0`*
* Initial release (16 Nov 2021)
* mount recipes in `/recipe_data` not `/code/recipe_data`

**Tandoor Compatability** *[docker](https://hub.docker.com/layers/nbpub/recipelook/tandoor/images/sha256-9e7abf1acdbce7667456bb74cbef2727cf4f61209af97a011541effe16076471): `tandoor`*
* This version works differently, so I made a new [repository](https://github.com/NBPub/RecipeBook-Tandoor)
* Github and Docker images will not updated past **Version 1.0**

----

### Current Version

**Version 1.1** *[docker](): `v1.1`, `latest`*
* update Python, Flask (March 2023)
* add API call for system info
  * adds [psutil](https://github.com/giampaolo/psutil#summary) as dependency
* restructured code
  * using "application factory" design in flask, moved initial loading + checks to `__init__.py`
  * added error page for No Recipe Data, rest of application will not load
  * JSON API is separate blueprint and file
* change mount point for recipe data, added checks and logging for data path
* building docker images via Github workflows
  * multi-stage builds with Python **slim-bullseye** and **alpine** base images
* wget instead of curl for healthchecks - no need to install curl on alpine image

----

***Version 1.2???***

* **Code**
  * Add tests
  * clean up CSS styling
  * Cache cleaning - delete recipe images from static
* **Deployment**
  * Volume binding for configuration folder, let user poke through directories
  * Allow recipe_data folder be specified by environmental variable, instead of hard-coded in app
  * Use non-root user in dockerfile, allow using non-root user for container (root required to make directory)

----

## Screenshots

<details>
  <summary>Home Page, lists all recipes</summary>
  
  ![Home](/Screenshots_Kindle/homepage.png "Home Page")
</details>

<details>
  <summary>Filter Button</summary>
    
  ![Home](/Screenshots_Kindle/category_filter.png "Filter Button")
</details>

<details>
  <summary>Text Search, recipe titles only</summary>
    
  ![Home](/Screenshots_Kindle/searchbar.png "Search Bar")
</details>

<details>
  <summary>Recipe Page example, full-sized image</summary>
    
  ![Home](/Screenshots_Kindle/ex_full.png "Big Image")
</details>


<details>
  <summary>Recipe Page example, thumb-sized image, Ingredients</summary>
    
  ![Home](/Screenshots_Kindle/ex_thumb.png "Small Image")
</details>


<details>
  <summary>Recipe Page example, continued . . . Instructions</summary>
    
  ![Home](/Screenshots_Kindle/instructions.png "Instructions")
</details> 


<details>
  <summary>Recipe Page example, continued . . . Reviews</summary>
    
  ![Home](/Screenshots_Kindle/reviews.png "Reviews")
</details> 



## Build Locally   

*Instructions may not be comprehensive. Docker deployment is recommended.*

If you want to run RecipeBook without Docker, a python virtual environment is recommended. 
See [Flask Installation](https://flask.palletsprojects.com/en/2.0.x/installation/) for more details. 
[Python 3.9](https://wiki.python.org/moin/BeginnersGuide/Download) or newer is recommended.

1. [Download](https://github.com/NBPub/RecipeBook/archive/refs/heads/main.zip) the code in the repository. Click the green code button at the top of the page for options.

2. Extract the folder contents. Copy the files+folders within "app" directory and "requirements.txt" to a new directory `newdirectory`. 
Rename "ExampleRecipes" to "recipe_data" if you want to test with example data. All other contents can be deleted.

3. Copy your recipe data folder to "recipe_data" within newly made directory: `newdirectory/recipe_data` OR see **Step 7**

4. Create and activate **venv** within new directory.

```
$ cd newdirectory
$ python -m venv venv
$ . venv/bin/activate
```

5. Install Flask, dependencies. *psutil* should be removed from [requirements.txt](/requirements.txt)

```
$ pip install -r requirements.txt
```


6. *Optional* Modify the path to recipe data. See line 18 of [__init__.py](https://github.com/NBPub/RecipeBook/blob/main/app/__init__.py#L18). 
If you are using the ExampleRecipe folder, specify its location. 
Using a raw text string may be beneficial, but shouldn't be required.  `path = r'path/to/ExampleRecipes'`
   - Modify local variables that are typically specified by environmental variables. See lines 6-15 of the same file.
       - `getenv("<environmental variable name>", "<parameter to be changed>"`.
   - Enable the API by setting [line 40](https://github.com/NBPub/RecipeBook/blob/main/app/__init__.py#L40) to `True`. Ensure [psutil](https://github.com/giampaolo/psutil#summary) is installed.

7. Run! Open site in web browser http://localhost:5000 . Adjust Flask parameters as desired, see [Flask Quickstart](https://flask.palletsprojects.com/en/2.2.x/quickstart/). 

```
$ flask --debug run
```

8. Press Ctrl+C to stop server. Deactivate **venv** when finished.

```
$ deactivate
```

