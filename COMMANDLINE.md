# Create orga

```bash
docker-compose exec snet-cli snet organization create trustlevel-org-id --metadata-file /data/organization_metadata.json
Creating transaction to create organization name=trustlevel-org id=trustlevel-org-id

# Calculating gas price. It might take ~60 seconds.
# gas_price = 0.000015 GWei
    transaction:
        chainId: 5
        data: '0xef72a9af74727573746c6576656c2d6f72672d6964000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000040697066733a2f2f516d616d437652356a6a6767695076613171553848446d727464705243507241516773674a52747a55705338716900000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        from: '0x007692276fe8d9941FF9bB4f2CfE0047dD9EB406'
        gas: 191712
        gasPrice: 14568
        nonce: 0
        to: '0x0DD7feC305f2374d7eed35d6d28134936c025A7A'
        value: 0

Proceed? (y/n): y
Submitting transaction...

    event_summaries:
    -   args:
            orgId: 74727573746c6576656c2d6f72672d6964000000000000000000000000000000
        event: OrganizationCreated
    receipt_summary:
        blockHash: '0xe49006a46cb4cf5cea64502b5d6bc7a8d24db6a6b9092ae16f183cf55de07711'
        blockNumber: 10167417
        cumulativeGasUsed: 8306317
        gasUsed: 191712
        transactionHash: '0xe8706d0f9b8f5240dbdc64093da86ef7c1fbaab4d6f22c3633cfa934b25e1d67'

id:
trustlevel-org-id
```


# Publish service 

```bash
Snet_NewDocs docker-compose exec snet-cli snet service publish trustlevel-org-id trustlevel-service --metadata-file /app/src/metadata/service_metadata.json
# Calculating gas price. It might take ~60 seconds.
# gas_price = 0.000015 GWei
    transaction:
        chainId: 5
        data: '0xa4123f0f74727573746c6576656c2d6f72672d696400000000000000000000000000000074727573746c6576656c2d73657276696365000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000040697066733a2f2f516d646755506e3265335a66576274795656553174795253314275676344656a694e32776a36646773584e325a710000000000000000000000'
        from: '0x007692276fe8d9941FF9bB4f2CfE0047dD9EB406'
        gas: 166873
        gasPrice: 14881
        nonce: 1
        to: '0x0DD7feC305f2374d7eed35d6d28134936c025A7A'
        value: 0

Proceed? (y/n): y
Submitting transaction...

    event_summaries:
    -   args:
            metadataURI: 697066733a2f2f516d646755506e3265335a66576274795656553174795253314275676344656a694e32776a36646773584e325a710000000000000000000000
            orgId: 74727573746c6576656c2d6f72672d6964000000000000000000000000000000
            serviceId: 74727573746c6576656c2d736572766963650000000000000000000000000000
        event: ServiceCreated
    receipt_summary:
        blockHash: '0xdee25b1851e4987bc7ee30cc83988a91ce338df422747298c0094811e64d0762'
        blockNumber: 10167452
        cumulativeGasUsed: 9788128
        gasUsed: 166873
        transactionHash: '0xfc325bb9cf0df99b3ba51035ec6474f973b117cd429476d30afc4dae687d125a'
```

# Check service

```bash

docker-compose exec snet-cli snet organization info trustlevel-org-id

Organization Name:
 - b'ipfs://QmamCvR5jjggiPva1qU8HDmrtdpRCPrAQgsgJRtzUpS8qi\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

Organization Id:
 - trustlevel-org-id

Owner:
 - 0x007692276fe8d9941FF9bB4f2CfE0047dD9EB406

Services:
 - trustlevel-service

 ```