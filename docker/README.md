# Python Micro-Enterprise-Service-Bus Examples Docker Container

## 1. Docker

If you want to build the docker examples image on your own, a running docker
installation is needed.

The working docker examples container can be downloaded here:

## 2. Build Image

The `build-examples.sh` script will do the following.

- Build Python micro-esb Module (sdist) inside /dist
- Build examples Docker Container from examples.dockerfile
- Put dependencies inside Docker Container
- Init postgres database
- Setup Example Number 1 database (hosting-example)

```bash
./build-examples.sh
```

## 3. Run Container

Start container by the following command. This will start postgresql database
in background.

```bash
./start-examples-container.sh
```

## 4. Execute Examples

When the container is running successfully, run `exec-example1.sh` to execute
example number 1. Also the inserted database records will be printed out when
execution was successful.

Run `exec-example2.sh` to execute all 3 examples
(cert-ca, cert-server and cert-client).

