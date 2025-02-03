// worker.js
const DEFAULT_URL = "https://youtube.com/pulumitv"

const redirects = {
  "pulumi.tv": {
    "modern-infrastructure": {
        to: "https://www.youtube.com/playlist?list=PLyy8Vx2ZoWloyj3V5gXzPraiKStO2GGZw"
    }
  },
};

addEventListener("fetch", async (event) => {
  event.respondWith(handleRedirect(event.request));
});

async function handleRedirect(request) {
  const requestUrl = new URL(request.url);
  const domain = requestUrl.host;
  const path = requestUrl.pathname.substring(1);

  console.log(`Handling request on domain ${domain} for ${path}`);

  if (!(domain in redirects)) {
    console.log(`Domain '${domain}' not found`);
    return Response.redirect(DEFAULT_URL);
  }

  if (path === "") {
    return Response.redirect(DEFAULT_URL);
  }

  const paths = redirects[domain];

  if (path in paths) {
    console.log(`Redirecting too ${paths[path].to}`);
    return Response.redirect(paths[path].to);
  }

  console.log(`Path '${path}' not found`);
  return Response.redirect(DEFAULT_URL);
}

