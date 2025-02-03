// import * as pulumi from "@pulumi/pulumi";
// import * as cloudflare from "@pulumi/cloudflare";
// import * as fs from "fs"
// import * as command from "@pulumi/command";

// const config = new pulumi.Config();
// const accountId = config.require("accountId");
// const domain = config.require("domain");

// const worker = new cloudflare.WorkersScript("worker-worker", {
//     accountId: accountId,
//     name: "worker-worker",
//     content: fs.readFileSync("worker.ts").toString(),
//     module: true, // ES6 module
// });


// const compileWorker = new command.local.Command("compile-worker", {
//     create:
//         "yarn run tsc >/dev/null && cat ./dist/index.js",
//     dir: "../serverless-cloudflare",
// });

// // index.ts
// const zone_libsurl = new cloudflare.Zone("libsurl.tv", {
//     zone: "libsurl.tv",
//     plan: "free",
//     accountId: accountId,
// });

// const zoneSettings = new cloudflare.ZoneSettingsOverride("pulumi.tv", {
//     zoneId: zone_libsurl.id,
//     settings: {
//         alwaysUseHttps: "on",
//         automaticHttpsRewrites: "on",
//         ssl: "strict",
//         minTlsVersion: "1.2",
//         universalSsl: "on",
//     },
// });

// const zone =  cloudflare.getZone({
//     name: "libsurl.tv",
// });

// const zoneId = zone.then(z => z.zoneId);
// // index.ts
// const record = new cloudflare.Record(
//     "libsurl.tv",
//     {
//         zoneId: zoneId,
//         name: "@",
//         type: "CNAME",
//         value: "libsurl.dev",
//         proxied: true,
//     },
//     {
//         deleteBeforeReplace: true,
//     }
// );

// const route = new cloudflare.WorkerRoute(
//     "pulumi.tv",
//     {
//         zoneId: zone.id,
//         pattern: pulumi.interpolate`${zone.zone}/*`,
//         scriptName: worker.name,
//     }
// );


// export const url = pulumi.interpolate`https://${record.hostname}`;


// index.ts
import * as pulumi from "@pulumi/pulumi";
import * as cloudflare from "@pulumi/cloudflare";
import * as fs from "fs";

const config = new pulumi.Config();
const accountId = config.require("accountId");
const domain = config.require("domain");
// Create a new Cloudflare Zone

const zone = cloudflare.getZone({
    accountId: accountId,
    name: domain
});
  

const zoneId = zone.then(z => z.zoneId);


// Create a Cloudflare Worker Script
const worker = new cloudflare.WorkerScript("lib", {
    name: "lib",
    content: fs.readFileSync("worker.js").toString(),
    accountId: accountId,
    module: true, // ES6 module
});



// Create a Worker Route to link the Worker to the Zone
const workerRoute = new cloudflare.WorkerRoute("lib-route", {
    zoneId: zoneId,
    pattern: pulumi.interpolate`${zone.zone}/*`,
    scriptName: worker.name,
});

// Export the URL of the deployed Worker
export const workerUrl = pulumi.interpolate`https://${zone.zone}`;
