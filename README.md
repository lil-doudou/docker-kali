# docker-kali
Kali environement in Docker


## How to use
Build the image
```sh
sudo docker build . -t kali
```

Run the Docker
```sh
sudo docker run --rm -d -p 2200:22 --name kali kali
```

Interact (user: kali / password : kali)
```sh
ssh -X kali@127.0.0.1 -p 2200
```

Example : run firefox