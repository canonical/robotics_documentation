---
sequential_nav: none
---

# Reference

% Include start summary

**Technical information** such as specifications, architecture, API documentation,
environment variables description, tool usage etc.

% Include stop summary

## Snapcraft

```{include} snapcraft/index.rst
   :start-after: .. Include start summary
   :end-before: .. Include stop summary
```

```{toctree}
:maxdepth: 2
:includehidden:

snapcraft/index
```

## ROS ESM

```{include} esm-package-list.md
   :start-after: % Include start summary
   :end-before: % Include stop summary
```

```{toctree}
:maxdepth: 2
:includehidden:

ROS ESM <esm-package-list>
```

## Observability

```{include} observability/index.rst
   :start-after: .. Include start summary
   :end-before: .. Include stop summary
```

```{toctree}
:maxdepth: 2
:includehidden:

observability/index
```

## Reference architecture

```{include} ref_architecture/reference_architecture.md
   :start-after: % Include start summary
   :end-before: % Include stop summary
```

```{toctree}
:maxdepth: 2
:includehidden:

ref_architecture/reference_architecture
```
