# Example Project Conventions (Ground Truth)

These are the actual project conventions that guided the implementation of Issue #47.
Use this file to verify what the AI extracts from the issue + diff pair.

---

## Architecture

- **Framework:** NestJS (Node.js)
- **ORM:** TypeORM with PostgreSQL
- **Pattern:** Controller → Service → Repository (3-layer architecture)
- Controllers handle HTTP concerns only (routing, params, response)
- Services contain all business logic
- Models define database entities with TypeORM decorators

## File & Folder Structure

- `src/models/` — TypeORM entity classes, one file per entity
- `src/services/` — business logic services, one file per domain
- `src/controllers/` — REST controllers, one file per resource
- `src/dto/` — Data Transfer Objects for request validation
- `src/tests/` — unit tests, named `*.spec.ts` alongside source structure
- `src/guards/` — authentication and authorization guards

## Naming Conventions

- Files: `kebab-case.type.ts` (e.g., `notification-preference.model.ts`)
- Classes: `PascalCase` (e.g., `NotificationPreferenceService`)
- Enums: `PascalCase` name, `UPPER_SNAKE_CASE` values
- Database tables: `snake_case` plural (e.g., `notification_preferences`)
- Database columns: `snake_case` (e.g., `user_id`, `event_type`)
- API endpoints: RESTful nested resources (e.g., `/api/users/:userId/resource`)

## Code Style

- Use `class-validator` decorators for DTO validation
- Use TypeORM `@Entity`, `@Column`, `@ManyToOne` decorators for models
- Use `readonly` for injected dependencies
- Use NestJS built-in exceptions (`BadRequestException`, etc.)
- Prefer `findOne` with `where` clause over query builder for simple lookups
- Enum-based columns use TypeORM `type: 'enum'` mapping

## Security Rules

- All user-specific endpoints use `AuthGuard` and `OwnerGuard`
- Business rules enforced at service level, not controller level
- Security-critical notifications cannot be disabled (server-side enforcement)

## Testing Conventions

- Unit tests use `jest` with `@nestjs/testing`
- Repository dependencies are mocked via `getRepositoryToken()`
- Test file naming: `[service-name].spec.ts`
- Test structure: `describe` → `beforeEach` setup → individual `it` blocks
- Focus on business rule edge cases (e.g., security constraint enforcement)

## Database Design

- UUIDs as primary keys (`@PrimaryGeneratedColumn('uuid')`)
- Cascade deletes on parent relationships (`onDelete: 'CASCADE'`)
- Default values specified in entity decorators (`default: true`)
- Enum columns stored as native PostgreSQL enums
