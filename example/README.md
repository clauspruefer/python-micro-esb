# Python MicroESB Examples

This directory contains comprehensive examples demonstrating different database paradigms and use cases with the microesb framework.

## Example 1: Hosting Use Case - Relational Database Transactions

Example 1 demonstrates the **classical relational database transactional model** using PostgreSQL.

**Key Features:**
- **ACID Transactions:** Demonstrates atomic operations with commit/rollback functionality
- **Relational Integrity:** Shows how to maintain referential integrity across related entities (Customer → Domain → DNS Records)
- **Transaction Management:** Illustrates proper database transaction handling with the microesb framework
- **Normalized Schema:** Uses a normalized PostgreSQL database schema with foreign key relationships

This example is ideal for understanding how microesb integrates with traditional SQL databases where data consistency and transaction atomicity are critical requirements.

## Example 2: PKI Management - NoSQL Document Model

Example 2 showcases the **NoSQL document-oriented model** using MongoDB.

**Key Features:**
- **Document Storage:** Demonstrates flexible schema design with MongoDB collections
- **Denormalized Data:** Shows how to work with embedded documents and flexible structures
- **Schema Evolution:** Illustrates the advantages of schema-less document storage
- **User-Defined Routing:** Implements custom routing functions for MongoDB CRUD operations
- **Horizontal Scalability:** Designed for scenarios requiring easy horizontal scaling

This example highlights how microesb seamlessly works with modern NoSQL databases, making it suitable for applications requiring rapid development, flexible data models, and high scalability.

## Database Model Comparison

| Aspect | Example 1 (PostgreSQL) | Example 2 (MongoDB) |
|--------|------------------------|---------------------|
| **Model** | Relational / Normalized | Document / Denormalized |
| **Transactions** | ACID compliant | Eventually consistent |
| **Schema** | Fixed schema | Flexible schema |
| **Relationships** | Foreign keys | Embedded documents |
| **Use Case** | Data integrity critical | Rapid development, scalability |

Refer to detailed documentation at: 
https://pythondocs.webcodex.de/micro-esb/examples.html

