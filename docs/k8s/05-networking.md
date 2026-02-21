# 05 - Networking

> **27 playbooks** for Kubernetes networking issues.

## Overview

Kubernetes networking enables communication between:
- Pods within the cluster
- Pods and services
- External traffic to services (via Ingress)
- DNS resolution within the cluster

This category covers Services, Ingress, CoreDNS, NetworkPolicies, and kube-proxy.

## Playbooks

### Service Issues

| Playbook | Description |
|----------|-------------|
| [ServiceNotAccessible-service](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/ServiceNotAccessible-service.md) | Service not accessible |
| [ServiceNotForwardingTraffic-service](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/ServiceNotForwardingTraffic-service.md) | Service not forwarding traffic |
| [ServiceNodePortNotAccessible-service](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/ServiceNodePortNotAccessible-service.md) | NodePort service not accessible |
| [ServiceExternal-IPPending-service](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/ServiceExternal-IPPending-service.md) | Service external IP pending |
| [ServicesIntermittentlyUnreachable-service](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/ServicesIntermittentlyUnreachable-service.md) | Services intermittently unreachable |
| [ErrorConnectionRefusedWhenAccessingService-service](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/ErrorConnectionRefusedWhenAccessingService-service.md) | Connection refused to service |

### DNS Issues

| Playbook | Description |
|----------|-------------|
| [ServiceNotResolvingDNS-dns](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/ServiceNotResolvingDNS-dns.md) | Service DNS not resolving |
| [DNSResolutionIntermittent-dns](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/DNSResolutionIntermittent-dns.md) | DNS resolution intermittent |
| [CoreDNSPodsCrashLooping-dns](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/CoreDNSPodsCrashLooping-dns.md) | CoreDNS pods crashing |
| [CoreDNSDown-dns](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/CoreDNSDown-dns.md) | CoreDNS down |
| [CoreDNSLatencyHigh-dns](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/CoreDNSLatencyHigh-dns.md) | CoreDNS latency high |

### Ingress Issues

| Playbook | Description |
|----------|-------------|
| [IngressNotWorking-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/IngressNotWorking-ingress.md) | Ingress not routing traffic |
| [IngressReturning502BadGateway-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/IngressReturning502BadGateway-ingress.md) | Ingress returning 502 errors |
| [IngressShows404-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/IngressShows404-ingress.md) | Ingress showing 404 errors |
| [IngressRedirectLoop-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/IngressRedirectLoop-ingress.md) | Ingress causing redirect loops |
| [IngressControllerPodsCrashLooping-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/IngressControllerPodsCrashLooping-ingress.md) | Ingress controller crashing |
| [IngressSSLTLSConfigurationFails-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/IngressSSLTLSConfigurationFails-ingress.md) | Ingress SSL/TLS configuration failing |
| [IngressCertificateExpiring-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/IngressCertificateExpiring-ingress.md) | Ingress certificate expiring |

### NGINX Ingress Issues

| Playbook | Description |
|----------|-------------|
| [NginxIngressDown-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/NginxIngressDown-ingress.md) | NGINX Ingress down |
| [NginxIngress4xxErrorsHigh-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/NginxIngress4xxErrorsHigh-ingress.md) | NGINX Ingress 4xx errors high |
| [NginxIngress5xxErrorsHigh-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/NginxIngress5xxErrorsHigh-ingress.md) | NGINX Ingress 5xx errors high |
| [NginxIngressConfigReloadFailed-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/NginxIngressConfigReloadFailed-ingress.md) | NGINX Ingress config reload failed |
| [NginxIngressHighLatency-ingress](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/NginxIngressHighLatency-ingress.md) | NGINX Ingress high latency |

### Network/kube-proxy Issues

| Playbook | Description |
|----------|-------------|
| [NetworkPolicyBlockingTraffic-network](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/NetworkPolicyBlockingTraffic-network.md) | Network policy blocking traffic |
| [NodesUnreachable-network](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/NodesUnreachable-network.md) | Nodes unreachable |
| [KubeProxyDown-network](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/KubeProxyDown-network.md) | kube-proxy down |
| [Kube-proxyFailing-network](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/K8s%20Playbooks/05-Networking/Kube-proxyFailing-network.md) | kube-proxy failing |

## Quick Troubleshooting

### Service Not Accessible

<details>
<summary>CLI Commands</summary>

```bash
# Check service exists
kubectl get svc <service-name> -n <namespace>

# Check service has endpoints
kubectl get endpoints <service-name> -n <namespace>

# Check service details
kubectl describe svc <service-name> -n <namespace>

# Test from within cluster
kubectl run test --rm -it --image=busybox -- wget -qO- <service-name>.<namespace>:port
```

</details>

### DNS Not Resolving

<details>
<summary>CLI Commands</summary>

```bash
# Check CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Test DNS resolution
kubectl run test --rm -it --image=busybox -- nslookup <service>.<namespace>.svc.cluster.local
```

</details>

### Ingress Issues

<details>
<summary>CLI Commands</summary>

```bash
# Check ingress
kubectl get ingress -n <namespace>

# Describe ingress
kubectl describe ingress <ingress-name> -n <namespace>

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

</details>

---

[Back to Kubernetes Playbooks](/k8s/)
