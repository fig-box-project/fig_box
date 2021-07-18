# Figbox

> Figbox is a simple and fast background service system, it can be simply installed on the server and simply run.

It relies on Fastapi, so it is very simple and easy to use. Even if you don't know how to program, you can use the already built modules to build your services for you.

## How to start it ?

Since Fastapi is used, you can use uvicorn to start it, for example:

```uvicorn app.main:app --port 8080 --host 0.0.0.0 --reload```

Of course you can't run it at the beginning, you have to build the environment, please find a way to download this project to your directory, you can use git clone, for example:

```git clone https://github.com/normidar/fig_box```

After cloning, please go to the directory, for example:

```cd fig_box```

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.