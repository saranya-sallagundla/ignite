# Topic 5 — Linux — Networking Fundamentals

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).
> Two-day topic per the roadmap, compressed into one session — see the Verdict for why the
> official score reflects a same-session revision pass.

---

## Day 1 — 2026-07-14 (both days, single session)

Note on pacing: both days were intentionally kept high-level/faster-paced the first time through,
per an explicit request to move quickly and expand only on request. The material didn't fully
land on the first pass, so a full second revision pass (with a simpler analogy table, extra
concept-check questions, real-world scenario questions, and genuine hands-on verification) was
done in the same session, right after — that full second pass is included below in detail, since
it's where real understanding actually solidified.

### Today's agenda
1. The mail analogy — the core mental model.
2. IP addresses — private vs. public.
3. CIDR notation.
4. Ports.
5. DNS.
6. Routing.
7. Firewalls (conceptual).
8. Combined scenario — unreachable service diagnostic.
9. `curl` hands-on — refused/no-route/timed-out.
10. The quiz, plus a revision pass and retest.

### 1. The mail analogy — the core mental model

Expanded during the revision pass with a "real example from today" column, tying each analogy
directly to something actually run/observed this session:

| Concept | Mail-world analogy | Real example from today |
|---|---|---|
| **IP address** | The street address of a building (which specific machine) | `192.168.180.212` — this machine's own `eth0` address |
| **Port** | The apartment/suite number at that address (which specific application on that machine — one machine can run many services, each on its own port) | `ss -tuln`'s `Local Address:Port` column (Topic 2) |
| **DNS** | The phone book — translates a human-friendly name into the actual address | `dig google.com` returning six real IPs for one name |
| **Routing** | The postal system deciding which roads/hubs a letter passes through | `ip route` showing the actual hop-out gateway |
| **TCP vs UDP** | Registered mail with delivery confirmation and reordering (TCP) vs. a postcard dropped in the mail with no guarantee (UDP) | `ss -tuln`'s separate TCP/UDP rows |
| **Firewall** | A security guard at the building who can still turn a visitor away, even if the right apartment (port) is genuinely occupied | the corporate-proxy TCP blocks from Topics 1/2/4 |
| **Private IP** | An internal apartment/mailroom number only meaningful inside one building, not a real postal address | `192.168.x.x` — not directly reachable from outside |
| **Public IP** | The building's real street address, the one the outside postal system actually uses | the router's one shared address after NAT |
| **Ping/ICMP** | Knocking on the building's front door just to check someone's home — says nothing about which apartment/suite answers | `ping` succeeding while a specific port stays unreachable |
| **TCP/UDP + port check** | Actually asking for a specific apartment by number, not just checking if the building has anyone home at all | `ss -tuln` / `curl` against a specific port |

### 2. IP addresses — private vs. public

**IPv4 format**: four octets (0-255), dot-separated, e.g. `192.168.1.10`.

**Private ranges** (usable only inside a local network, never globally unique, never directly
reachable from the internet):
| Range | Starts with |
|---|---|
| `10.0.0.0/8` | `10.x.x.x` |
| `172.16.0.0/12` | `172.16.x.x` through `172.31.x.x` **inclusive** — `172.32.x.x` and above are already public |
| `192.168.0.0/16` | `192.168.x.x` |

**Quick check method**: starts with `10` → private. Starts with `192.168` → private. Starts with
`172`, second number between **16 and 31 inclusive** → private (the one range people get wrong —
only that specific 16-31 slice is reserved, not all of `172.x.x.x`). Anything else → public.

**Why private IPs can still reach the internet — NAT**: routers **translate** ("NAT" — Network
Address Translation) between a machine's private IP and a shared public IP whenever traffic
actually leaves the local network for the internet. This is why a machine can have a private,
non-globally-unique address and still browse the web — the router swaps addresses at the
boundary, so the outside world only ever sees the router's one public IP, not every private
device behind it.

**A third category, distinct from both private and public — reserved/special addresses**:
- **`127.0.0.0/8`** (loopback, `127.0.0.1` being the common one) — reserved to mean "this same
  machine, talking to itself." Never routable to any other machine, on any network. Not private
  (i.e., not an address meant for use on a LAN), not public (not usable on the internet either) —
  a pure self-reference.
- **`0.0.0.0`** — a wildcard/unspecified address. Not a real destination at all. Meaningful only
  as (1) a *bind* address meaning "accept connections on every interface," or (2) in a routing
  table meaning "the default route for anything unmatched."

**Syntax**: `ip addr show [dev IFACE]`

**Verified hands-on**: `ip addr show` on this WSL2 machine:
```
1: lo: <LOOPBACK,UP,LOWER_UP> ...
    inet 127.0.0.1/8 scope host lo
    inet 10.255.255.254/32 brd 10.255.255.254 scope global lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    inet 192.168.180.212/20 brd 192.168.191.255 scope global eth0
```
- `192.168.180.212` — private (`192.168.x.x` rule). **First guess on this one was actually
  "public"** — corrected by walking through the octets digit-by-digit against the private-range
  rules above until `192.168` was matched.
- `10.255.255.254` — private range, but `/32` (see below) — WSL2's internal Windows↔WSL2 bridge
  address, not a real "network."
- `127.0.0.1` — reserved loopback, this machine talking to itself.

### 3. CIDR notation

An IPv4 address is 32 bits total. The number after `/` = how many bits are the fixed **network**
portion; the rest are free **host** bits. Addresses available = `2^(host bits)`.

**Full reference table built during the session** (extended past what was originally taught, up
to `/1`, since it clarified the whole pattern):
| CIDR | Host bits free | Addresses |
|---|---|---|
| `/32` | 0 | 1 |
| `/28` | 4 | 16 |
| `/24` | 8 | 256 |
| `/22` | 10 | 1,024 |
| `/20` | 12 | 4,096 |
| `/16` | 16 | 65,536 |
| `/12` | 20 | 1,048,576 |
| `/8` | 24 | 16,777,216 |
| `/1` | 31 | 2,147,483,648 |
| `/0` | 32 | 4,294,967,296 (entire IPv4 space) |

**Rule of thumb**: smaller number after `/` = bigger network (more host bits free = more
addresses). `/32` = exactly one specific host, not a range at all — used for point-to-point/
internal addressing (this is what explained `10.255.255.254/32` above).

**Verified/reasoned through, hands-on**:
- `/24` → 8 host bits free → 256 addresses (confirmed via `2^8`)
- `/16` → 16 host bits free → 65,536 addresses (confirmed via `2^16`)
- `/28` → 4 host bits free → 16 addresses (confirmed via `2^4`, corrected after an initial slip)
- `/12` → 20 host bits free → 1,048,576 addresses (`172.16.5.20/12` example, correctly identified
  as private AND correctly computed the address count in the same answer)
- `/1` → 31 host bits free → 2,147,483,648 addresses — extremely rare in practice, only relevant
  at very high-level internet routing infrastructure, not something normally configured directly

**Real-world scenario, reasoned through correctly**: sizing a subnet for ~20 office devices →
`/24` (256 addresses) chosen over `/28` (only 16 — wouldn't even fit today's 20 devices, let
alone allow growth) — correct reasoning: room to grow matters, not just today's exact count.

### 4. Ports

A port identifies which specific application on a machine you're talking to (the "apartment
number"). Range: **0-65535**. Well-known ports (0-1023): `22` = SSH, `80` = HTTP, `443` = HTTPS,
`53` = DNS. Full destination written as `IP:PORT`.

**Syntax**: `ss -tuln` — show listening sockets. `-t` TCP, `-u` UDP, `-l` listening only,
`-n` numeric (skip name resolution).

**Verified hands-on**:
```
$ ss -tuln
udp    UNCONN  0  0     127.0.0.54:53          0.0.0.0:*
udp    UNCONN  0  0  127.0.0.53%lo:53          0.0.0.0:*
udp    UNCONN  0  0  10.255.255.254:53          0.0.0.0:*
udp    UNCONN  0  0      127.0.0.1:323          0.0.0.0:*
tcp    LISTEN  0  4096  127.0.0.53%lo:53         0.0.0.0:*
tcp    LISTEN  0  511      127.0.0.1:43211       0.0.0.0:*
tcp    LISTEN  0  4096   127.0.0.54:53          0.0.0.0:*
tcp    LISTEN  0  1000  10.255.255.254:53         0.0.0.0:*
```
Port `53` (DNS) listening multiple times across different local addresses — this is
`systemd-resolved`, a local DNS resolver stub that forwards real lookups to an upstream DNS
server. Shows up on **both UDP and TCP**: UDP for the common case (small, fast queries, no
handshake overhead); TCP as a fallback specifically when a response is too large for one UDP
packet (server sets a "truncated" flag, client retries the same query over TCP for reliable
multi-packet delivery).

**`0.0.0.0` vs `127.0.0.1` as a *bind* address — the practical difference, worked through with
real correction needed**:
- **`127.0.0.1`** bind → app accepts connections **only from the same machine**, not from any
  other machine, not even ones on the same local network.
- **`0.0.0.0`** bind → app accepts connections from **every interface the machine has** — local
  network and internet too, if a public IP and open firewall exist. Not itself "the public IP" —
  more like "don't restrict which interface, accept on all of them."
- **Real consequence**: if an app binds to `127.0.0.1:8080` instead of `0.0.0.0:8080`,
  `ss -tuln` will still show it as "listening" — but literally no one else, from anywhere, can
  ever reach it. Not a firewall issue at all — the app is genuinely "listening to itself" only,
  a binding-address choice, not a network block. This is a very common real bug: a dev server
  works fine locally (`localhost` = `127.0.0.1`) then mysteriously "doesn't work" once deployed
  for others, purely because the bind address was never changed to `0.0.0.0`.

### 5. DNS

**Syntax**: `dig DOMAIN` (or `nslookup DOMAIN`) — query DNS, show the resolved IP(s).

**Verified hands-on** — had to install `bind9-dnsutils` first (`dig`/`nslookup` weren't present):
```
$ sudo apt update && sudo apt install -y bind9-dnsutils
... (full successful install of 6 packages from archive.ubuntu.com / security.ubuntu.com) ...
Error: Timeout was reached      (appeared twice, after the update and after the install)
```
**Real discovery, distinct from Topic 1's SSH block**: unlike Topic 1's fully-blocked
`openssh-server` install, this `apt install` **fully succeeded** — all 6 packages fetched and
configured with no errors in the actual package-fetch/install steps. The `Error: Timeout was
reached` lines appeared to come from a **separate background check** (most likely Ubuntu's
Pro/ESM service-status hook, which pings a different Canonical endpoint on every `apt`
operation), not from the main package mirrors (`archive.ubuntu.com`, `security.ubuntu.com`)
themselves. Working theory, not yet fully confirmed via `pro status`/`apt-config dump | grep -i
esm` — **left as an open thread to verify later** if revisited. Real lesson either way: this
network's block is more surgical than a blanket block — some endpoints reachable, others not,
same shape as prior corporate-network discoveries but even narrower here.

```
$ dig google.com
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 63230
;; ANSWER SECTION:
google.com.  221  IN  A  142.250.134.138
google.com.  221  IN  A  142.250.134.100
google.com.  221  IN  A  142.250.134.139
google.com.  221  IN  A  142.250.134.102
google.com.  221  IN  A  142.250.134.113
google.com.  221  IN  A  142.250.134.101
;; SERVER: 10.255.255.254#53(10.255.255.254) (UDP)
;; Query time: 32 msec
```
- `status: NOERROR` — query succeeded.
- Six `A` records in the `ANSWER SECTION` — six different IPs returned for one name.
- `SERVER: 10.255.255.254#53` — confirms this query went through the local `systemd-resolved`
  stub identified in `ss -tuln` above.
- `(UDP)` on the `SERVER` line — confirms UDP was actually used for this query (not inferred from
  speed; `Query time: 32 msec` is just typical for a fast UDP round-trip, not proof by itself).

**Round-robin DNS — why multiple IPs for one name**: large-scale services run many identical
servers behind the scenes; DNS hands out multiple valid IPs so that (1) load is spread across
different servers instead of all requests hitting one machine, and (2) if one server/IP goes
down, the client can simply try the next IP in the list — real failover without any special
client logic. Same underlying idea as AWS load balancers (Topic 24), just implemented via DNS
instead of a dedicated device.

**Real-world scenario, reasoned through**: a company migrates its website to a new server with a
different IP. What actually needs to change: the domain's **DNS "A record"** — the name-to-IP
mapping — gets updated to point at the new IP; nothing else about the domain changes. Users never
notice, because they always type the *name*, and their machine looks up the current IP fresh via
DNS every time — once the record updates, the next lookup simply returns the new address. Real
caveat: DNS changes take time to fully propagate, since some users may briefly get a cached
answer until it expires (why migrations plan a low TTL in advance) — a deeper detail flagged but
not gone into further this session.

**Contrast — single IP vs. multiple**: a small app returning just one IP from `dig` isn't a
problem by itself — it's proportional to scale, not a defect. The real tradeoff: **no built-in
redundancy** — if that one server goes down, the whole app becomes unreachable, unlike a
multi-IP round-robin setup which can route around a single failed server.

### 6. Routing

When sending data outside the local network, a machine forwards it to its **default gateway**
(usually the router), which forwards it toward its next hop, and so on.

**Syntax**: `ip route` — show the routing table.

**Verified hands-on**:
```
$ ip route
default via 192.168.176.1 dev eth0 proto kernel
192.168.176.0/20 dev eth0 proto kernel scope link src 192.168.180.212
```
`default via 192.168.176.1` = the gateway used for anything outside the local network (the
"local post office"). Second line = the local subnet, reachable directly without going through
the gateway at all, matching the `/20` identified earlier for `eth0`.

(`traceroute` — would show every hop a packet takes to a destination — mentioned conceptually,
not installed/run this session, kept at a lighter pace by request.)

### 7. Firewalls (brief, conceptual only)

A firewall decides which traffic is allowed in/out, based on rules matching IP/port/protocol.
Traditional Linux tool: `iptables`; its modern kernel-level replacement: `nftables`; simpler
front-ends built on top of either: `ufw`, `firewalld`. Not gone hands-on here — the key point
kept: **every silent "timed out" hit across this whole program (Topics 1, 4, and today) is a
firewall decision somewhere in the path**, whether on the local machine, the corporate network, or
the remote server — "connection refused," by contrast, actively rules a firewall block out (see
§9's key takeaway below).

### 8. Combined scenario — unreachable service, full diagnostic order

**Scenario**: a teammate can't reach an app at `10.0.1.15:8080` (later re-posed as
`10.0.2.20:5000` during the retest). Full diagnostic sequence, reasoned through correctly (with
guidance) across both passes:

1. **`ping` the IP** — basic reachability check. Correctly identified that `ping` succeeding does
   **not** prove port 8080 is reachable (ICMP vs. TCP/UDP are independently controlled — same
   lesson as Topic 2's ICMP-vs-TCP firewall discovery).
2. **`ss -tuln` on the server itself** (not the teammate's machine) — confirms whether the app is
   actually listening on that port at all.
3. **If listening but still unreachable, two distinct possible causes**:
   - **Firewall/security group blocking the port** — most common cause. Blocks at the **network
     level**.
   - **App bound to `127.0.0.1` instead of `0.0.0.0`** — app-level config choice, not a network
     block at all. The app is genuinely "listening to itself" only.

### 9. `curl` hands-on — distinguishing refused / no-route / timed-out (real verification)

**Syntax**: `curl -v [--max-time N] URL`

Real commands run to observe the actual different failure signatures, not just described:

**Refused — target reachable, nothing listening on that port**:
```
$ curl -v http://127.0.0.1:9999
* connect to 127.0.0.1 port 9999 from 127.0.0.1 port 45348 failed: Connection refused
* Failed to connect to 127.0.0.1 port 9999 after 2 ms: Couldn't connect to server
```
Instant (2 ms) — the OS itself actively said "nothing is listening here" (a TCP `RST`).

**No route to host — a third, distinct category**:
```
$ curl -v --max-time 5 http://192.168.180.250
* connect to 192.168.180.250 port 80 from 192.168.180.212 port 57320 failed: No route to host
* Failed to connect to 192.168.180.250 port 80 after 3072 ms: Couldn't connect to server
```
`192.168.180.250` is actually on the same local subnet as this machine (`192.168.176.0/20`
covers `192.168.176.0`–`192.168.191.255`, and `.180.x` falls inside that range) — so no gateway
is ever consulted at all for this destination; it's an on-link lookup. The real cause: the local
machine tried to resolve that address via ARP ("who has this IP on our local network?") and
nothing answered, so the local kernel itself gave up and returned "No route to host" — an active
local error, distinct from both a remote refusal and a silent firewall drop, but still not
involving the destination machine at all.

**Full comparison table, built from the two real tests above (timeout is the theoretical third
case, matching prior corporate-proxy discoveries — not separately re-tested this session)**:
| Result | What actually happened | Response time (observed) |
|---|---|---|
| **Connection refused** | Target machine reachable, nothing listening on that port | Instant — 2 ms |
| **No route to host** | Network itself can't find the destination at all | Fast-ish, active — 3072 ms |
| **Connection timed out** | Total silence, no response of any kind — classic firewall silently dropping packets | Slow — waits the full timeout with nothing back (this is the shape of the Topic 1/4 corporate-proxy blocks) |

**Wrong first guess, corrected**: asked what a "connection refused" result on port 443 implies,
the first answer was "may be a firewall issue" — backwards from the actual lesson. Corrected
before landing on the rule below.

**Key takeaway**: "refused" **rules in** "nothing listening on that port" and **rules out** a
*silently-dropping* firewall specifically, since that kind of firewall drops the packet rather
than sending an active refusal back — that case shows up as "timed out" instead, which is exactly
why it's the hardest of the three to diagnose (no information at all comes back). Caveat worth
knowing: a firewall configured to **REJECT** (rather than DROP) also sends an active refusal back,
indistinguishable from "nothing listening" at the client — so "refused" only rules out a *silent*
firewall block, not every firewall. Every block seen so far in this course (corporate proxies,
cloud security groups) has been the silent-DROP kind, which is why the simpler rule held up here.

---

## Topic 5 Quiz — both days combined — Attempt 1: PASS, 74/100, voluntary retest: PASS, 82/100 (official)

The retest score is used as the official record, since it reflects deeper, hands-on-verified
understanding reached after the revision pass.

### Attempt 1 — PASS, 74/100

Interview-style, open-ended, 4 questions (kept shorter, matching the session's faster pace).
Question and full correct answer for each:

1. **CIDR `/24` vs `/16` — why does the smaller number after the `/` mean a bigger network?**
   The number after the `/` is how many of the 32 total bits in an IPv4 address are the fixed
   **network** portion; the rest are free **host** bits, and the number of addresses available
   equals `2^(host bits)`. A `/24` leaves 8 host bits free → `2^8` = 256 addresses. A `/16` leaves
   16 host bits free → `2^16` = 65,536 addresses. Because host bits free = 32 − network bits, a
   *smaller* number after the `/` leaves *more* bits free for hosts, which means *more* addresses —
   i.e. a bigger network. That's why `/16` is a much larger network than `/24`, even though 16 is
   numerically less than 24.

2. **Round-robin DNS — why does `google.com` return 6 different IPs from one `dig` query?**
   Large-scale services run many identical servers behind the scenes, and DNS hands out multiple
   valid IPs for the one name so that (1) load is spread across different servers instead of every
   request hitting the same machine, and (2) if one server/IP goes down, the client can simply try
   the next IP in the list — real failover with no special client-side logic required. This
   pattern is called **round-robin DNS**. The `dig google.com` output demonstrated it directly: a
   single query returned six separate `A` records (six IPs) for the same name.

3. **Why doesn't `ping` succeeding prove that a specific port (e.g. `8080`) is reachable?**
   `ping` uses **ICMP**, a protocol completely separate from the TCP/UDP traffic that actual
   applications use. A firewall, security group, or host can allow ICMP through while blocking a
   specific TCP/UDP port (or vice versa) — the two are controlled independently. So a successful
   ping only proves the machine itself responds at the network layer; it says nothing about
   whether any particular application/port is listening or reachable. Confirming a port requires
   checking that port and protocol specifically (e.g. `ss -tuln` on the server, or a direct
   connection attempt like `curl` against that port).

4. **Two root causes for "the port is listening but the service is still unreachable," and how do
   they differ?**
   - **Firewall/security group blocking the port** — a **network-level** block. Something along
     the path (local firewall, corporate network, cloud security group) stops the traffic before
     it ever reaches the app, even though the app itself is fine and listening.
   - **App bound to `127.0.0.1` instead of `0.0.0.0`** — an **app-level** configuration choice, not
     a network block at all. A `127.0.0.1` bind only accepts connections from the same machine;
     `ss -tuln` will still show the app as "listening," but literally no one else, from anywhere,
     can reach it. The app is genuinely "listening to itself" only.

   The key distinction: one is the network actively refusing to deliver traffic that the app would
   otherwise accept; the other is the app itself only ever accepting traffic from itself, with
   nothing in the network blocking anything.

**How the actual quiz session went** (for context, not the answers themselves): Q1 needed a full
reset after initially conflating the two networks' host-bit counts, then recovered cleanly once
separated step by step; Q2 was correct on the mechanism immediately, with one nudge needed to name
the actual term "round-robin DNS"; Q3 passed cleanly, first try; Q4 named app-binding unprompted,
needed a nudge for the firewall cause, then correctly distinguished network-level vs. app-level
once both were named.

**Score: 74/100**
- **Quiz 28/40** — correct throughout, but 3 of 4 needed a follow-up nudge.
- **Hands-on 24/30** — real commands run and interpreted correctly, but intentionally
  lighter/faster-paced than prior topics.
- **Depth 22/30** — solid scenario reasoning, breadth traded for speed this pass.

### Revision pass — simplified recap + concept checks + real-world scenarios + hands-on

Requested directly after Attempt 1, since "the 1st time doesn't work that great" — full second
pass covering everything in sections 1-9 above, including the mail-analogy recap table, the
extended CIDR table (down to `/1`), the third "reserved address" category (`127.0.0.1`/`0.0.0.0`,
genuinely clarified only after back-and-forth), real-world scenarios (subnet sizing, DNS record
migration, single-IP tradeoff), and the live `curl` verification of refused/no-route/timeout.

### Retest — full fresh quiz, all-new questions — PASS, 82/100 (official score)

Question and full correct answer for each:

1. **`172.16.5.20/12` — is it private or public, and how many addresses does that `/12` cover?**
   Private/public check for `172.x.x.x`: it's private only when the second octet is between 16
   and 31 inclusive. `172.16.5.20`'s second octet is `16`, which falls in that range, so it's
   **private**. Address count: `/12` means 12 fixed network bits out of 32, leaving `32 − 12 = 20`
   host bits free → `2^20` = **1,048,576 addresses**.

2. **Is a single IP returned for an app (vs. multiple IPs in round-robin DNS) a problem?**
   Not inherently — it's proportional to scale, not a defect; a small app simply doesn't need
   multiple servers behind it. The real tradeoff is redundancy: with only one IP/server, there is
   **no built-in failover** — if that one server goes down, the whole app becomes unreachable. A
   multi-IP round-robin setup, by contrast, can route around a single failed server by having the
   client simply try the next IP in the list. So the difference isn't "wrong vs. right," it's
   "no failover vs. has failover."

3. **What do `0.0.0.0` and `127.0.0.1` mean when they show up in `ss -tuln` output?**
   Both are *bind* addresses — what a listening app has chosen to accept connections from — not
   "the app's IP address" or "the public IP." `127.0.0.1` is the reserved loopback address, meaning
   "this machine talking to itself"; an app bound to it accepts connections **only from the same
   machine**, not even from other machines on the same local network. `0.0.0.0` is a
   wildcard/unspecified address; as a bind address it means the app accepts connections on
   **every interface the machine has** — local network and internet too, if a public IP and open
   firewall exist. Practically, this matters because an app bound to `127.0.0.1` still shows as
   "listening" in `ss -tuln` — yet no one else, from anywhere, can ever reach it. This is a common
   real bug: a dev server works fine locally (`localhost` = `127.0.0.1`) then mysteriously "doesn't
   work" once deployed, purely because the bind address was never changed to `0.0.0.0`.

4. **Walk through the full diagnostic order for a service a teammate can't reach.**
   1. **`ping` the IP** — a basic reachability check, but success here does **not** prove the
      target port is reachable, since ICMP and TCP/UDP are controlled independently.
   2. **`ss -tuln` on the server itself** (not the teammate's machine) — confirms whether the app
      is actually listening on that port at all.
   3. **If listening but still unreachable, check two distinct causes**: a firewall/security group
      blocking the port at the **network level** (most common), or the app being bound to
      `127.0.0.1` instead of `0.0.0.0` (an **app-level** configuration choice, not a network block
      at all).

5. **What does a "Connection refused" result rule in, and what does it rule out?**
   It **rules in** that the target machine was reached and nothing is listening on that port — the
   OS itself actively responded with a TCP `RST`, which is why it comes back almost instantly (2 ms
   in the real `curl -v` test). It **rules out** a *silently-dropping* firewall specifically,
   because that kind of firewall drops the packet rather than sending an active refusal back; that
   case instead produces the "connection timed out" result — total silence, waiting the full
   timeout with nothing returned. (Caveat: a **REJECT**-configured firewall also sends an active
   refusal, indistinguishable from "nothing listening" — "refused" only rules out a silent DROP,
   not every firewall.) So "refused" is usually more informative than "timed out": it confirms the
   target is reachable and simply means no app is bound to that port, whereas "timed out" gives no
   information at all.

**How the actual quiz session went** (for context, not the answers themselves): Q1 passed cleanly,
first try, both parts correct in one answer; Q2 was correct on "not inherently a problem," needed
one nudge to name the redundancy/failover tradeoff explicitly; Q3's initial answer incorrectly
called both addresses "the public IP," corrected via the reserved-address-category explanation;
Q4 passed with hints needed for the last two steps (bind address, then firewall) after naming the
first two independently; Q5 ruled in correctly first try, needed one nudge to articulate why it
also rules out a firewall block specifically.

**Score: 82/100**
- **Quiz 30/40** — all 5 ultimately correct, 4 of 5 needed some help (a nudge, or in Q3's case a
  real correction).
- **Hands-on 26/30** — real `curl -v` tests run and correctly interpreted to verify the
  refused/no-route distinction live, stronger verification than Attempt 1.
- **Depth 26/30** — correctly reasoned through the reserved-address category, which went beyond
  what was explicitly taught, with guidance.

**Verdict**: **Topic 5 CLEARED, official score, 82/100.** The retest score supersedes Attempt 1's
74/100 as the logged record, reflecting the stronger, hands-on-verified understanding reached
after the revision pass.
