import * as pulumi from "@pulumi/pulumi";
import * as vault from "@pulumi/vault";

const config = new pulumi.Config();
const secretMessage = config.requireSecret("secretMessage");

secretMessage.apply(msg => {
    pulumi.log.info(`The secret using default config the message is: ${msg}`);
});

const mySecret = vault.kv.getSecret({
    path: "my-secret/my-secret"
});

mySecret.then(secret => {
    if (secret && secret.data && secret.data["my-key"]) {
        pulumi.log.info(`Retrieved secret value using vault: ${secret.data["my-key"]}`);
    } else {
        pulumi.log.error("Failed to retrieve 'my-key' from the secret.");
    }
});