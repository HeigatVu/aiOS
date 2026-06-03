import http from "http";
import os from "os";

const LISTEN_PORT = 9119;
const TARGET_HOST = "127.0.0.1";
const TARGET_PORT = 9119;

function getContainerIP() {
  const ifaces = os.networkInterfaces();
  for (const [name, addrs] of Object.entries(ifaces)) {
    if (name === "lo") continue;
    for (const addr of addrs) {
      if (addr.family === "IPv4" && !addr.internal) return addr.address;
    }
  }
  return "0.0.0.0";
}

const LISTEN_HOST = getContainerIP();

const server = http.createServer((clientReq, clientRes) => {
  const options = {
    hostname: TARGET_HOST,
    port: TARGET_PORT,
    path: clientReq.url,
    method: clientReq.method,
    headers: {
      ...clientReq.headers,
      host: `localhost:${TARGET_PORT}`,
    },
  };

  const proxyReq = http.request(options, (proxyRes) => {
    clientRes.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(clientRes);
  });

  proxyReq.on("error", (err) => {
    clientRes.writeHead(502);
    clientRes.end("Proxy error");
  });

  clientReq.pipe(proxyReq);
});

server.listen(LISTEN_PORT, LISTEN_HOST, () => {
  console.log(
    `[dashboard-proxy] ${LISTEN_HOST}:${LISTEN_PORT} -> ${TARGET_HOST}:${TARGET_PORT} (host-rewrite enabled)`
  );
});
