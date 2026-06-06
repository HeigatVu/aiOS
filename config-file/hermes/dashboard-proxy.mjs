import http from "http";
import net from "net";
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
    if (!clientRes.headersSent) {
      clientRes.writeHead(502);
    }
    clientRes.end("Proxy error");
  });

  clientReq.pipe(proxyReq);
});

// Handle WebSocket upgrade connections — the http.createServer callback
// above does NOT fire for upgrade requests; the 'upgrade' event is needed.
server.on("upgrade", (clientReq, clientSocket, head) => {
  // Forward the upgrade request to the dashboard
  const proxySocket = net.connect(TARGET_PORT, TARGET_HOST, () => {
    // Replay the HTTP upgrade request to the backend
    const headers = [];
    for (const [key, val] of Object.entries(clientReq.headers)) {
      headers.push(`${key}: ${val}`);
    }
    const reqLine = `${clientReq.method} ${clientReq.url} HTTP/1.1\r\n`;
    const headerBlock = headers.join("\r\n") + "\r\n";
    proxySocket.write(reqLine + headerBlock + "\r\n");

    // Forward any data already read by the HTTP parser (rare for upgrade)
    if (head && head.length > 0) {
      proxySocket.write(head);
    }

    // Bidirectional pipe
    proxySocket.pipe(clientSocket);
    clientSocket.pipe(proxySocket);
  });

  proxySocket.on("error", (err) => {
    clientSocket.destroy();
  });

  clientSocket.on("error", (err) => {
    proxySocket.destroy();
  });
});

server.listen(LISTEN_PORT, LISTEN_HOST, () => {
  console.log(
    `[dashboard-proxy] ${LISTEN_HOST}:${LISTEN_PORT} -> ${TARGET_HOST}:${TARGET_PORT} (host-rewrite enabled, WS upgrade supported)`
  );
});
