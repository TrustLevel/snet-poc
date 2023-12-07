## etcd

```bash
docker-compose build etcd
```

## snet cli

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

## Identity and Org setup

```bash
docker-compose up -d snet-cli

# create identity
docker-compose exec snet-cli snet identity create trustlevel-test-2 key --private-key <metamask-private-key> --network goerli

# Output
#You've just added your first identity trustlevel-test. We will automatically switch to it!
#Identity "trustlevel-test" is bind to network "goerli"
#Switch to network: goerli
#Switch to identity: trustlevel-test

# Create organization
docker-compose exec snet-cli snet organization metadata-init trustlevel-org trustlevel-org-id-2 individual --metadata-file /data/organization_metadata.json

# Add description
docker-compose exec snet-cli snet organization metadata-add-description --description "Trustlevel long description" --short-description  "Trustlevel short description" --url "https://www.trustlevel.io/" --metadata-file /data/organization_metadata.json

# Add default group connected with internal etcd
# https://docs.google.com/document/d/1jkkIMvUObSc81Cv3WXl9wtjFwt-itFSaOctyGdPg_30/edit#heading=h.ovkzit52gx4v
docker-compose exec snet-cli snet organization add-group default_groups 0x007692276fe8d9941FF9bB4f2CfE0047dD9EB406 http://etcd:2379 --metadata-file /data/organization_metadata.json

## CREATE ORG on Blockchain
docker-compose exec snet-cli snet organization create trustlevel-org-id-2 --metadata-file /data/organization_metadata.json

## DELETE
docker-compose exec snet-cli snet organization delete trustlevel-org-id

```

# Service

```bash

# /app/src is mounted into snet-cli
docker-compose exec snet-cli snet --print-traceback service metadata-init \
    --metadata-file /app/src/metadata/service_metadata.json \
    /app/src \
    trustlevel-service-3 \
    --group-name default_groups \
    --endpoints http://snetd:7001 \
    --fixed-price 0.00000001

# Add description
docker-compose exec snet-cli snet --print-traceback service metadata-add-description --json '{"description": "Description of my Service.", "url": "https://www.trustlevel.io/"}' \
    --metadata-file /app/src/metadata/service_metadata.json


docker-compose exec snet-cli snet service publish trustlevel-org-id-2 trustlevel-service-3 --metadata-file /app/src/metadata/service_metadata.json


docker-compose exec snet-cli snet organization info trustlevel-org-id-2
```

# Deamon

Note: etcd must run externally because the embedded one can not be emulated due to arm64 architecture

```bash
docker-compose up -d snetd
```

# Calling service with snet-cli

```bash
docker-compose up -d grpc-server

docker-compose exec snet-cli snet account deposit 0.000001

docker-compose exec snet-cli snet channel open-init trustlevel-org-id-2 default_groups 0.000001 +2days

docker-compose exec snet-cli snet client call trustlevel-org-id-2 trustlevel-service-3 default_groups call '{"query":"Hello Josch"}'

# claim payments https://docs.google.com/document/d/1jkkIMvUObSc81Cv3WXl9wtjFwt-itFSaOctyGdPg_30/edit#heading=h.r684e4ffzwng
docker-compose exec snet-cli snet treasurer claim-all --endpoint http://snetd:7001

# OR set gas price to overcome err: max fee per gas less than block base fee

docker-compose exec snet-cli snet treasurer claim-all --endpoint http://snetd:7001 --gas-price 100000000000

# Client close channels: https://docs.google.com/document/d/1jkkIMvUObSc81Cv3WXl9wtjFwt-itFSaOctyGdPg_30/edit#heading=h.y464yvlwwaa4
docker-compose exec snet-cli snet channel claim-timeout-all
```

# Token Transfers

## Understanding the Payment Process:
Payment Channels: SingularityNET uses state channels for payments. When a client uses your service, they pay by sending a signed message agreeing to release a portion of their funds from a Multi-Party Escrow (MPE) account to you. This action doesn't immediately transfer tokens but updates the state of the payment channel.

Claiming Payments: The tokens remain in the MPE until you submit these signed messages to the blockchain to claim your payment. This process is what you did with the `snet treasurer claim-all` command.

Token Transfer: Once you claim the payments, the AGIX tokens should be transferred from the MPE account to your wallet address.

## Problem only outgoing payments

If you're only seeing outgoing payments from your wallet (0x19570fbC4e05940960b0A44C5f771008Af7935A2) to the Multi-Party Escrow (MPE) address of SingularityNET (0x6245F856EFFBDB3ED6a3c64385b27A78B42F65e1) and no incoming AGIX token transactions, it suggests a few possibilities:

### Gas Costs Exceeding Claim Amounts:

As previously discussed, if the gas cost for claiming AGIX tokens is higher than the amount being claimed, you might end up with a net outflow of Ether (ETH) from your wallet with no visible increase in AGIX tokens. This is more likely if the claimed AGIX amount is small.

## Etherscans

### ETH Transfers
https://goerli.etherscan.io/address/0x007692276fe8d9941FF9bB4f2CfE0047dD9EB406

### AGIX Contract filtered by my wallet address
https://goerli.etherscan.io/token/0xdd4292864063d0DA1F294AC65D74d55a44F4766C?a=0x007692276fe8d9941ff9bb4f2cfe0047dd9eb406

###  Multi-Party Escrow (MPE) address of SingularityNET
https://goerli.etherscan.io/address/0x6245f856effbdb3ed6a3c64385b27a78b42f65e1

# Faucets
You can use the faucets to get ETH and AGIX in your testnet wallet.

__Note: To prevent bots and abuse, the Goerli faucet requires a minimum mainnet balance of 0.001 ETH on the wallet address being used__

## AGIX
https://faucet.singularitynet.io/

## ETH
https://goerlifaucet.com/

# Add AGIX to Metamask
https://blog.singularitynet.io/how-to-add-singularitynet-agix-tokens-to-your-wallet-db97ba727b8e

use address mentioned in: https://github.com/singnet/agix-contracts
