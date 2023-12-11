# Snet-POC

For this POC the following guide was followed: [SNET Full Guide (Testnet)
](https://docs.google.com/document/d/1jkkIMvUObSc81Cv3WXl9wtjFwt-itFSaOctyGdPg_30/edit)

On arm64 systems it was not an option to use internal [etcd](https://etcd.io/), as this way snet deamon was unable to run on in a virtualized amd64 docker container.

## Execution

Execution was tested on a Mac with arm64 architecture.
You need to have [docker](https://www.docker.com/) installed and running on your computer.
Make sure to provide the volumes defined in the [docker-compose.yml](./docker-compose.yml) file if not already existent.

### etcd

Build and start the docker container defined in the [docker-compose.yml](./docker-compose.yml) file:

```bash
# build etcd container
docker-compose build etcd

# start the etcd docker container
docker-compose up -d etcd
```

### snet cli

Setup a snet-cli and run snet commands as follows:

```bash

# build container
docker-compose build snet-cli

# start container
docker-compose up -d snet-cli

# stop container
docker-compose down snet-cli

# connect to bash
docker-compose exec snet-cli bash

# Replace [SNET-CLI-COMMAND] with the actual SNET-cli command you want to run.
docker-compose exec snet-cli snet [SNET-CLI-COMMAND]
```

### grpc service

Build and start the docker container defined in the [docker-compose.yml](./docker-compose.yml) file:

```bash
# start snet deamon
docker-compose up -d grpc-server

# stop container
docker-compose down snet-cli
```

### Snet deamon

Note: Before starting the deamon, you should create your [organisation](##identity-and-org-setup) and [service](##service-setup). Moreover, the [grpc service](###grpc-service) should be running.

```bash
# start snet deamon
docker-compose up -d snetd

# stop container
docker-compose down snetd
```

### Calling service with snet-cli

All [docker-compose.yml](./docker-compose.yml) services must be up and running.
Make sure to switch into the clients identiy (e.g.: `docker-compose exec snet-cli snet identity <name-of-identity>`)

```bash
# Create a deposit for service executions
docker-compose exec snet-cli snet account deposit 10.0

# Create a channel for service executions (example org)
docker-compose exec snet-cli snet channel open-init trustlevel-org-id-2 default_groups 10.0 +2days

# Execute the example service
docker-compose exec snet-cli snet client call trustlevel-org-id-2 trustlevel-service-4 default_groups call '{"query":"Hello Josch"}'

# Claim payments https://docs.google.com/document/d/1jkkIMvUObSc81Cv3WXl9wtjFwt-itFSaOctyGdPg_30/edit#heading=h.r684e4ffzwng
docker-compose exec snet-cli snet treasurer claim-all --endpoint http://snetd:7001

docker-compose exec snet-cli snet account balance

# Withdraw money from MPE into Wallet
docker-compose exec snet-cli snet account withdraw <AMOUNT>

# Client close channels: https://docs.google.com/document/d/1jkkIMvUObSc81Cv3WXl9wtjFwt-itFSaOctyGdPg_30/edit#heading=h.y464yvlwwaa4
docker-compose exec snet-cli snet channel claim-timeout-all
```

## Identity and Org setup

```bash
# Make sure snet-cli is started
docker-compose up -d snet-cli

# create identity
docker-compose exec snet-cli snet identity create <name-of-your-identity> key --private-key <metamask-private-key> --network goerli

# switch to identity
docker-compose exec snet-cli snet identity <name-of-identity>
# example:
docker-compose exec snet-cli snet identity trustlevel-test-2

# Create organization
docker-compose exec snet-cli snet organization metadata-init <org-name> <org-id> individual --metadata-file /data/organization_metadata.json
# example:
docker-compose exec snet-cli snet organization metadata-init trustlevel-org trustlevel-org-id-2 individual --metadata-file /data/organization_metadata.json

# Add description for the example
docker-compose exec snet-cli snet organization metadata-add-description --description "Trustlevel long description" --short-description  "Trustlevel short description" --url "https://www.trustlevel.io/" --metadata-file /data/organization_metadata.json

# Add default group connected with internal etcd
docker-compose exec snet-cli snet organization add-group default_groups 0x007692276fe8d9941FF9bB4f2CfE0047dD9EB406 http://etcd:2379 --metadata-file /data/organization_metadata.json

## Create example org on Blockchain
docker-compose exec snet-cli snet organization create trustlevel-org-id-2 --metadata-file /data/organization_metadata.json

## DELETE example org from Blockchain (note that you can not reuse the name even after deletion)
docker-compose exec snet-cli snet organization delete trustlevel-org-id

```

## Service setup

```bash

# Create service metadata for example service
# /app/src is mounted into snet-cli
docker-compose exec snet-cli snet --print-traceback service metadata-init \
    --metadata-file /app/src/metadata/service_metadata.json \
    /app/src \
    trustlevel-service-4 \
    --group-name default_groups \
    --endpoints http://snetd:7001 \
    --fixed-price 0.5

# Add example service description
docker-compose exec snet-cli snet --print-traceback service metadata-add-description --json '{"description": "Description of my Service.", "url": "https://www.trustlevel.io/"}' \
    --metadata-file /app/src/metadata/service_metadata.json

## Publish example service org on Blockchain
docker-compose exec snet-cli snet service publish trustlevel-org-id-2 trustlevel-service-4 --metadata-file /app/src/metadata/service_metadata.json

## Retrieve org info
docker-compose exec snet-cli snet organization info trustlevel-org-id-2
```

## Additional information

### Token Transfers

#### Understanding the Payment Process:
Payment Channels: SingularityNET uses state channels for payments. When a client uses your service, they pay by sending a signed message agreeing to release a portion of their funds from a Multi-Party Escrow (MPE) account to you. This action doesn't immediately transfer tokens but updates the state of the payment channel.

Claiming Payments: The tokens remain in the MPE until you submit these signed messages to the blockchain to claim your payment. This process is what you did with the `snet treasurer claim-all` command.

Token Transfer: Once you claim the payments, the AGIX tokens should be transferred from the MPE account to your wallet address.

#### Problem only outgoing payments

Within the scope of this POC I have seen only outgoing payments from my wallet (0x19570fbC4e05940960b0A44C5f771008Af7935A2) to the Multi-Party Escrow (MPE) address of SingularityNET (0x6245F856EFFBDB3ED6a3c64385b27A78B42F65e1) and no incoming AGIX token transactions.

### Etherscans for test accounts in the wallet

#### ETH Transfers
https://goerli.etherscan.io/address/0x007692276fe8d9941FF9bB4f2CfE0047dD9EB406

#### AGIX Contract filtered by my wallet address
https://goerli.etherscan.io/token/0xdd4292864063d0DA1F294AC65D74d55a44F4766C?a=0x007692276fe8d9941ff9bb4f2cfe0047dd9eb406

####  Multi-Party Escrow (MPE) address of SingularityNET
https://goerli.etherscan.io/address/0x6245f856effbdb3ed6a3c64385b27a78b42f65e1

### Faucets
You can use the faucets to get ETH and AGIX in your testnet wallet.

__Note: To prevent bots and abuse, the Goerli faucet requires a minimum mainnet balance of 0.001 ETH on the wallet address being used__

#### AGIX
https://faucet.singularitynet.io/

#### ETH
https://goerlifaucet.com/

### Add AGIX to Metamask
https://blog.singularitynet.io/how-to-add-singularitynet-agix-tokens-to-your-wallet-db97ba727b8e

use address mentioned in: https://github.com/singnet/agix-contracts
