# Sentry Error Tracking Playbooks

> **19 playbooks** for application exceptions and error handling.

## General Error Playbooks

| Playbook | Description |
|----------|-------------|
| [UnhandledException](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/UnhandledException-Error-application.md) | Unhandled exception troubleshooting |
| [MemoryError](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/MemoryError-Error-application.md) | Memory exhaustion errors |
| [APICallFailed](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/APICallFailed-Error-application.md) | External API call failures |

## Python Exception Playbooks

| Playbook | Description |
|----------|-------------|
| [AttributeError - MissingAttribute](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/AttributeError-MissingAttribute-Error-application.md) | Missing attribute errors |
| [ImportError - ModuleNotFound](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ImportError-ModuleNotFound-Error-application.md) | Module import failures |
| [IndexError - IndexOutOfRange](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/IndexError-IndexOutOfRange-Error-application.md) | Index out of range errors |
| [KeyError - MissingKey](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/KeyError-MissingKey-Error-application.md) | Missing dictionary key errors |
| [ValueError - InvalidValue](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ValueError-InvalidValue-Error-application.md) | Invalid value errors |
| [ValidationError - DataValidation](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ValidationError-DataValidation-Error-application.md) | Data validation failures |

## Database Error Playbooks

| Playbook | Description |
|----------|-------------|
| [DatabaseConnectionError - ConnectionRefused](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/DatabaseConnectionError-ConnectionRefused-Database-Error-application.md) | Database connection refused |
| [ConnectionError - ConnectionRefused (Database)](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ConnectionError-ConnectionRefused-Database-Error-application.md) | Database connection errors |
| [ProgrammingError - ColumnMissing](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ProgrammingError-ColumnMissing-Database-Error-application.md) | Missing database column |
| [ProgrammingError - ConstraintViolation](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ProgrammingError-ConstraintViolation-Database-Error-application.md) | Database constraint violations |
| [ProgrammingError - RelationMissing](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ProgrammingError-RelationMissing-Database-Error-application.md) | Missing database table/relation |
| [ProgrammingError - SyntaxError](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ProgrammingError-SyntaxError-Database-Error-application.md) | SQL syntax errors |

## Redis Error Playbooks

| Playbook | Description |
|----------|-------------|
| [ConnectionError - ConnectionRefused (Redis)](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ConnectionError-ConnectionRefused-Redis-Error-application.md) | Redis connection failures |

## Kafka Error Playbooks

| Playbook | Description |
|----------|-------------|
| [ConsumerError - ConnectionError](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ConsumerError-ConnectionError-Kafka-Error-application.md) | Kafka consumer connection errors |
| [ConsumerError - PartitionError](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ConsumerError-PartitionError-Kafka-Error-application.md) | Kafka partition errors |
| [ConsumerError - TopicNotFound](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/blob/master/Sentry%20Playbooks/01-Error-Tracking/ConsumerError-TopicNotFound-Kafka-Error-application.md) | Missing Kafka topic |

---

[Back to Sentry Overview](/sentry/) | [View on GitHub](https://github.com/Scoutflo/scoutflo-SRE-Playbooks/tree/master/Sentry%20Playbooks/01-Error-Tracking)
