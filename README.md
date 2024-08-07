# Cats Against Humanity 🙀 

An online version of the game "Cards Against Humanity" (with added cats)

#### Websockets

Websockets are used to enable the real time behaviour of the game. The server uses flask-socketio and the client uses vue-socketio.

#### Client Application

A Flask view is used to serve the `index.html` as an entry point into the Vue app at the endpoint `/`.

The template uses vue-cli 3 and assumes Vue Cli & Webpack will manage front-end resources and assets.


#### Important Files

| Location             |  Content                                   |
|----------------------|--------------------------------------------|
| `/app`               | Flask Application                          |
| `/app/client.py`     | Flask Client (`/`)                         |
| `/src`               | Vue App .                                  |
| `/src/main.js`       | JS Application Entry Point                 |
| `/public/index.html` | Html Application Entry Point (`/`)         |
| `/public/static`     | Static Assets                              |
| `/dist/`             | Bundled Assets Output (generated at `yarn build` |


## Setup

##### Prerequisites

- Node
- Yarn
- Vue Cli 3
- Python 3
- Pipenv
- Heroku Cli

##### Install Dependencies

* Clone this repository:
	```
	$ git clone https://github.com/minchus/cats-against-humanity.git
	```

* Install node and python
Use `nvm` and `pyenv` to install the required versions of node and python.
 

* Setup node for Windows
	```
	$ npm install --global windows-build-tools
	$ npm config set python python2.7
	```

* Setup virtual environment, install dependencies, and activate it:
	```
	$ pipenv install --dev

  # or

	$ pip install -r requirements.txt
	```

* Install JS dependencies
	```
	$ nvm use 14.16.0
	$ yarn install
	```


## Development Server

Run Flask development server:
```
$ python run.py
```
It is not recommended to start the app with ```flask run```
(see https://flask-socketio.readthedocs.io/en/latest/getting_started.html)

```run.py``` is only used in development environments. It loads ```.env``` files that can be used to set variables
such as ```FLASK_PORT```.

From another terminal, start the webpack dev server:
```
$ yarn serve
```

The Vuejs application will be served from `localhost:8080` and the Flask Api
and static files will be served from `localhost:5000`.

The dual dev-server setup allows you to take advantage of
webpack's development server with hot module replacement.

Proxy config in `vue.config.js` is used to route the requests
back to Flask's Api on port 5000.

If you would rather run a single dev server, you can run Flask's
development server only on `:5000`, but you have to build the Vue app first
and the page will not reload on changes.
```
$ nvm use 14.16.0
$ yarn build
$ python run.py
```

## Docker images
```
# Build
docker build --no-cache -t cats-against-humanity .

# Get a shell
docker run --rm -it -v $(pwd):/code --entrypoint /bin/sh cats-against-humanity:latest

# Run locally
docker run -d --restart=always -p 8080:5000 cats-against-humanity:latest
```


## Deployment on DigitalOcean App Platform (deprecated)
App Platform sets the PORT environment variable to the port for your service to listen on 
([docs](https://docs.digitalocean.com/support/how-to-troubleshoot-apps-in-app-platform/#check-for-a-misconfigured-port-or-network-interface))

## Building and Deploying on Heroku (deprecated)
The Heroku free tier has been deprecated.

Gunicorn is used as the production server when deployed on Heroku

Heroku's nodejs buildpack will handle install for all the dependencies from the `packages.json` file.
It will then trigger the `postinstall` command which calls `yarn build`.
This will create the bundled `dist` folder which will be served by Flask.

The python buildpack will detect the `Pipfile` and install all the python dependencies.

Here are the commands we need to run to get things setup on the Heroku side:

	```
	$ heroku apps:create cats-against-humanity
	$ heroku git:remote --app cats-against-humanity
	$ heroku buildpacks:add --index 1 heroku/nodejs
	$ heroku buildpacks:add --index 2 heroku/python
	$ heroku config:set FLASK_ENV=production
	$ heroku config:set FLASK_SECRET=SuperSecretKey

	$ git push heroku

	$ heroku ps:scale web=1
	```
### TO DO
Add game stats to "about" page?
