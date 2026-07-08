"""CI/CD, Docker, Kubernetes, DevOps, Terraform, Monitoring questions with full answers."""

_ALL_ENG = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn","Stripe","Razorpay","PhonePe","Swiggy","Zomato","CRED","Dream11","Atlassian","Adobe","Netflix","Coinbase"]
_G3 = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn"]
_IND = ["Razorpay","PhonePe","Swiggy","Zomato","CRED","Dream11","Groww"]

def A(*sections):
    """Helper: build formatted answer HTML from (label, content) pairs."""
    parts = []
    for label, content in sections:
        parts.append(f'<span class="answer-label">{label}</span><br>{content}')
    return '<div class="answer-section">' + '</div><div class="answer-section" style="margin-top:10px">'.join(parts) + '</div>'

CICD_QUESTIONS = [
  ("cicd001",
   "Docker container vs Virtual Machine — key differences?",
   "cicd","docker","Easy",
   _ALL_ENG, 93, "docker,vm,container,isolation", "CI/CD Round",
   A(("Answer",
      "<b>Virtual Machine:</b> Full OS per VM, hardware emulation via hypervisor (Type-1: bare metal, Type-2: hosted). "
      "Heavy: ~GBs, slow boot (~minutes), strong isolation.<br>"
      "<b>Docker Container:</b> Shares host OS kernel, isolates via Linux namespaces (PID, NET, MNT, UTS, IPC) + cgroups for resource limits. "
      "Lightweight: ~MBs, starts in milliseconds, process-level isolation."),
     ("Key Differences",
      "<ul><li><b>Boot time:</b> VM ~1-2 min | Container ~100ms</li>"
      "<li><b>Size:</b> VM ~GBs | Container ~MBs (shared layers)</li>"
      "<li><b>Isolation:</b> VM = full kernel isolation | Container = namespace isolation (kernel shared)</li>"
      "<li><b>Use case:</b> VM for multi-OS, strong isolation | Container for microservices, CI/CD</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• What Linux namespaces does Docker use? (PID, NET, MNT, IPC, UTS, USER)<br>'
      '• How do cgroups limit CPU/memory in containers?<br>'
      '• What is a container runtime? (runc, containerd, CRI-O)</div>')
   )),

  ("cicd002",
   "How do Docker image layers work? (Union filesystem)",
   "cicd","docker","Medium",
   _ALL_ENG, 90, "docker,layers,overlay2,union-fs", "CI/CD Round",
   A(("Answer",
      "Docker images are built as <b>read-only layers</b> stacked using a Union Filesystem (OverlayFS/AUFS). "
      "Each <code>RUN</code>, <code>COPY</code>, <code>ADD</code> instruction in a Dockerfile creates a new layer.<br><br>"
      "When a container runs, Docker adds a thin <b>read-write layer</b> on top (Copy-on-Write). "
      "Writes go to the container layer; reads search layers bottom-up."),
     ("Dockerfile Layer Example",
      "<pre>FROM ubuntu:22.04          # Layer 1: base OS\n"
      "RUN apt-get install -y java # Layer 2: java install\n"
      "COPY app.jar /app/          # Layer 3: app binary\n"
      "CMD [\"java\", \"-jar\", \"/app/app.jar\"]  # metadata only</pre>"),
     ("Optimization Tips",
      "<ul><li>Order layers from least to most frequently changing</li>"
      "<li>Combine <code>RUN</code> commands to reduce layer count</li>"
      "<li>Use <code>.dockerignore</code> to exclude build artifacts</li>"
      "<li>Use multi-stage builds to discard build-time layers</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• What is <code>docker build --cache-from</code>?<br>'
      '• How does <code>docker squash</code> work?<br>'
      '• Difference between image and container filesystem?</div>')
   )),

  ("cicd003",
   "Explain multi-stage Docker builds and why they matter",
   "cicd","docker","Medium",
   _G3 + _IND, 87, "docker,multi-stage,build,optimization", "CI/CD Round",
   A(("Answer",
      "Multi-stage builds use multiple <code>FROM</code> statements in one Dockerfile. "
      "Build artifacts are copied from one stage to another, <b>discarding build-time dependencies</b> from the final image."),
     ("Example: Go Application",
      "<pre># Stage 1: Build\nFROM golang:1.22 AS builder\nWORKDIR /app\nCOPY . .\nRUN CGO_ENABLED=0 go build -o server .\n\n"
      "# Stage 2: Minimal runtime (5MB vs 800MB!)\nFROM scratch\nCOPY --from=builder /app/server /server\nCMD [\"/server\"]</pre>"),
     ("Benefits",
      "<ul><li>Final image contains <b>only runtime artifacts</b>, no compiler/SDK</li>"
      "<li>Security: smaller attack surface</li>"
      "<li>Faster pulls and deployments</li>"
      "<li>Build cache is still leveraged per stage</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• How do you pass build args between stages?<br>'
      '• What is <code>docker build --target builder</code> for?<br>'
      '• Distroless vs scratch images?</div>')
   )),

  ("cicd004",
   "Kubernetes architecture — explain all components",
   "cicd","kubernetes","Hard",
   _G3 + ["Stripe","Razorpay","PhonePe","CRED","Swiggy","Atlassian"], 92, "kubernetes,api-server,etcd,scheduler,kubelet", "CI/CD Round",
   A(("Control Plane",
      "<ul>"
      "<li><b>kube-apiserver:</b> REST API gateway; all kubectl commands go here. Validates, authenticates, stores to etcd.</li>"
      "<li><b>etcd:</b> Distributed KV store (Raft consensus). Single source of truth for all cluster state.</li>"
      "<li><b>kube-scheduler:</b> Watches unscheduled pods, assigns them to nodes based on resources, affinity, taints.</li>"
      "<li><b>kube-controller-manager:</b> Runs controllers (ReplicaSet, Node, Job, Endpoint) in reconciliation loops.</li>"
      "<li><b>cloud-controller-manager:</b> Integrates with cloud provider APIs (LB, volumes, routes).</li></ul>"),
     ("Worker Nodes",
      "<ul>"
      "<li><b>kubelet:</b> Agent on each node. Ensures containers in pods are running. Reports to API server.</li>"
      "<li><b>kube-proxy:</b> Manages iptables/IPVS rules for Service networking and load balancing.</li>"
      "<li><b>Container Runtime:</b> containerd or CRI-O. Pulls images, runs containers.</li></ul>"),
     ("Flow: kubectl apply",
      "<pre>kubectl apply → apiserver (auth+validate) → etcd (store)\n"
      "→ controller-manager (create pods) → scheduler (assign node)\n"
      "→ kubelet on node (pull image, start container)</pre>"),
     ("Follow-ups",
      '<div class="followup">• What happens when the API server goes down?<br>'
      '• How does etcd leader election work?<br>'
      '• Difference between kubelet and kube-proxy?</div>')
   )),

  ("cicd005",
   "Pod vs ReplicaSet vs Deployment vs StatefulSet",
   "cicd","kubernetes","Medium",
   _G3 + _IND + ["Atlassian","Stripe"], 90, "kubernetes,pod,deployment,statefulset", "CI/CD Round",
   A(("Pod",
      "Smallest deployable unit. 1+ containers sharing network namespace and volumes. <b>Ephemeral</b> — deleted pods don't restart."),
     ("ReplicaSet",
      "Ensures N pod replicas are always running. Uses label selectors. <b>Rarely used directly</b> — Deployments manage them."),
     ("Deployment",
      "Manages ReplicaSets for <b>stateless apps</b>. Provides: rolling updates, rollback, pause/resume. "
      "<code>kubectl rollout undo deployment/app</code> for rollback."),
     ("StatefulSet",
      "For <b>stateful apps</b> (databases, Kafka, ZooKeeper). Provides: stable pod names (<code>pod-0, pod-1</code>), "
      "stable DNS, ordered start/stop, per-pod PersistentVolumeClaims."),
     ("When to use what",
      "<ul><li>Stateless API service → <b>Deployment</b></li>"
      "<li>Database (MySQL, Redis) → <b>StatefulSet</b></li>"
      "<li>One pod per node → <b>DaemonSet</b></li>"
      "<li>One-off batch job → <b>Job/CronJob</b></li></ul>"),
     ("Follow-ups",
      '<div class="followup">• How does rolling update work in a Deployment?<br>'
      '• What is a headless Service and when is it used with StatefulSets?<br>'
      '• How do you do a canary deployment in K8s?</div>')
   )),

  ("cicd006",
   "Kubernetes Services — ClusterIP, NodePort, LoadBalancer, ExternalName",
   "cicd","kubernetes","Medium",
   _G3 + _IND, 88, "kubernetes,service,clusterip,loadbalancer", "CI/CD Round",
   A(("ClusterIP (default)",
      "Exposes service on a <b>cluster-internal IP</b>. Only reachable within the cluster. "
      "kube-proxy creates iptables rules to load-balance across matching pods. Used for inter-service communication."),
     ("NodePort",
      "Exposes service on each node's IP at a static port (30000-32767). "
      "<code>nodeIP:nodePort</code> routes to ClusterIP then to pods. OK for dev/testing, not production."),
     ("LoadBalancer",
      "Provisions a <b>cloud load balancer</b> (AWS ALB/NLB, GCP LB) and assigns an external IP. "
      "Each service gets its own LB — expensive. Use Ingress for shared LB."),
     ("Ingress",
      "Not a Service type but routes external HTTP(S) to ClusterIP services. "
      "L7 routing by host/path. One LB for many services. Needs an Ingress Controller (nginx, traefik, AWS ALB)."),
     ("Follow-ups",
      '<div class="followup">• What is a headless Service (<code>clusterIP: None</code>)?<br>'
      '• How does kube-proxy implement service routing (iptables vs IPVS)?<br>'
      '• What is EndpointSlice?</div>')
   )),

  ("cicd007",
   "Kubernetes HPA — Horizontal Pod Autoscaler, how does it work?",
   "cicd","kubernetes","Medium",
   _G3 + ["Stripe","Razorpay","Swiggy","CRED"], 85, "kubernetes,hpa,autoscaling,metrics-server", "CI/CD Round",
   A(("How HPA works",
      "HPA watches metrics (CPU, memory, custom) via the <b>Metrics API</b> and adjusts pod replica count.<br><br>"
      "<b>Control loop (every 15s):</b><br>"
      "<pre>desiredReplicas = ceil(currentReplicas × currentMetric / targetMetric)</pre>"
      "e.g., 3 pods at 90% CPU, target 50% → ceil(3 × 90/50) = 6 pods"),
     ("Setup",
      "<pre>kubectl autoscale deployment app \\\n"
      "  --cpu-percent=50 --min=2 --max=20\n\n"
      "# Or declarative:\napiVersion: autoscaling/v2\nkind: HorizontalPodAutoscaler\nspec:\n"
      "  scaleTargetRef:\n    kind: Deployment\n    name: app\n  minReplicas: 2\n  maxReplicas: 20\n"
      "  metrics:\n  - type: Resource\n    resource:\n      name: cpu\n      target:\n        type: Utilization\n        averageUtilization: 50</pre>"),
     ("VPA vs HPA vs KEDA",
      "<ul><li><b>HPA:</b> scales pod count (horizontal)</li>"
      "<li><b>VPA:</b> adjusts CPU/memory requests per pod (vertical) — requires restart</li>"
      "<li><b>KEDA:</b> event-driven scaling (queue depth, Kafka lag, cron)</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• What happens when HPA and VPA conflict?<br>'
      '• How do you scale on custom metrics (e.g., requests/sec)?<br>'
      '• What is scale-down stabilization window?</div>')
   )),

  ("cicd008",
   "ConfigMaps vs Secrets in Kubernetes",
   "cicd","kubernetes","Easy",
   _ALL_ENG, 88, "kubernetes,configmap,secrets,env", "CI/CD Round",
   A(("ConfigMap",
      "Stores <b>non-sensitive</b> configuration as key-value pairs. "
      "Mounted as environment variables or volume files. Plain text in etcd."),
     ("Secret",
      "Stores <b>sensitive data</b> (passwords, tokens, TLS certs). Base64-encoded in etcd (NOT encrypted by default). "
      "Enable encryption at rest with <code>EncryptionConfiguration</code>. "
      "Types: Opaque, kubernetes.io/tls, kubernetes.io/dockerconfigjson, etc."),
     ("Usage",
      "<pre># Mount as env\nenv:\n- name: DB_PASSWORD\n  valueFrom:\n    secretKeyRef:\n      name: db-secret\n      key: password\n\n"
      "# Mount as volume\nvolumeMounts:\n- name: config\n  mountPath: /etc/config\nvolumes:\n- name: config\n  configMap:\n    name: app-config</pre>"),
     ("Best Practices",
      "<ul><li>Use <b>external secret managers</b>: HashiCorp Vault, AWS Secrets Manager with External Secrets Operator</li>"
      "<li>Never bake secrets into Docker images</li>"
      "<li>RBAC: restrict Secret read access to specific ServiceAccounts</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• How does Vault Agent injector work?<br>'
      '• What is Sealed Secrets (Bitnami)?<br>'
      '• How do you rotate secrets without pod restart?</div>')
   )),

  ("cicd009",
   "Explain Kubernetes resource requests and limits — QoS classes",
   "cicd","kubernetes","Medium",
   _G3 + ["Stripe","Razorpay","Swiggy"], 84, "kubernetes,resources,qos,oom", "CI/CD Round",
   A(("Requests vs Limits",
      "<b>Requests:</b> Minimum guaranteed resources. Used by scheduler to find a node with enough capacity.<br>"
      "<b>Limits:</b> Maximum allowed. CPU is throttled if exceeded. Memory: container is OOMKilled if exceeded."),
     ("QoS Classes",
      "<ul><li><b>Guaranteed:</b> requests == limits for all containers. Highest priority, last to be evicted.</li>"
      "<li><b>Burstable:</b> requests < limits. Medium priority.</li>"
      "<li><b>BestEffort:</b> No requests or limits set. First to be evicted under pressure.</li></ul>"),
     ("Example",
      "<pre>resources:\n  requests:\n    cpu: \"250m\"     # 0.25 CPU core\n    memory: \"256Mi\"\n"
      "  limits:\n    cpu: \"1000m\"    # 1 CPU core\n    memory: \"512Mi\"</pre>"),
     ("Follow-ups",
      '<div class="followup">• What is a LimitRange resource?<br>'
      '• What is ResourceQuota and how does it work per namespace?<br>'
      '• What happens when a node runs out of memory?</div>')
   )),

  ("cicd010",
   "What is Helm and what problem does it solve?",
   "cicd","helm","Medium",
   _G3 + _IND + ["Atlassian","Stripe"], 86, "helm,chart,release,values", "CI/CD Round",
   A(("What is Helm",
      "Helm is the <b>package manager for Kubernetes</b>. It bundles K8s manifests into a <b>Chart</b> "
      "(a directory of YAML templates + <code>values.yaml</code>). "
      "Manages versioned releases, upgrades, and rollbacks."),
     ("Key Concepts",
      "<ul><li><b>Chart:</b> Package of K8s manifests (Deployment, Service, Ingress, etc.)</li>"
      "<li><b>Release:</b> A running instance of a chart in a cluster</li>"
      "<li><b>Values:</b> Configuration injected into templates at render time</li>"
      "<li><b>Repository:</b> Collection of charts (like npm/pip registry)</li></ul>"),
     ("Common Commands",
      "<pre>helm install myapp ./chart -f values.prod.yaml\n"
      "helm upgrade myapp ./chart --set image.tag=v2.0\n"
      "helm rollback myapp 1\n"
      "helm template ./chart  # render YAML without installing</pre>"),
     ("Helm vs Kustomize",
      "<ul><li><b>Helm:</b> Templating + packaging + release management. Better for distributing software.</li>"
      "<li><b>Kustomize:</b> Overlay-based patching, no templating. Better for environment-specific customization.</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• What is a Helm hook?<br>'
      '• How do you test a Helm chart?<br>'
      '• What are Helm library charts?</div>')
   )),

  ("cicd011",
   "What is GitOps? How does Argo CD work?",
   "cicd","gitops","Medium",
   _G3 + ["Stripe","Razorpay","Atlassian","CRED"], 82, "gitops,argocd,flux,declarative", "CI/CD Round",
   A(("GitOps Principles",
      "<b>GitOps:</b> Git is the single source of truth for infrastructure and application state. "
      "All changes happen via PRs. An operator continuously reconciles cluster state with Git state."),
     ("Argo CD Architecture",
      "<ul><li><b>API Server:</b> gRPC/REST API, RBAC, webhook receiver</li>"
      "<li><b>Repository Server:</b> Clones Git repos, renders manifests (Helm/Kustomize/plain YAML)</li>"
      "<li><b>Application Controller:</b> Watches K8s cluster, compares with desired state, syncs</li></ul>"),
     ("Sync Flow",
      "<pre>Git commit → Argo detects drift (polls or webhook)\n"
      "→ Renders manifests → Diffs vs cluster state\n"
      "→ Applies changes (kubectl apply) → Marks app Synced</pre>"),
     ("Argo CD vs Flux",
      "<ul><li><b>Argo CD:</b> UI, multi-cluster, App of Apps, RBAC. Better UX.</li>"
      "<li><b>Flux:</b> Lighter, CNCF graduated, Helm controller, image automation.</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• What is App of Apps pattern in Argo CD?<br>'
      '• How do you handle secrets in GitOps? (Sealed Secrets, Vault, SOPS)<br>'
      '• What is progressive delivery? (Argo Rollouts, Flagger)</div>')
   )),

  ("cicd012",
   "CI/CD pipeline stages — what should a production pipeline include?",
   "cicd","pipeline","Medium",
   _ALL_ENG, 90, "ci-cd,pipeline,stages,testing", "CI/CD Round",
   A(("Typical Pipeline",
      "<pre>1. Source  →  git push/PR triggers pipeline\n"
      "2. Build   →  compile, docker build\n"
      "3. Test    →  unit → integration → contract tests\n"
      "4. SAST    →  static analysis (SonarQube, Semgrep)\n"
      "5. Scan    →  container vulnerability scan (Trivy, Snyk)\n"
      "6. Publish →  push image to registry (ECR/GCR/DockerHub)\n"
      "7. Deploy  →  to staging (auto) → prod (gated/manual or canary)\n"
      "8. Smoke   →  health check post-deploy\n"
      "9. Notify  →  Slack/PagerDuty on failure</pre>"),
     ("GitHub Actions Example (simplified)",
      "<pre>on: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n"
      "    - uses: actions/checkout@v4\n    - run: docker build -t app:${{ github.sha }} .\n"
      "    - run: docker push $ECR_REPO:${{ github.sha }}</pre>"),
     ("Key Metrics",
      "<ul><li><b>DORA:</b> Deployment Frequency, Lead Time for Changes, MTTR, Change Failure Rate</li>"
      "<li>Aim: deploy multiple times/day, MTTR < 1hr</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• How do you implement trunk-based development vs GitFlow?<br>'
      '• How do you handle database migrations in CI/CD?<br>'
      '• What is shift-left testing?</div>')
   )),

  ("cicd013",
   "How does Terraform manage infrastructure state?",
   "cicd","terraform","Medium",
   _G3 + ["Stripe","Razorpay","Atlassian","Dream11"], 80, "terraform,state,remote-backend,plan-apply", "CI/CD Round",
   A(("State File",
      "Terraform tracks real-world resources in a <b>state file</b> (<code>terraform.tfstate</code>). "
      "It maps config to actual cloud resources. Without state, Terraform can't know what already exists."),
     ("Remote State (production must-have)",
      "<pre># backend.tf\nterraform {\n  backend \"s3\" {\n    bucket         = \"my-tf-state\"\n    key            = \"prod/terraform.tfstate\"\n    region         = \"us-east-1\"\n    encrypt        = true\n    dynamodb_table = \"tf-lock\"  # distributed locking\n  }\n}</pre>"),
     ("Core Commands",
      "<pre>terraform init    # download providers, init backend\n"
      "terraform plan    # show what will change (diff)\n"
      "terraform apply   # apply changes\n"
      "terraform destroy # tear down resources\n"
      "terraform import  # import existing resource into state</pre>"),
     ("State Locking",
      "DynamoDB table prevents concurrent state modifications. "
      "Always use remote backend with locking in teams."),
     ("Follow-ups",
      '<div class="followup">• What is a Terraform workspace?<br>'
      '• How do you refactor state (<code>terraform state mv</code>)?<br>'
      '• Terraform vs Pulumi vs CDK?</div>')
   )),

  ("cicd014",
   "Docker networking modes explained",
   "cicd","docker","Medium",
   _G3 + _IND, 82, "docker,networking,bridge,host,overlay", "CI/CD Round",
   A(("Bridge (default)",
      "Docker creates a virtual <code>docker0</code> bridge. Containers get their own IP on <code>172.17.0.0/16</code>. "
      "Containers communicate by container name (with <code>--network</code>). NAT for outbound traffic."),
     ("Host",
      "Container shares the host's network namespace. No isolation, best performance. "
      "<code>docker run --network=host nginx</code> — port 80 on container is port 80 on host."),
     ("Overlay",
      "Multi-host networking (Docker Swarm / Kubernetes). VXLAN encapsulation for container-to-container traffic across nodes."),
     ("None",
      "No network interface. Maximum isolation. Used for batch processing with no network needs."),
     ("Kubernetes CNI",
      "K8s uses CNI plugins (Calico, Flannel, Cilium) to implement pod networking. "
      "Cilium uses eBPF for high-performance, policy-aware networking."),
     ("Follow-ups",
      '<div class="followup">• How do you expose a container port? (<code>-p host:container</code>)<br>'
      '• What is CNI (Container Network Interface)?<br>'
      '• How does Kubernetes pod-to-pod networking work?</div>')
   )),

  ("cicd015",
   "Prometheus + Grafana monitoring stack — how does it work?",
   "cicd","monitoring","Medium",
   _G3 + ["Stripe","Razorpay","Swiggy","CRED","Atlassian","Dream11"], 86, "prometheus,grafana,metrics,alertmanager", "CI/CD Round",
   A(("Prometheus",
      "<b>Pull-based</b> metrics collection. Scrapes HTTP <code>/metrics</code> endpoints (Prometheus exposition format) "
      "at configurable intervals. Stores as time-series (metric + labels + timestamp + value).<br><br>"
      "<b>Key components:</b> scrape engine, TSDB (local), PromQL query language, Alertmanager integration."),
     ("PromQL Examples",
      "<pre># Request rate per second\nrate(http_requests_total[5m])\n\n"
      "# 99th percentile latency\nhistogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))\n\n"
      "# CPU usage\n100 - (avg by(instance)(rate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)</pre>"),
     ("Grafana",
      "Visualization layer. Connects to Prometheus as a data source. Dashboards with panels (graphs, gauges, heatmaps). "
      "Alerting, annotations, templating for dynamic dashboards."),
     ("Full Stack: LGTM",
      "<ul><li><b>Loki:</b> Log aggregation (like Prometheus but for logs)</li>"
      "<li><b>Grafana:</b> Visualization</li>"
      "<li><b>Tempo:</b> Distributed tracing</li>"
      "<li><b>Mimir/Prometheus:</b> Metrics</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• What is a Prometheus exporter? (node_exporter, blackbox_exporter)<br>'
      '• How does Alertmanager route and deduplicate alerts?<br>'
      '• What is OpenTelemetry and how does it relate to Prometheus?</div>')
   )),

  ("cicd016",
   "How does distributed tracing work? (OpenTelemetry, Jaeger)",
   "cicd","monitoring","Medium",
   _G3 + ["Stripe","Uber","Razorpay","CRED"], 80, "distributed-tracing,opentelemetry,jaeger,spans", "CI/CD Round",
   A(("Core Concepts",
      "<ul><li><b>Trace:</b> End-to-end journey of a request across services</li>"
      "<li><b>Span:</b> Single operation within a trace (has: traceID, spanID, parentSpanID, start/end time, attributes)</li>"
      "<li><b>Context propagation:</b> TraceID passed via HTTP headers (<code>traceparent</code> W3C standard, or <code>X-B3-TraceId</code> Zipkin)</li></ul>"),
     ("OpenTelemetry",
      "Vendor-neutral CNCF standard for instrumentation. SDK instruments code → exports to backend (Jaeger/Zipkin/Tempo/Datadog).<br>"
      "<pre>// Go example\nctx, span := tracer.Start(ctx, \"ProcessOrder\")\ndefer span.End()\nspan.SetAttributes(attribute.String(\"order.id\", orderID))</pre>"),
     ("Jaeger Architecture",
      "<pre>App (OTel SDK) → Jaeger Agent → Jaeger Collector → Cassandra/ES\n"
      "                                          ↓\n"
      "                                  Jaeger Query UI</pre>"),
     ("Follow-ups",
      '<div class="followup">• What is sampling in tracing? (head-based vs tail-based)<br>'
      '• How does trace correlation with logs work?<br>'
      '• What is the difference between metrics, logs, and traces (the 3 pillars)?</div>')
   )),

  ("cicd017",
   "Git internals — rebase vs merge, when to use each",
   "cicd","git","Medium",
   _ALL_ENG, 88, "git,rebase,merge,history", "CI/CD Round",
   A(("Merge",
      "Creates a <b>merge commit</b> that ties two branches together. Preserves full history including branch structure. "
      "Safe for shared branches — never rewrites history.<br>"
      "<pre>git checkout main\ngit merge feature/login\n# Creates commit: Merge branch 'feature/login'</pre>"),
     ("Rebase",
      "<b>Replays</b> commits from one branch onto another. Creates <b>linear history</b>. "
      "Rewrites commit SHAs — <b>never rebase shared/public branches</b>.<br>"
      "<pre>git checkout feature/login\ngit rebase main\n# Moves feature commits on top of latest main</pre>"),
     ("When to use",
      "<ul><li><b>Merge:</b> Merging feature into main (preserves context). Shared branches.</li>"
      "<li><b>Rebase:</b> Keeping feature branch up-to-date with main. Clean PR history. <code>git pull --rebase</code>.</li>"
      "<li><b>Squash merge:</b> Combine all feature commits into 1 clean commit on main.</li></ul>"),
     ("Interactive Rebase",
      "<pre>git rebase -i HEAD~3\n# Options: pick, squash, fixup, reword, drop</pre>"),
     ("Follow-ups",
      '<div class="followup">• What is <code>git cherry-pick</code>?<br>'
      '• How do you recover from a bad rebase? (<code>git reflog</code>)<br>'
      '• What is the difference between <code>git reset</code> and <code>git revert</code>?</div>')
   )),

  ("cicd018",
   "Container security best practices",
   "cicd","security","Medium",
   _G3 + ["Stripe","Razorpay","Atlassian"], 78, "docker,security,non-root,readonly,sca", "CI/CD Round",
   A(("Dockerfile Hardening",
      "<ul><li>Run as <b>non-root user</b>: <code>USER 1000:1000</code></li>"
      "<li>Use <b>minimal base images</b>: scratch, distroless, alpine</li>"
      "<li>Multi-stage build to remove build tools</li>"
      "<li>Pin image versions: <code>FROM golang:1.22.3</code> not <code>:latest</code></li>"
      "<li><code>COPY</code> only needed files; use <code>.dockerignore</code></li></ul>"),
     ("Kubernetes Security Context",
      "<pre>securityContext:\n  runAsNonRoot: true\n  runAsUser: 1000\n  readOnlyRootFilesystem: true\n"
      "  allowPrivilegeEscalation: false\n  capabilities:\n    drop: [ALL]</pre>"),
     ("Supply Chain Security",
      "<ul><li>Scan images with <b>Trivy</b> or <b>Snyk</b> in CI pipeline</li>"
      "<li>Sign images with <b>Cosign</b> (Sigstore)</li>"
      "<li>Use <b>OPA/Gatekeeper</b> or <b>Kyverno</b> for admission control</li>"
      "<li>SBOM (Software Bill of Materials) generation</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• What is a Pod Security Standard (baseline/restricted)?<br>'
      '• How does AppArmor/seccomp apply to containers?<br>'
      '• What is network policy in Kubernetes?</div>')
   )),

  ("cicd019",
   "ELK / EFK stack — log aggregation pipeline",
   "cicd","monitoring","Medium",
   _G3 + _IND + ["Atlassian"], 80, "elasticsearch,kibana,fluentd,logstash,logs", "CI/CD Round",
   A(("ELK Stack",
      "<ul><li><b>Elasticsearch:</b> Distributed search + analytics engine. Stores logs as JSON documents.</li>"
      "<li><b>Logstash:</b> Log ingestion pipeline: collect → filter (parse/transform) → output to ES</li>"
      "<li><b>Kibana:</b> Visualization: dashboards, Discover (search), Lens, Alerting</li></ul>"),
     ("EFK (Kubernetes preferred)",
      "<ul><li><b>Fluentd / Fluent Bit:</b> Lightweight log forwarder. DaemonSet on each node collects container logs from <code>/var/log/containers/</code> → Elasticsearch</li></ul>"
      "<pre>Container stdout → /var/log/containers/*.log\n"
      "→ Fluent Bit (parse JSON) → Elasticsearch → Kibana</pre>"),
     ("Structured Logging",
      "Always log in <b>JSON format</b>: <code>{\"level\":\"error\",\"traceId\":\"abc\",\"msg\":\"DB timeout\",\"ts\":\"...\"}</code><br>"
      "Correlate with traceID from distributed tracing."),
     ("Follow-ups",
      '<div class="followup">• What is Loki (Grafana) vs Elasticsearch?<br>'
      '• How do you handle log sampling at high throughput?<br>'
      '• What is Vector (log aggregator)?</div>')
   )),

  ("cicd020",
   "GitHub Actions vs Jenkins vs GitLab CI — comparison",
   "cicd","pipeline","Medium",
   _ALL_ENG, 82, "github-actions,jenkins,gitlab-ci,ci-tools", "CI/CD Round",
   A(("GitHub Actions",
      "<ul><li>YAML workflows in <code>.github/workflows/</code></li>"
      "<li>Hosted runners (GitHub-managed) or self-hosted</li>"
      "<li>Marketplace: 15,000+ pre-built actions</li>"
      "<li>Deep GitHub integration (PRs, issues, releases)</li>"
      "<li>Pricing: free for public repos, limited minutes for private</li></ul>"),
     ("Jenkins",
      "<ul><li>Self-hosted, open-source. Most flexible.</li>"
      "<li>Pipeline as code: <code>Jenkinsfile</code> (declarative or scripted Groovy)</li>"
      "<li>Huge plugin ecosystem (1,800+ plugins)</li>"
      "<li>Cons: maintenance overhead, not cloud-native</li></ul>"),
     ("GitLab CI",
      "<ul><li><code>.gitlab-ci.yml</code> in repo root</li>"
      "<li>Built-in: Docker registry, Kubernetes integration, security scanning</li>"
      "<li>Runners: shared or self-hosted</li>"
      "<li>Best for teams already on GitLab</li></ul>"),
     ("When to choose",
      "<ul><li><b>GitHub Actions:</b> GitHub-hosted projects, modern cloud-native teams</li>"
      "<li><b>Jenkins:</b> Legacy enterprise, complex custom pipelines</li>"
      "<li><b>GitLab CI:</b> GitLab monorepo, all-in-one DevSecOps</li></ul>"),
     ("Follow-ups",
      '<div class="followup">• How do you cache dependencies in GitHub Actions?<br>'
      '• What is a self-hosted runner and when to use it?<br>'
      '• How does matrix strategy work for parallel jobs?</div>')
   )),
]

def _to_dict(q):
    return {
        "id": q[0], "text": q[1], "category": q[2], "subcategory": q[3],
        "difficulty": q[4], "companies": q[5], "frequency": q[6],
        "tags": q[7].split(","), "round_type": q[8], "answer_hint": q[9]
    }

QUESTIONS = [_to_dict(q) for q in CICD_QUESTIONS]
