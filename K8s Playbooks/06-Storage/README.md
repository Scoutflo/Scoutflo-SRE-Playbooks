# Storage Playbooks

This folder contains **9 playbooks** for troubleshooting Kubernetes storage and volume issues.

## What is Kubernetes Storage?

Kubernetes storage allows pods to persist data beyond pod lifecycles. Key concepts:
- **PersistentVolume (PV)**: Storage provisioned in the cluster
- **PersistentVolumeClaim (PVC)**: Request for storage by a user
- **StorageClass**: Describes different classes of storage
- **Volume Mounts**: How pods access storage

## Common Issues Covered

- PersistentVolume issues
- PVC stuck in pending state
- Volume mount failures
- Storage class problems
- Volume attachment failures
- Storage filling up

## Playbooks in This Folder

1. `FailedAttachVolume-storage.md` - Failed to attach volume to pod
2. `KubePersistentVolumeErrors-storage.md` - PersistentVolume errors
3. `KubePersistentVolumeFillingUp-storage.md` - PersistentVolume running out of space
4. `PersistentVolumeNotResizing-storage.md` - PersistentVolume not resizing
5. `PersistentVolumeStuckinReleasedState-storage.md` - PV stuck in released state
6. `PodCannotAccessPersistentVolume-storage.md` - Pod cannot access PV
7. `PVCinLostState-storage.md` - PVC in lost state
8. `PVCPendingDueToStorageClassIssues-storage.md` - PVC pending due to storage class
9. `VolumeMountPermissionsDenied-storage.md` - Volume mount permission denied

## Quick Start

If you're experiencing storage issues:

1. **PVC Pending**: Start with `PVCPendingDueToStorageClassIssues-storage.md`
2. **Volume Mount Issues**: See `PodCannotAccessPersistentVolume-storage.md` or `VolumeMountPermissionsDenied-storage.md`
3. **Volume Attachment**: Check `FailedAttachVolume-storage.md`
4. **Storage Full**: See `KubePersistentVolumeFillingUp-storage.md`
5. **PV State Issues**: Check `PersistentVolumeStuckinReleasedState-storage.md` or `PVCinLostState-storage.md`

## Related Categories

- **03-Pods/**: Pod issues related to volume mounts
- **02-Nodes/**: Node disk pressure issues
- **09-Resource-Management/**: Resource quota issues affecting storage

## Understanding Playbook Steps

**Important**: These playbooks are designed for **AI agents** using natural language processing. The playbook steps use natural language instructions like:

- "Retrieve PVC `<pvc-name>` in namespace `<namespace>` and check PVC status and storage class"
- "Retrieve pod `<pod-name>` in namespace `<namespace>` and verify volume mounts and permissions"
- "Retrieve PersistentVolume `<pv-name>` and check PV status and reclaim policy"

AI agents interpret these instructions and execute the appropriate actions using available tools.

### Manual Verification Commands

If you need to manually verify or troubleshoot (outside of AI agent usage), here are equivalent kubectl commands:

**PVCs:**
```bash
# Check PVCs
kubectl get pvc -n <namespace>

# Describe PVC
kubectl describe pvc <pvc-name> -n <namespace>

# Check PVC status
kubectl get pvc <pvc-name> -n <namespace> -o jsonpath='{.status.phase}'
```

**PVs:**
```bash
# Check PVs
kubectl get pv

# Describe PV
kubectl describe pv <pv-name>
```

**Storage Classes:**
```bash
# Check storage classes
kubectl get storageclass

# Describe storage class
kubectl describe storageclass <storageclass-name>
```

**Pod Volume Information:**
```bash
# Check pod volume mounts
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 "Volumes:"
```

## Best Practices

### Storage Design
- **Storage Classes**: Use storage classes for dynamic provisioning
- **Access Modes**: Choose appropriate access modes (RWO, ROX, RWX)
- **Reclaim Policy**: Set reclaim policy based on data importance
- **Volume Modes**: Use Filesystem mode for most cases, Block mode for databases

### PVC Management
- **Resource Requests**: Set appropriate storage size requests
- **Storage Limits**: Consider using storage limits where supported
- **Backup Strategy**: Implement regular backups for persistent data
- **Volume Expansion**: Enable volume expansion where supported

### Performance Optimization
- **Storage Performance**: Choose storage class based on performance needs
- **Volume Types**: Use SSD for high-performance workloads
- **I/O Patterns**: Understand read/write patterns for storage selection
- **Snapshot Strategy**: Use volume snapshots for backups

### Troubleshooting Tips
- **Check PVC Status**: Verify PVC is Bound, not Pending
- **Storage Class**: Ensure storage class exists and is available
- **Node Affinity**: Check if PV has node affinity requirements
- **Volume Attachments**: Verify volume is attached to the node
- **Permissions**: Check file permissions on mounted volumes

## Additional Resources

### Official Documentation
- [Kubernetes Storage](https://kubernetes.io/docs/concepts/storage/) - Storage overview
- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) - PV guide
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/) - Storage class guide
- [Volume Snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/) - Snapshot guide
- [Volume Expansion](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims) - Volume expansion

### Learning Resources
- [Storage Best Practices](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#types-of-persistent-volumes) - Best practices
- [Dynamic Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/) - Dynamic provisioning guide
- [Volume Modes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#volume-mode) - Volume mode explanation

### Tools & Utilities
- [CSI Drivers](https://kubernetes-csi.github.io/docs/) - Container Storage Interface
- [Velero](https://velero.io/) - Backup and restore tool
- [Rook](https://rook.io/) - Storage orchestrator

### Community Resources
- [Kubernetes Slack #sig-storage](https://slack.k8s.io/) - Storage discussions
- [Stack Overflow - Kubernetes Storage](https://stackoverflow.com/questions/tagged/kubernetes+storage) - Q&A

[Back to Main K8s Playbooks](../README.md)
