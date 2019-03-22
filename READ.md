# ffprobe Audio Channel Analyzer - python3


:zap: This is a python3 flask base audio channel server. Will start flask server and provide audio channels, url link, and duration 


## Install & use
:coffee: Install last Python 3 stable version and:

```sh

# activate virtuale enviroment
. ./venv/bin/activate

# run applicatoin

flask run 

```

To make request 

method=POST
```
Local API:

http://0.0.0.0:9000/ffprobe-analyze

request json:

{
    url: <some-url-goes-here>
}

```


## Contributing
Feel free to use for your needs as you wish. Project can be improved to be much more flexible and be more informative
