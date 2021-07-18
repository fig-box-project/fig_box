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

After entering the directory, you also need to create a virtual space (if you want to make it simple or not create it), for example:

```python3 -m venv tutorial-env```

Then you can download the required installation package in the virtual environment, please run the following command:

```pip3 install -r requirements.txt```

At this point you can start to run the command written in the front, and you only need to execute it in the future.

```uvicorn app.main:app --port 8080 --host 0.0.0.0 --reload```

> We hope this part can be made simpler. Simplicity is our original intention. If you have the time and ability, I hope you can help us develop a launcher.

## The Api View

After starting the system, you can enter this link to view the API view of your system:

```http://0.0.0.0:8080/docs```


