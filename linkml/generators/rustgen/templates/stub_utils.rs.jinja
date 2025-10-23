use std::io::{Error, ErrorKind};
use std::path::{Component, PathBuf};

/// Convert a stub module name into a relative filesystem path.
///
/// The generator currently expects module names that mirror Python package
/// semantics (``foo.bar``) with optional hyphens. Hyphens are replaced with
/// underscores and dots map to directory separators. The helper rejects
/// absolute paths, traversal markers, or characters that cannot appear in
/// stub files so we never escape the designated stub root.
pub fn normalize_stub_module(name: &str) -> std::io::Result<PathBuf> {
    if name.is_empty() {
        return Err(Error::new(
            ErrorKind::InvalidInput,
            "module name may not be empty",
        ));
    }

    let normalized = name.replace('-', "_");
    let path_str = normalized.replace('.', "/");
    let path = PathBuf::from(&path_str);

    if path.is_absolute() {
        return Err(Error::new(
            ErrorKind::InvalidInput,
            format!("absolute module path `{name}` not allowed"),
        ));
    }

    for component in path.components() {
        match component {
            Component::Normal(part) => {
                let segment = part.to_string_lossy();
                if segment.is_empty() {
                    return Err(Error::new(
                        ErrorKind::InvalidInput,
                        format!("module name `{name}` contains an empty segment"),
                    ));
                }
                if segment == "." || segment == ".." {
                    return Err(Error::new(
                        ErrorKind::InvalidInput,
                        format!(
                            "module name `{name}` contains disallowed segment `{segment}`"
                        ),
                    ));
                }
                if segment
                    .chars()
                    .any(|ch| matches!(ch, '*' | '?' | '<' | '>' | '|' | ':' | '\\' | '/'))
                {
                    return Err(Error::new(
                        ErrorKind::InvalidInput,
                        format!(
                            "module name `{name}` contains invalid characters in `{segment}`"
                        ),
                    ));
                }
            }
            Component::CurDir | Component::ParentDir => {
                return Err(Error::new(
                    ErrorKind::InvalidInput,
                    format!("module name `{name}` attempts directory traversal"),
                ));
            }
            Component::RootDir | Component::Prefix(_) => {
                return Err(Error::new(
                    ErrorKind::InvalidInput,
                    format!("module name `{name}` resolves outside stub root"),
                ));
            }
        }
    }

    Ok(path)
}
