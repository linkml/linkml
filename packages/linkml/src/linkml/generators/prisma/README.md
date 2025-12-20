# Prisma Schema Generator

The Prisma generator converts LinkML schemas into [Prisma](https://www.prisma.io/) schema files for database ORM usage.

## Overview

Prisma is a modern database toolkit that uses a schema file to define your database models. This generator transforms LinkML schemas into Prisma schema format, allowing you to:

- Generate type-safe database clients from LinkML schemas
- Use Prisma's migration tools with LinkML models
- Integrate LinkML with Node.js/TypeScript applications

## Usage

### Command Line

```bash
# Basic usage
gen-prisma my_schema.yaml > schema.prisma

# Or using the Python module directly
python -m linkml.generators.prismagen my_schema.yaml > schema.prisma

# Specify database provider
python -m linkml.generators.prismagen --datasource-provider mysql my_schema.yaml

# Disable scalar arrays (for MySQL/SQLite)
python -m linkml.generators.prismagen --no-use-scalar-arrays my_schema.yaml
```

### Python API

```python
from linkml.generators.prismagen import PrismaGenerator

# Basic usage
gen = PrismaGenerator("my_schema.yaml")
prisma_schema = gen.serialize()

# With options
gen = PrismaGenerator(
    "my_schema.yaml",
    datasource_provider="postgresql",  # postgresql, mysql, sqlite, cockroachdb
    use_scalar_arrays=True             # Use String[] for multivalued slots
)
prisma_schema = gen.serialize()
```

## Features

### Type Mapping

LinkML types are mapped to Prisma scalar types:

| LinkML Type | Prisma Type |
|-------------|-------------|
| string      | String      |
| integer     | Int         |
| boolean     | Boolean     |
| float       | Float       |
| double      | Float       |
| decimal     | Decimal     |
| date        | DateTime    |
| datetime    | DateTime    |
| json        | Json        |
| bytes       | Bytes       |

### Supported Features

- **Basic types**: All LinkML scalar types
- **Enums**: Converted to Prisma enums
- **Identifiers**: Mapped to `@id` directive
- **Required fields**: Non-optional fields in Prisma
- **Multivalued slots**: Can use scalar arrays (PostgreSQL/CockroachDB) or join tables
- **Relationships**: One-to-many and many-to-many relationships

### Database Providers

Supported database providers:
- PostgreSQL (default) - supports scalar arrays
- MySQL - no scalar array support
- SQLite - no scalar array support
- CockroachDB - supports scalar arrays

## Example

### Input LinkML Schema

```yaml
id: https://example.org/person
name: person

classes:
  Person:
    attributes:
      id:
        identifier: true
        range: string
      name:
        range: string
        required: true
      age:
        range: integer
      status:
        range: StatusEnum

enums:
  StatusEnum:
    permissible_values:
      - ACTIVE
      - INACTIVE
```

### Output Prisma Schema

```prisma
// Prisma schema generated from LinkML schema: person
// @linkml:id https://example.org/person

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Enums
enum StatusEnum {
  ACTIVE
  INACTIVE
}

// Models
model Person {
  id       String       @id
  name     String
  age      Int?
  status   StatusEnum?
}
```

## Architecture

The generator uses a three-tier architecture:

1. **Type Mapping** (`type_mappings.py`): Maps LinkML types to Prisma types
2. **Model Preparation** (`prepare_prisma_models()`): Transforms schema to data structures
3. **Template Rendering** (`prisma_template.py`): Jinja2 template for output

The generator leverages the `RelationalModelTransformer` to normalize schemas, handling:
- Foreign key injection
- Join table creation for many-to-many relationships
- Multivalued slot normalization

## Limitations

- Scalar arrays only work with PostgreSQL and CockroachDB
- Some LinkML features (like inheritance) are preserved as comments only
- Complex constraints may need manual adjustment in the generated schema

## Next Steps

After generating a Prisma schema:

1. Save the output to `schema.prisma`
2. Set up your `DATABASE_URL` environment variable
3. Run `npx prisma migrate dev` to create migrations
4. Run `npx prisma generate` to generate the Prisma Client

See [Prisma documentation](https://www.prisma.io/docs/) for more details on using Prisma.
