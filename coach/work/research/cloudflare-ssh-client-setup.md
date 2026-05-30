# SSH via Cloudflare Tunnel — Client Setup Guide

## Prerequisites

- Server (this PC) already has the Cloudflare Tunnel running
- Tunnel hostname: `ssh.midtech.ggff.net`
- Server SSH listening on port **2222**

**Note:** If the client PC is on the **same local network** as the server, you don't need the tunnel — just SSH directly:
```cmd
ssh -p 2222 hamid@192.168.1.147
```
The tunnel is only needed when connecting from **outside** your home/office network.

---

## Windows — Prerequisites

Windows 10/11 have OpenSSH built-in. Verify:
```cmd
ssh -V
```
If not found, install it:
- **Settings → Apps → Optional Features → Add a feature → OpenSSH Client → Install

## Step 1 — Install cloudflared on the client

### Windows
1. Download the latest Windows binary:
   - Open PowerShell as Admin and run:
   ```
   curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -o cloudflared.exe
   ```
2. Move it to a folder in your PATH (e.g., `C:\Windows\System32\`)
3. Verify: `cloudflared --version`

### macOS (Intel)
```
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz -o cloudflared.tgz
tar -xzf cloudflared.tgz
sudo mv cloudflared /usr/local/bin/
```

### macOS (Apple Silicon M1/M2/M3)
```
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz -o cloudflared.tgz
tar -xzf cloudflared.tgz
sudo mv cloudflared /usr/local/bin/
```

### Linux (any distro)
```
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/
```

---

## Step 1.5 — Cloudflare Zero Trust: Create an Access Application (one-time setup)

Before the client can authenticate, you need to create an **Access application** in the Cloudflare dashboard.

1. Go to [one.dash.cloudflare.com](https://one.dash.cloudflare.com/)
2. **Access → Applications → Add an application**
3. Choose **Self-hosted**
4. **Application name:** `SSH Tunnel` (or any name)
5. **Domain:** select your domain, **Subdomain:** `ssh` → auto-fills `ssh.midtech.ggff.net`
6. **Application logo** (optional) — skip
7. Click **Next**
8. **Policy name:** `Allow All` (or `My Users`)
9. **Action:** `Allow`
10. **Configure rules:** `Everyone` → `Everyone` (or restrict to your email if you prefer)
11. Click **Next**
12. **Cross-Origin headers** — skip (leave defaults)
13. Click **Add application**

That's it. The Access app is now linked to your tunnel hostname. Users will authenticate via their Cloudflare login before SSH traffic passes through.

---

## Step 2 — Authenticate with Cloudflare (on the client)

Run this on the **client** PC (only once):
```
cloudflared tunnel login
```

This will:
- Open a browser window
- Ask you to log in to Cloudflare
- Ask you to select which domain to authorize (select `midtech.ggff.net` or whereever the tunnel hostname is)
- Save a certificate to `~/.cloudflared/cert.pem`

If no browser opens, it will give you a URL — open it manually in a browser.

---

## Step 3 — Connect via SSH

### Method A: One-liner (recommended for occasional use)

Run this every time you want to SSH:
```
cloudflared access ssh --hostname ssh.midtech.ggff.net --destination localhost:2222
```

Then open a **second terminal** and SSH as usual:
```
ssh -p 2222 hamid@localhost
```

The first terminal keeps the tunnel open. When done, press `Ctrl+C` to close it.

### Method B: Persistent SSH config (recommended for frequent use)

Add this to `~/.ssh/config` on the client:
```
Host remote-tunnel
    HostName localhost
    Port 2222
    User hamid
    ProxyCommand cloudflared access ssh --hostname ssh.midtech.ggff.net --destination localhost:2222
```

Then connect with just:
```
ssh remote-tunnel
```

This automatically starts the tunnel, connects, and closes it when done.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `cloudflared` not found | Check it's installed and in PATH. Restart terminal. |
| `login` opens browser but nothing happens | Copy the URL from terminal and open manually |
| `failed to connect to origin` | Server tunnel might be down — check server: `systemctl status cloudflared` |
| `access denied` / `403` | Cloudflare Access application not set up for this hostname — contact server admin |
| Connection hangs / timeout | Try: `cloudflared access tcp --hostname ssh.midtech.ggff.net --url localhost:2222` instead |
| SSH asks for password | Use your server login password (same as when you SSH locally on the server) |

---

## Quick check — is the tunnel alive?

Ask someone on the server to run:
```
systemctl status cloudflared
```
Look for `active (running)`. Then check:
```
cloudflared tunnel list
```
The `myssh` tunnel should show `CONNECTIONS` with active entries.
