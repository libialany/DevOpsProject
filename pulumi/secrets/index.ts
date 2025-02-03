// import * as pulumi from "@pulumi/pulumi";
// const vault = require("@pulumi/vault");

// // const cfg = new pulumi.Config();
// // const secretMessage = cfg.requireSecret("secretMessage");
// // pulumi.log.info(`Secret Message using  default config: ${secretMessage}`);

// // Retrieve the secret from Vault
// const mySecret = vault.kv.getSecret("my-secret/my-secret");

// // Log the secret value (masked)
// pulumi.log.info(`Secret value masked using vault: ${mySecret.data["my-key"]}`);

// // If you want to print it in a secure way, use requireSecret
// const secretValue = pulumi.secret(mySecret.data["my-key"]);
// pulumi.log.info(`Secret value in a secure way using vault: ${secretValue}`);
// // ... existing code ...


import * as pulumi from "@pulumi/pulumi";
import * as vault from "@pulumi/vault";

const config = new pulumi.Config();
const secretMessage = config.requireSecret("secretMessage");

secretMessage.apply(msg => {
    pulumi.log.info(`The secret using default config the message is: ${msg}`);
});
// Retrieve the secret
// ... existing code ...

// Retrieve the secret with the correct argument type
const mySecret = vault.kv.getSecret({
    path: "my-secret/my-secret"
});

// ... existing code ...

// Use apply to handle the asynchronous nature of secret retrieval
mySecret.then(secret => {
    // Check if 'data' exists and contains 'my-key'
    if (secret && secret.data && secret.data["my-key"]) {
        pulumi.log.info(`Retrieved secret value using vault: ${secret.data["my-key"]}`);
    } else {
        pulumi.log.error("Failed to retrieve 'my-key' from the secret.");
    }
});