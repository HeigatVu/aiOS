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

// Rewrite Host header so the dashboard's loopback-only allowlist accepts the
// request. Without this the server returns 421 Misdirected Request.
function rewriteHostHeader(buf, lanIP, port) {
  const str = buf.toString("binary");
  const headerEnd = str.indexOf("\r\n\r\n");
  if (headerEnd === -1) return buf; // incomplete — pass through unchanged
  const headers = str.slice(0, headerEnd);
  const body = str.slice(headerEnd);
  const rewritten = headers.replace(
    new RegExp(`^Host: ${lanIP.replace(/\./g, "\\.")}:${port}\\r?$`, "im"),
    `Host: localhost:${port}`
  );
  return Buffer.from(rewritten + body, "binary");
}

const server = net.createServer((src) => {
  const dst = net.connect(TARGET_PORT, TARGET_HOST);
  let firstChunk = true;

  src.on("data", (chunk) => {
    if (firstChunk) {
      firstChunk = false;
      chunk = rewriteHostHeader(chunk, LISTEN_HOST, LISTEN_PORT);
    }
    dst.write(chunk);
  });
  dst.pipe(src);
  dst.on("error", () => src.destroy());
  src.on("error", () => dst.destroy());
});

server.listen(LISTEN_PORT, LISTEN_HOST, () => {
  console.log(`[dashboard-proxy] ${LISTEN_HOST}:${LISTEN_PORT} -> ${TARGET_HOST}:${TARGET_PORT} (host-rewrite enabled)`);
});
