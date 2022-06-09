

## Docker build 

```docker
docker build -t pythondep .
docker run --rm -it --env-file env.list -p 80:80 pythondep
````