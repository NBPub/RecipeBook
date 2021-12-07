# RecipeBook
Python web-app (Flask) to browse [Nextcloud Cookbook](https://apps.nextcloud.com/apps/cookbook) recipes on the local network. Designed for use with E-Ink screens. 

For a version that works with [Tandoor](https://docs.tandoor.dev/), please navigate to [RecipeBook-Tandoor](https://github.com/NBPub/RecipeBook-Tandoor)

[Deploy with Docker](https://github.com/NBPub/RecipeBook#application-setup) • [Local Build](https://github.com/NBPub/RecipeBook#build-locally) • [Screenshots](https://github.com/NBPub/RecipeBook#screenshots) • [Upcoming](https://github.com/NBPub/RecipeBook#upcoming)

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

 
### Usage

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

### Parameters

Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 5001:5000` would expose port `5000` from inside the container to be accessible from the host's IP on port `5001` outside the container.

| Parameter | Function |
| :----: | --- |
| `-p 5000:5000` | Default Flask port. Internal port should not be changed. |
| `-e TZ=America/Los_Angeles` | Set timezone for logging using tzdata. |
| `-e PAGE_TITLE=Recipe Book` | Home page title. Displays on tab. |
| `-e IMAGE_SIZE=Full` | Default image size to load. Can be changed to `Thumbnails`. Recipe pages have a toggle button to switch between sizes. |
| `-e FONT_SMALL=30` | Default size for "small" sections: **Description** and **Reviews**. Can be changed to any `<integer>` to adjust web-page display. |
| `-e FONT_LARGE=36` | Default size for "large" sections: **Ingredients** and **Instructions**. Can be changed to any `<integer>` to adjust web-page display. |
| `-v /recipe_data` | Recipes in this folder are read and displayed on the homepage. A refresh button is provided to re-parse recipes in the volume. Read only option added for example "ro" |
  
  
## Upcoming

**Version 1.0** is released. If issues are found or enhancements dreamt, they will come here until pushed to a new version.

**Version 1.1?**
* wget instead of curl for healthchecks - does this provide smaller docker image?
* Add tests
* clean up CSS styling
* Volume binding for configuration folder, let user poke through directories
* Error handling

**Tandoor Compatability**
* This version will work quite differently, so I made a new repository. See [here](https://github.com/NBPub/RecipeBook-Tandoor)
* To be released on DockerHub soon!

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

If you want to run RecipeBook without Docker, a python virtual environment is recommended. See [Flask Installation](https://flask.palletsprojects.com/en/2.0.x/installation/) for more details (and appropriate code for Windows). [Python 3.7](https://wiki.python.org/moin/BeginnersGuide/Download) or newer is recommended.

1. [Download](https://github.com/NBPub/RecipeBook/archive/refs/heads/main.zip) the code in the repository. Click the green code button at the top of the page for options.

2. Extract the folder contents. Copy the files+folders within "app" directory and "requirements.txt" to a new directory. Keep "ExampleRecipes" folder if you want to test with example data. All other contents can be deleted.

3. Move to newly made directory and create and activate **venv**.

```
$ cd newdirectory
$ python -m venv venv
$ . venv/bin/activate
```

4. Install Flask, dependencies.

```
$ pip install -r requirements.txt
```

5. Adjust Flask parameters as desired, see [Flask Quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/). A **Flask Env** file saves some typing when running the application. For example, if you only want the server to be visible from the local machine, remove `FLASK_RUN_HOST=0.0.0.0` from the file. The port number (default, 5000) can be changed in this file, too.

```
$ nano .flaskenv
```

*Note that all local variables associated with environmental variables can be modified by changing the code. See next step for an example*

6. Modify the path to recipe data. See line 13 of [RecipeReader.py](https://github.com/NBPub/RecipeBook/blob/main/app/RecipeReader.py). If you are using the ExampleRecipe folder, specify its location. Using a raw text string may be beneficial, but shouldn't be required.  `path = r'path/to/ExampleRecipes'`

*Optional* - Modify local variables that are typically specified by docker-container environmental variables. See lines 15-20 or the same file. Values can be changed by modifying the second entry in `environ.get("<environmental variable name>", "<parameter to be changed>"`.

7. Run! Open site in web browser (http://localhost:5000). 

```
$ flask run
```

8. Press Ctrl+C to stop server. Deactivate **venv** when finished.

```
$ deactivate
```

