# Networking Playbooks

This folder contains **19 playbooks** for troubleshooting Kubernetes networking issues.

## What is Kubernetes Networking?

Kubernetes networking enables communication between:
- Pods within the cluster
- Pods and services
- External traffic to services (via Ingress)
- DNS resolution within the cluster

Key components include Services, Ingress, CoreDNS, and kube-proxy.

## Common Issues Covered

- Service connectivity problems
- Ingress configuration issues
- DNS resolution failures
- Network policy blocking traffic
- kube-proxy failures
- External service access problems
- Service IP issues

## Playbooks in This Folder

1. `CoreDNSPodsCrashLooping-dns.md` - CoreDNS pods crashing
2. `DNSResolutionIntermittent-dns.md` - DNS resolution intermittent
3. `ErrorConnectionRefusedWhenAccessingService-service.md` - Connection refused to service
4. `IngressControllerPodsCrashLooping-ingress.md` - Ingress controller crashing
5. `IngressNotWorking-ingress.md` - Ingress not routing traffic
6. `IngressRedirectLoop-ingress.md` - Ingress causing redirect loops
7. `IngressReturning502BadGateway-ingress.md` - Ingress returning 502 errors
8. `IngressShows404-ingress.md` - Ingress showing 404 errors
9. `IngressSSLTLSConfigurationFails-ingress.md` - Ingress SSL/TLS configuration failing
10. `KubeProxyDown-network.md` - kube-proxy down
11. `Kube-proxyFailing-network.md` - kube-proxy failing
12. `NetworkPolicyBlockingTraffic-network.md` - Network policy blocking traffic
13. `NodesUnreachable-network.md` - Nodes unreachable
14. `ServiceExternal-IPPending-service.md` - Service external IP pending
15. `ServiceNodePortNotAccessible-service.md` - NodePort service not accessible
16. `ServiceNotAccessible-service.md` - Service not accessible
17. `ServiceNotForwardingTraffic-service.md` - Service not forwarding traffic
18. `ServiceNotResolvingDNS-dns.md` - Service DNS not resolving
19. `ServicesIntermittentlyUnreachable-service.md` - Services intermittently unreachable

## Quick Start

If you're experiencing networking issues:

1. **Service Not Working**: Start with `ServiceNotAccessible-service.md` or `ServiceNotResolvingDNS-dns.md`
2. **Ingress Problems**: See `IngressNotWorking-ingress.md` or `IngressReturning502BadGateway-ingress.md`
3. **DNS Issues**: Check `ServiceNotResolvingDNS-dns.md` or `CoreDNSPodsCrashLooping-dns.md`
4. **Network Policies**: See `NetworkPolicyBlockingTraffic-network.md`
5. **kube-proxy**: Check `KubeProxyDown-network.md`

## Related Categories

- **03-Pods/**: Pod networking issues
- **01-Control-Plane/**: Control plane issues affecting networking
- **02-Nodes/**: Node networking problems

## Useful Commands

### Services
```bash
# Check services
kubectl get services -n <namespace>
kubectl get svc -A  # All namespaces

# Describe service
kubectl describe service <service-name> -n <namespace>

# Check service endpoints
kubectl get endpoints <service-name> -n <namespace>

# Check service selector matches
kubectl get pods -l <selector> -n <namespace>

# Test service connectivity
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- <service-name>.<namespace>.svc.cluster.local
```

### Ingress
```bash
# Check ingress
kubectl get ingress -n <namespace>

# Describe ingress
kubectl describe ingress <ingress-name> -n <namespace>

# Check ingress controller pods
kubectl get pods -n <ingress-namespace> -l app=<ingress-controller>

# Check ingress controller logs
kubectl logs -n <ingress-namespace> -l app=<ingress-controller>
```

### DNS
```bash
# Check CoreDNS pods
kubectl get pods -n kube-system | grep coredns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Test DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup <service-name>.<namespace>.svc.cluster.local

# Test DNS from pod
kubectl exec -it <pod-name> -n <namespace> -- nslookup <service-name>.<namespace>.svc.cluster.local
```

### Network Policies
```bash
# Check network policies
kubectl get networkpolicies -n <namespace>

# Describe network policy
kubectl describe networkpolicy <policy-name> -n <namespace>

# Check network policy rules
kubectl get networkpolicy <policy-name> -n <namespace> -o yaml
```

### kube-proxy
```bash
# Check kube-proxy pods
kubectl get pods -n kube-system | grep kube-proxy

# Check kube-proxy logs
kubectl logs -n kube-system -l k8s-app=kube-proxy

# Check kube-proxy configuration
kubectl get configmap -n kube-system kube-proxy -o yaml
```

### Network Debugging
```bash
# Check pod network interfaces
kubectl exec <pod-name> -n <namespace> -- ip addr

# Check pod routing
kubectl exec <pod-name> -n <namespace> -- ip route

# Test connectivity between pods
kubectl exec <pod-1> -n <namespace> -- ping <pod-2-ip>

# Check service IP
kubectl get service <service-name> -n <namespace> -o jsonpath='{.spec.clusterIP}'
```

## Best Practices

### Service Design
- **Service Discovery**: Use DNS names for service discovery
- **Service Types**: Choose appropriate service type (ClusterIP, NodePort, LoadBalancer)
- **Session Affinity**: Use session affinity when needed for stateful applications
- **Headless Services**: Use headless services for StatefulSets

### Ingress Configuration
- **Ingress Controller**: Ensure ingress controller is running and healthy
- **TLS/SSL**: Always use TLS for production ingress
- **Path-based Routing**: Use path-based routing for multiple services
- **Ingress Classes**: Use ingress classes for multiple controllers

### DNS Best Practices
- **CoreDNS Health**: Monitor CoreDNS pod health
- **DNS Caching**: Understand DNS caching behavior
- **External DNS**: Use ExternalDNS for cloud provider DNS integration
- **DNS Policies**: Configure DNS policies for pod DNS behavior

### Network Policies
- **Default Deny**: Start with deny-all and allow specific traffic
- **Namespace Isolation**: Use network policies for namespace isolation
- **Label Selectors**: Use consistent label selectors for policies
- **Policy Testing**: Test network policies in non-production first

### Troubleshooting Tips
- **Check Endpoints**: Verify service has endpoints (pods selected)
- **DNS Resolution**: Test DNS resolution from within pods
- **Network Policies**: Check if network policies are blocking traffic
- **Ingress Controller**: Verify ingress controller is processing ingress resources
- **kube-proxy**: Ensure kube-proxy is running on all nodes

## Additional Resources

### Official Documentation
- [Kubernetes Networking](https://kubernetes.io/docs/concepts/services-networking/) - Networking overview
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/) - Service guide
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) - Ingress guide
- [DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) - DNS guide
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) - Network policy guide

### Learning Resources
- [Service Types Explained](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) - Service types
- [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) - Controller options
- [CoreDNS Configuration](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/) - DNS configuration

### Tools & Utilities
- [CoreDNS](https://coredns.io/) - DNS server documentation
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/) - Popular ingress controller
- [Traefik](https://doc.traefik.io/traefik/) - Alternative ingress controller

### Community Resources
- [Kubernetes Slack #sig-network](https://slack.k8s.io/) - Networking discussions
- [Stack Overflow - Kubernetes Networking](https://stackoverflow.com/questions/tagged/kubernetes+networking) - Q&A

[Back to Main K8s Playbooks](../README.md)
