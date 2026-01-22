# Upstream Divergences from sphinx-docs-starter-pack

This file documents intentional divergences from the upstream sphinx-docs-starter-pack configuration that should be preserved during updates.

## .pymarkdown.json

### line-length (line 23-27)
- **Divergence**: Custom line length limit set to 85 characters
- **Reason**: Project-specific preference for stricter line length enforcement
- **Upstream**: Does not specify this custom limit

### no-inline-html (line 60-63)
- **Divergence**: Allows `<br>` HTML elements
- **Reason**: Some documentation requires line breaks in specific contexts
- **Upstream**: Does not allow any inline HTML elements by default
