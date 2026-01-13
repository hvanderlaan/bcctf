# bcpen docker images
Bcpen docker images is a set of security tool images an vulnerable images to test the security tools. The images are multi-arch `amd64` and `arm64` therefor the images can be used on AMD, Intel and Apple Silicon processors.

## Usage tools

```bash
git clone https://github.com/hvanderlaan/bcpen.git
cd bcpen/<image>
docker builder prune
docker build --no-cache -t <usernane>/<tool>:<arch> --build-arg ARCH=<arch>/ .
docker push <username>/<tool>:<arch>

docker buildx imagetools create -t <username>/<tool>:latest <username>/<tool>:amd64 <username>/<tool>:arm64
docker pull bcpen/<tool>:latest
docker run --rm -ti bcpen/<tool> --help
```
or get the latest version from docker hub
```bash
docker pull bcpen/<tool>:latest
docker run --rm -ti bcpen/<tool> --help
```

## Usage servers
```bash
git clone https://github.com/hvanderlaan/bcpen.git
cd bcpen/<server>
docker builder prune
docker build --no-cache -t <usernane>/<server>:<arch> --build-arg ARCH=<arch>/ .
docker push <username>/<server>:<arch>

docker buildx imagetools create -t <username>/<server>:latest <username>/<server>:amd64 <username>/<server>:arm64
docker pull bcpen/<server>:latest
docker run --name <server> -d --rm -p <port>:<port> bcpen/<server>
```
or get the latest version from docker hub
```bash
docker pull bcpen/<tool>:latest
docker run --name <server> -d --rm -p <port>:<port> bcpen/<server>
```

## pwncat-cs
```bash
cd tools/pwncat-cs
docker builder prune
docker build --no-cache --tag bcpen/pwncat:latest .
docker run --rm --name pwncat -ti -p <port>:<port> -v <workdir>:/work bcpen/pwncat -lp <port>
```

## License M.I.T.

```
Docker images
Copyright © 2025 Harald van der Laan

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```