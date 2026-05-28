#!/usr/bin/env node
/**
 * proxy.mjs — expose internal Docker services on the container's LAN IP
 *
 * Edit PORTS to add/remove services. Then run:
 *   node proxy.mjs
 *
 * Each entry forwards  <LAN_IP>:<port>  →  127.0.0.1:<port>
 * so the host machine can reach the service via the container IP.
 */

import net from "net";
import os from "os";

// ── Config ────────────────────────────────────────────────────────────────────
const PORTS = [
  { port: 3113, label: "agentmemory-viewer" },
  // { port: 8080, label: "my-app" },   ← add new services here
];
// ─────────────────────────────────────────────────────────────────────────────

function getLanIP() {
  for (const [name, addrs] of Object.entries(os.networkInterfaces())) {
    if (name === "lo") continue;
    for (const addr of addrs) {
      if (addr.family === "IPv4" && !addr.internal) return addr.address;
    }
  }
  return "0.0.0.0";
}

const LAN_IP = getLanIP();

for (const { port, label } of PORTS) {
  const server = net.createServer((src) => {
    const dst = net.connect(port, "127.0.0.1");
    src.pipe(dst);
    dst.pipe(src);
    dst.on("error", () => src.destroy());
    src.on("error", () => dst.destroy());
  });

  server.on("error", (err) => {
    console.error(`[proxy] ${label}:${port} error: ${err.message}`);
  });

  server.listen(port, LAN_IP, () => {
    console.log(`[proxy] ${label.padEnd(24)} ${LAN_IP}:${port} -> 127.0.0.1:${port}`);
  });
}
