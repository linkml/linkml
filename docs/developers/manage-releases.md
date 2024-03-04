# How to Manage Releases of your LinkML Schema

Making a schema release in LinkML can be streamlined and efficient if done correctly. This guide will walk you through the process, focusing on semantic versioning, using GitHub for release notes, and ensuring your releases are consistent and well-documented.

Note: This guide assumes you use the [LinkML Cookiecutter](/howtos/linkml-project-cookiecutter) to seed your repository. If you did not,
then you should still be able to adapt this guide to your workflow.

## Follow Semantic Versioning (SemVer)

1. **Version Format:** Always use the `vX.X.X` format for your versions. This follows the [Semantic Versioning Specification](https://semver.org/), which is essential for maintaining clarity and consistency.

2. **Version Types:**
   - **Major (`X.0.0`):** Introduce breaking changes.
   - **Minor (`0.X.0`):** Add functionality in a backward-compatible manner.
   - **Patch (`0.0.X`):** Make backward-compatible bug fixes.

You may wish to document local conventions for how you apply semver
to your schema. See the [HCA guidelines](https://github.com/HumanCellAtlas/metadata-schema/blob/master/docs/evolution.md#schema-versioning) for an example.

## Using GitHub for Release Notes

1. **Automated Release Setup:** A GitHub action should be pre-configured to automatically create releases
   - If you configured your repo as a Python repo, schema releases will be auto-distributed to PyPI
   - Currently the standard release mechanism does not handle package repositories for other languages, you will need to manage this part yourself

2. **Creating a GitHub Release:**
   - When ready for a new release, create a GitHub release using the GitHub web interface
   - Ensure the version follows the `vX.X.X` format.
   - __NOTE__ if you used the cookiecutter, there is no need to manually set the release in your `pyproject.toml`, this should be left as `0.0.0`.

3. **Autogenerating Release Notes:**
   - Click the “Generate Release Notes” button to auto-fill from Pull Requests (PRs).
   - **Important:** You can tweak these notes, but ensure PR titles are clear and concise, as they form the basis of these notes.
   - Note that this procedure will auto-credit PR contributors, and mark first-time contributors, which is a good feature for ensuring attribution of contributions

4. **No Separate CHANGELOG:** Instead of maintaining a separate CHANGELOG file, all changes should be documented directly in the release notes.

5. **Post-Release Actions:**
   - After the release is created, the GitHub action triggers to publish the release to PyPI using the version specified (if configured as a PyPI repo)

6. **Handling Release Failures:**
   - If the PyPI release fails, make necessary fixes.
   - Delete the problematic GitHub release.
   - Recreate a new release with the same version.


## Making pre-releases

Sometimes you may want to make a pre-release. These should follow standard conventions:

- Using `vX.Y.ZrcN` as the version, where this is the `N`th pre-release candidate for `X.Y.Z` (which is not yet released)
- Select "this is a pre-release" (this will automatically tag the PyPI release as a pre-release)

### Best Practices

- **PR Titles:** Ensure these are descriptive yet concise. This is crucial as they are directly used in autogenerating release notes.
- **Regular Releases:** Frequent releases help in maintaining a consistent and up-to-date package.
- **Pre-Release Testing:** Always test the package thoroughly before creating a release to minimize failures.

## Database Migrations and Their Role in Releases

Database migrations are a critical aspect of managing and releasing updates in any software that relies on a database. They ensure that changes to the database schema and data are applied in a consistent, reliable, and reversible manner. When accompanying releases, database migrations play a key role in maintaining the integrity and performance of the application. Here's how to effectively incorporate database migrations into your release process:

### Understanding Database Migrations

1. **Definition:** A database migration refers to the process of moving from one version of a database schema to another, typically when the application code requires changes to the database structure or data.

2. **Purpose:** Migrations are essential for:
   - Applying schema changes (like adding or altering tables or columns).
   - Modifying existing data (like transforming values or adding new rows).
   - Ensuring that these changes can be applied across different environments (development, testing, production) in a controlled manner.

### Integrating Migrations in Releases

1. **Synchronizing with Code Changes:**
   - Migrations should be part of the same release as the corresponding application code changes.
   - This ensures that the database schema is always compatible with the application version.

2. **Version Control for Migrations:**
   - Store migration scripts in your version control system alongside your application code.
   - This practice helps in tracking changes and facilitates rollback if needed.

3. **Automated Migration Scripts:**
   - Use automated scripts or migration tools that can apply migrations in a consistent order.
   - This automation reduces human error and ensures a smooth transition between database versions.

4. **Testing Migrations:**
   - Always test migrations in a staging environment before applying them to production.
   - This testing should include both the application of the migration and the rollback process.

5. **Release Documentation:**
   - Include detailed notes about the database migrations in your release documentation.
   - This should cover what the migration does, any potential impacts, and rollback procedures.

6. **Monitoring Post-Release:**
   - After applying migrations in a production environment, monitor the application and database performance closely.
   - Be prepared to quickly address any issues that arise from the migration.

### Best Practices

- **Reversible Migrations:** Design migrations so they can be reversed without data loss. This is crucial for quick rollbacks in case of issues.
- **Incremental Changes:** Prefer small, incremental changes over large, complex migrations. This approach reduces risk and makes troubleshooting easier.
- **Communication:** Coordinate with the development team, database administrators, and operations team to ensure everyone is aware of the changes and their potential impact.
- **Backup:** Always backup the database before applying migrations, especially in a production environment.

### Conclusion

Database migrations are a vital component of a well-managed release process. By carefully planning, testing, and documenting these migrations, you can ensure smooth and successful releases that maintain the integrity and performance of your database-dependent applications.

## Conclusion

Following these guidelines ensures that your LinkML schema releases are efficient, consistent, and well-documented. Always remember the importance of semantic versioning and clear communication through your PR and issue titles.
