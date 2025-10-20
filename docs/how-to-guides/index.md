---
sequential_nav: none
---

# How-to guides

% Include start summary

Our How-to guides help you **achieve common and specific goals**
while working with Canonical's robotics stack.
They may require you to understand and adapt the steps
to fit your specific requirements.

% Include stop summary

## Packaging

```{include} packaging/index.rst
   :start-after: .. Include start summary
   :end-before: .. Include stop summary
```

```{toctree}
:maxdepth: 2

packaging/index
```

## Operation

```{include} operation/index.rst
   :start-after: .. Include start summary
   :end-before: .. Include stop summary
```

```{toctree}
:maxdepth: 2

operation/index
```

## Maintenance

```{include} maintenance/index.rst
   :start-after: .. Include start summary
   :end-before: .. Include stop summary
```

```{toctree}
:maxdepth: 2

maintenance/index
```

## Security

```{include} security/hardening-your-robot.md
   :start-after: % Include start summary
   :end-before: % Include stop summary
```

* [Hardening your robot](./security/hardening-your-robot.md)

```{toctree}
:hidden:
:maxdepth: 2

Security <security/hardening-your-robot.md>
```
