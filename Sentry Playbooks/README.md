# Sentry Playbooks

This directory contains SRE playbooks for handling Sentry error issues. Playbooks are organized by category to help quickly locate the appropriate response procedure.

## Directory Structure

```
Sentry Playbooks/
├── 01-Error-Tracking/     # Exception handling and error patterns
├── 02-Performance/        # Transaction issues, latency, performance
├── 03-Release-Health/     # Release correlation, deployment issues
└── README.md
```

## Categories

### 01-Error-Tracking
Playbooks for exception handling and error patterns. This category includes:
- **Kafka Errors**: ConsumerError (ConnectionError, PartitionError, TopicNotFound)
- **Database Errors**: ConnectionError-ConnectionRefused, ProgrammingError (ColumnMissing, ConstraintViolation, RelationMissing, SyntaxError)
- **Redis Errors**: ConnectionError-ConnectionRefused
- **Application Errors**: MemoryError, UnhandledException, APICallFailed
- **Code Errors**: KeyError, ValidationError, ValueError, AttributeError, ImportError, IndexError

**Total Files**: 19

### 02-Performance
Playbooks for transaction issues, latency, and performance problems. This category includes:
- **Timeout Errors**: ConnectionTimeout (Database, Redis, API)
- **Query Performance**: QueryTimeout-Database
- **API Performance**: RequestTimeout-API

**Total Files**: 6

### 03-Release-Health
Playbooks for release correlation and deployment-related issues. This category includes playbooks that help diagnose issues tied to specific releases, deployments, or version changes.

**Total Files**: 0 (placeholder for future playbooks)

## Usage

1. When a Sentry alert fires, identify the error type from the issue details
2. Navigate to the appropriate category folder based on the error type
3. Find the matching playbook by error pattern
4. Follow the playbook steps for diagnosis and resolution

## Playbook Structure

Each playbook follows a consistent format:
- **Meaning**: What the error indicates and its context
- **Impact**: Business and technical impact of the error
- **Playbook**: Step-by-step investigation procedure
- **Diagnosis**: Analysis guidance based on collected data

## Priority Levels

Playbooks are sourced from different priority levels:
- **P0**: Critical issues requiring immediate attention
- **P1**: High-priority issues with significant impact
- **P2**: Medium-priority issues for standard response

## Contributing

When adding new playbooks:
1. Categorize based on the primary error type:
   - Error/exception handling -> `01-Error-Tracking/`
   - Timeout/latency/performance -> `02-Performance/`
   - Release/deployment correlation -> `03-Release-Health/`
2. Follow the existing naming convention: `ErrorType-SubType-Component-Error-application.md`
3. Use the standard playbook structure (Meaning, Impact, Playbook, Diagnosis)
