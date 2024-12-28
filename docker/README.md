# Python Micro-Enterprise-Service-Bus Examples Docker Container

## 1. Docker

A running docker installation is required.

You can either download the working docker examples container here:
https://docker.webcodex.de/microesb-examples-latest.tar

Import with the following command, afterwards continue with step 3.

```bash
docker image load < microesb-examples-latest.tar
```

Or build the image by yourself: just continue with step 2.

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

```bash
# run example 1 and print out db tables content
./exec-example1.sh
```

```bash
# run example 2, cert-ca, cert-server and cert-client
./exec-example2.sh
```

