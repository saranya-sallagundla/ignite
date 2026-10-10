# Topic 12 — Kubernetes — Architecture & Core Concepts

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (the session log).
> Two-day topic per the roadmap — covered across two sessions, ending in the quiz. This session

---

## Day 1 — 2026-10-05 (what Kubernetes is, control-plane/worker architecture, the Pod, a real local cluster)

### Today's agenda
1. What Kubernetes is, why it matters to DevOps, how it fixes real problems, and the alternatives.
2. Core architecture: control plane vs. worker nodes, and every piece inside them.
3. The Pod — Kubernetes' actual deployable unit, distinct from a container.
4. Hands-on: install `kind`, create a real two-node local cluster, verify it.

### 1. What Kubernetes actually is

**Kubernetes** (shortened to **K8s** — "8" for the eight letters between the K and the s) is a
system that automatically manages many containers running across many machines: starting them,
restarting them if they crash, spreading them out sensibly, scaling their count up or down, and
routing traffic only to healthy copies. Built originally inside Google (based on an internal
system called Borg), open-sourced in 2014, now maintained by a neutral foundation (the CNCF)
rather than any single company.

**Why it matters to DevOps**: a containerized app on one single machine (Topics 9-11) has real
limits — if that machine dies, everything on it goes down; if the container crashes, nothing
restarts it automatically; if traffic spikes, there's no automatic way to add capacity. Docker
Compose solved this only for one machine. Kubernetes solves it across *many* machines, which is
the real production question almost every DevOps/SRE role runs into.

**How it fixes things**: you declare the desired state — "3 healthy copies of my app, reachable
through one address" — and Kubernetes continuously works to keep that true: restarting a crashed
copy, rescheduling work off a dead machine, adding capacity when the desired count goes up.

**Alternatives**: Docker Swarm (simpler, lost the orchestration race years ago), Nomad
(lighter-weight, HashiCorp-ecosystem), AWS ECS/Fargate or Google Cloud Run (fully-managed, hides
orchestration, less portable), and managed Kubernetes itself (EKS/GKE/AKS — not an alternative to
K8s, just someone else running the harder parts). Kubernetes won out mainly on being
vendor-neutral (the same config runs identically on any cloud or a laptop) and having by far the
largest ecosystem.

### 2. Architecture — the two-part split

Every cluster splits into two fundamentally different kinds of machines.

**Control plane**: the "brain." Doesn't run your application — makes all the decisions (what
should be running, where, whether reality matches the desired state) and keeps a record of
everything.

**Worker nodes**: the machines that actually run your containers. Plain and replaceable — one
dying isn't a crisis, the control plane just reschedules its work elsewhere.

**Analogy used**: an airport control tower (control plane) and the runways/planes (worker nodes).
The tower doesn't fly anyone anywhere — it decides which runway each plane uses and tracks
everything. If one runway closes, the tower reroutes traffic; it doesn't shut down the airport.

Inside the **control plane**, four pieces, each with one job:
- **API server** — the single front door of the entire cluster. Every request — a `kubectl`
  command, or one internal component talking to another — goes *through* here; nothing talks
  directly to the database or to a node. (Analogy: a hotel front desk — you don't walk into the
  back office yourself.) Needed a second, plainer re-explanation mid-session before it fully
  landed — worth remembering this term needs to be concrete, not just defined once in passing.
- **etcd** — the cluster's actual database. Stores the entire current state. Lose it, the cluster
  loses its memory of itself.
- **Scheduler** — decides *which* worker node a new container should run on, based on available
  resources.
- **Controller manager** — continuously compares actual state to desired state (both fetched via
  the API server) and corrects any drift — this is the "crashed copy gets restarted" mechanism.

On each **worker node**: the **kubelet** — an agent that talks to the API server and actually
starts/stops/monitors the containers assigned to that node. Kubelet doesn't run containers
itself, though — it hands that off to a **container runtime** (containerd or CRI-O) through a
standard interface called **CRI**. This is the exact same *pattern* as **WSGI** from Topic 11 (a
server handing requests to a framework through a standard contract, without needing to know its
internals) — just one layer up, and it's precisely why Kubernetes could drop direct Docker support
in 2022 without breaking anything: it was never talking to Docker's specific internals, only to
whatever implements the standard interface.

One more pair of terms: a **node** is one machine (control plane or worker); a **cluster** is the
whole set of nodes working together as one system.

### 3. The Pod

A **Pod** is the smallest thing actually deployed in Kubernetes — but it is *not* the same thing
as a container. A Pod is a wrapper around one or more containers meant to always run together:
same node, same network address, same storage.

Most of the time a Pod holds exactly **one** container. The "one or more" exists for a specific
pattern: a small helper container (shipping logs, handling TLS) that needs to run tightly coupled
to the main container, sharing its network/storage directly. For Orbit, it'll just be one Pod,
one container.

**Analogy used**: a Pod is a single hotel room. The room (Pod) has one address. Multiple people
(containers) *can* share that room if they truly need to be together, but usually it's just one
occupant.

**Why the extra wrapper exists at all**: the network/storage identity needs to belong to
*something stable* — and the Pod, not the container itself, is the stable unit Kubernetes
schedules, restarts, and tracks. A container can be swapped for a new one; the Pod concept is
what stays consistent underneath.

### 4. Hands-on — a real local cluster

**Tooling check**, from `C:\CloudOps\ignite`:
```
kind version
# kind: command not found
kubectl version --client
# Client Version: v1.34.1
```
`kubectl` was already present (bundled with Docker Desktop). `kind` needed installing.

**Verified the actual current release first**, rather than assuming a remembered version number:
```
gh api repos/kubernetes-sigs/kind/releases/latest --jq .tag_name
# v0.33.0
```

**Installed via `winget`** (Windows' built-in package manager, handles picking the current version
automatically):
```powershell
winget install -e --id Kubernetes.kind
```
Confirmed: `kind version` → `kind v0.33.0 go1.26.7 windows/amd64` — matching the release just
verified above.

**Alternative — direct binary download**, worth knowing even though `winget` is what was actually
used here: download the exact release binary and place it on PATH yourself:
```powershell
curl.exe -Lo kind.exe https://kind.sigs.k8s.io/dl/v0.33.0/kind-windows-amd64.exe
```
Useful when `winget`/Chocolatey aren't available, or when a specific pinned version is needed
rather than whatever the package manager currently offers.

**Syntax** — a `kind` cluster config:
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
```
Note the naming collision worth flagging: the `kind:` field inside this file is an unrelated,
standard Kubernetes-style config concept ("what type of object is this"), not the `kind` tool
naming itself twice — just a coincidence.

**Written to** `orbit/k8s/kind-config.yaml` — a two-node cluster (one control-plane, one worker),
named `orbit` to match everything else in the project rather than `kind`'s own default name:

```
kind create cluster --config kind-config.yaml --name orbit
```
```
Creating cluster "orbit" ...
 ✓ Ensuring node image (kindest/node:v1.37.0) 🖼️
 ✓ Preparing nodes 📦 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
 ✓ Joining worker nodes 🚜
Set kubectl context to "kind-orbit"
```
**New term — context**: `kubectl` can be configured to talk to multiple clusters; a "context" is
which cluster (plus which user/namespace) it's currently pointed at. `kind` set this
automatically, so `kubectl` now defaults to the new cluster with no extra configuration needed.
**CNI** (cluster networking) and **StorageClass** (storage) were installed automatically as part
of bringing the cluster up — covered properly in Topics 13-14.

**Verified the architecture live**, not just conceptually:
```
kubectl cluster-info --context kind-orbit
```
```
Kubernetes control plane is running at https://127.0.0.1:54792
CoreDNS is running at https://127.0.0.1:54792/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```
**New term — CoreDNS**: Kubernetes' own internal DNS server, running inside the cluster
(`kube-system` namespace) — the direct Kubernetes-level equivalent of the automatic name-based
service discovery Docker Compose gave in Topic 10 (`project_default` network, containers finding
each other by name), same underlying idea, one layer up.

```
kubectl get nodes
```
```
NAME                  STATUS   ROLES           AGE    VERSION
orbit-control-plane   Ready    control-plane   2m4s   v1.37.0
orbit-worker          Ready    <none>          97s    v1.37.0
```
Proof of the exact architecture just taught: `orbit-control-plane` correctly labeled
`control-plane`; `orbit-worker` shows `<none>` in the ROLES column — which is normal, not
missing. Kubernetes doesn't auto-assign a "worker" label the way it does for control-plane; a
node with no special role listed *is* a worker node by default.

No quiz today — Day 1 of a 2-day topic, per the roadmap's multi-day rule. Day 2 goes deeper
(Pods/Deployments/Services build on this) before the quiz.
