# Example 2: PKI Management with NoSQL (MongoDB)

This example demonstrates a **Public Key Infrastructure (PKI) Certificate Management System** using the microesb framework with a **NoSQL MongoDB** backend.

## Overview

Example 2 showcases how microesb can manage a hierarchical PKI system with three certificate types:

- **Certificate Authority (CA)** - Root certificate that signs server and client certificates
- **Server Certificates** - Signed by the CA, used for server authentication
- **Client Certificates** - Signed by the CA, used for client authentication with server verification

The example demonstrates:
- **NoSQL Document Storage** using MongoDB for flexible certificate data management
- **User-Defined Routing** with custom routing functions for MongoDB operations
- **Hierarchical Class Dependencies** showing CA → Server → Client certificate relationships
- **Smartcard/HSM Integration** for secure key storage (simulated in this example)

## Prerequisites

### MongoDB Requirement

This example requires a running MongoDB instance.

**Local MongoDB Installation:**

```bash
# Install MongoDB (varies by OS)
# For Ubuntu/Debian - install official MongoDB package:
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | \
   sudo gpg --dearmor -o /usr/share/keyrings/mongodb-archive-keyring.gpg
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | \
   sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Note:** Integration of example 2 into the docker example container with MongoDB support is planned for a future release.

### Python Dependencies

- Python 3.8 or later
- pymongo library
- microesb package

## Execution Order

**IMPORTANT:** The execution order of the scripts is critical due to certificate dependencies:

1. **First:** `00-main-ca.py` - Creates the Certificate Authority (CA)
2. **Second:** `01-main-server.py` - Creates Server Certificate (requires CA to exist)
3. **Third:** `02-main-client.py` - Creates Client Certificate (requires both CA and Server certificates to exist)

The hierarchical dependencies mean:
- Server certificates require the CA certificate to be created first (for signing)
- Client certificates require both CA (for signing) and Server certificates (for verification)

Running scripts out of order will result in missing certificate references in the MongoDB database.

## Execution

Navigate to the example directory and execute the scripts in the correct order:

```bash
# Step 1: Create Certificate Authority
python3 ./00-main-ca.py

# Step 2: Create Server Certificate
python3 ./01-main-server.py

# Step 3: Create Client Certificate
python3 ./02-main-client.py
```

## How It Works

### 1. Service Metadata

Each script uses different service metadata defining the certificate hierarchy:

- `service_metadata_ca` - CA certificate with Smartcard container
- `service_metadata_server` - Server certificate referencing CA
- `service_metadata_client` - Client certificate referencing both CA and Server

See: [service_call_metadata.py](service_call_metadata.py)

### 2. Class Hierarchy

The class reference structures define parent-child relationships:

```
CertCA
├── Smartcard
│   └── SmartcardContainer

CertServer
├── Smartcard
│   └── SmartcardContainer
└── CertCA (reference)
    └── Smartcard
        └── SmartcardContainer

CertClient
├── Smartcard
│   └── SmartcardContainer
├── CertCA (reference)
│   └── Smartcard
│       └── SmartcardContainer
└── CertServer (reference)
    └── Smartcard
        └── SmartcardContainer
```

See: [class_reference.py](class_reference.py)

### 3. User-Defined Routing

The `user_routing.py` module provides custom routing functions for MongoDB operations:

- `CertGetById(metadata)` - Retrieves certificate documents by ID
- `CertStore(metadata)` - Stores certificate documents
- `KeypairGenerate(metadata)` - Simulates key pair generation

See: [user_routing.py](user_routing.py)

### 4. MongoDB Collections

The example uses the following MongoDB collections in the `microesb` database:

- `cert` - Individual certificate data with properties
- `cert_hierarchy` - Complete certificate hierarchies with all related objects

### 5. Class Implementation

The implementation includes abstract base class `Cert` with three concrete implementations:

- `CertCA` - Certificate Authority implementation
- `CertServer` - Server certificate implementation
- `CertClient` - Client certificate implementation

Each class handles:
- Loading referenced certificate data from MongoDB
- Simulating OpenSSL certificate generation
- Smartcard/HSM key pair generation (simulated)
- Storing generated certificate data

See: [service_implementation.py](service_implementation.py)

## Post-Execution

After executing all three scripts, you can verify the data in MongoDB:

```bash
# Connect to MongoDB (using mongosh for MongoDB 5.0+)
mongosh

# Switch to microesb database
use microesb

# View individual certificates
db.cert.find().pretty()

# View complete certificate hierarchies
db.cert_hierarchy.find().pretty()
```

## Key Features Demonstrated

1. **NoSQL Flexibility:** MongoDB's schema-less design allows flexible certificate document structures
2. **Hierarchical Processing:** Automatic deserialization of nested certificate references
3. **Custom Routing:** User-defined routing functions for database operations
4. **Property Registration:** Dynamic property management with type checking and validation
5. **Recursive Class Hierarchy:** Automatic resolution and connection of certificate dependencies

## Additional Information

For more detailed documentation, see: [https://pythondocs.webcodex.de/micro-esb/examples.html](https://pythondocs.webcodex.de/micro-esb/examples.html)
