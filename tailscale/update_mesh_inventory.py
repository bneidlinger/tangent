import requests, yaml, os

TAILSCALE_API_KEY = os.environ.get("TAILSCALE_API_KEY")
TAILSCALE_TAILNET = os.environ.get("TAILSCALE_TAILNET")  # e.g., brandon.tailscale.net
OUTPUT_YAML = "docs/mesh-inventory-auto.yaml"
OUTPUT_MD = "docs/mesh-inventory-auto.md"
OUTPUT_SVG = "docs/mesh-status.svg"

def get_tailscale_devices():
    url = f'https://api.tailscale.com/api/v2/tailnet/{TAILSCALE_TAILNET}/devices'
    r = requests.get(url, auth=(TAILSCALE_API_KEY, ''))
    r.raise_for_status()
    return r.json()['devices']

def device_to_dict(dev):
    ips = dev.get('addresses', [])
    return {
        'Name': dev['hostname'],
        'IP': ips[0] if ips else '',
        'OS': dev.get('os', ''),
        'User': dev.get('user', '').split('@')[0] if dev.get('user') else '',
        'Tags': ', '.join(dev.get('tags', [])),
        'Online': dev.get('online', False),
        'Last Seen': dev.get('lastSeen', '').replace('T', ' ')[:19] if dev.get('lastSeen') else '',
    }

def write_yaml(devices):
    with open(OUTPUT_YAML, 'w') as f:
        yaml.dump({'tailscale_mesh': devices}, f, default_flow_style=False)

def write_markdown(devices):
    header = "| Name | IP | OS | User | Tags | Online | Last Seen |\n"
    header += "|------|----|----|------|------|--------|-----------|\n"
    rows = []
    for dev in devices:
        row = f"| {dev['Name']} | {dev['IP']} | {dev['OS']} | {dev['User']} | {dev['Tags']} | {'✅' if dev['Online'] else '❌'} | {dev['Last Seen']} |"
        rows.append(row)
    md_table = header + '\n'.join(rows) + '\n'
    with open(OUTPUT_MD, 'w') as f:
        f.write("# Live Mesh Network Inventory (Auto-generated)\n\n")
        f.write(md_table)
        f.write("\n_Last updated automatically via Tailscale API_\n")

def write_svg_badge(devices):
    total = len(devices)
    online = sum(1 for d in devices if d['Online'])
    if online == total:
        color = "#3bff39"  # portal green
        status_emoji = "🌀"
        mascot = "🤖"  # Rick or Morty, you can use "🧑‍🔬" or "🧑‍🦱"
        status_text = "All Schwifty!"
    elif online == 0:
        color = "#fe2851"
        status_emoji = "💀"
        mascot = "😵"
        status_text = "Existence is Pain!"
    else:
        color = "#ffd600"
        status_emoji = "⚡"
        mascot = "😬"
        status_text = "Somewhere, Something's Screwed Up!"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="340" height="42">
  <defs>
    <radialGradient id="portal" cx="0.5" cy="0.4" r="1">
      <stop offset="0%" stop-color="#b5ff75"/>
      <stop offset="80%" stop-color="#37ff79" />
      <stop offset="100%" stop-color="#153519"/>
    </radialGradient>
    <filter id="portal-glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect rx="16" width="340" height="42" fill="url(#portal)" filter="url(#portal-glow)"/>
  <text x="33" y="30" font-family="monospace" font-size="32">{mascot}</text>
  <text x="68" y="28" font-family="monospace" font-size="19" font-weight="bold" fill="{color}">{status_emoji} {online}/{total} Mesh Nodes</text>
  <text x="68" y="39" font-family="monospace" font-size="13" fill="#00fff6">{status_text}</text>
  <text x="262" y="29" font-family="monospace" font-size="15" fill="#b4befe" opacity="0.82">Rick & Morty Mesh</text>
</svg>'''
    with open("docs/mesh-status.svg", "w") as f:
        f.write(svg)

def main():
    devices = get_tailscale_devices()
    parsed = [device_to_dict(dev) for dev in devices]
    write_yaml(parsed)
    write_markdown(parsed)
    write_svg_badge(parsed)
    print(f"✅ Inventory and badge written to {OUTPUT_YAML}, {OUTPUT_MD}, {OUTPUT_SVG}")

if __name__ == '__main__':
    main()
