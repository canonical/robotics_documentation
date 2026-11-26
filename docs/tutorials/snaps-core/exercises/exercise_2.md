(tutorials-snaps-core-exercises-exercise-2)=

# Part 2 exercise: Clean up unused maps

Extend the {ref}`Part 2 snap <tutorials-snaps-core-packaging-complex-robotics-software-with-snaps>`
with a timer that deletes saved maps older than 30 days, except the active
map. A map is a pair of files, not just the YAML file.

````{dropdown} One solution

Save the following script as `scripts/map-cleaner` and make it executable.
The `commands` part copies it to the root of the snap.

```sh
#!/bin/sh
set -eu
dir="$SNAP_COMMON/map"
test -d "$dir" || exit 0
active=$(readlink -e "$dir/current_map.yaml")
find "$dir" -maxdepth 1 -type f -name 'map-*.yaml' -mtime +30 \
    ! -path "$active" -exec sh -ec '
        for yaml do
            rm -- "$yaml" "${yaml%.yaml}.pgm"
        done
    ' sh {} +
```

If the active map cannot be resolved, the command fails before deleting
anything. Add a timed service to `apps`:

```yaml
  map-cleaner:
    command: map-cleaner
    daemon: oneshot
    timer: "04:00"
```

Rebuild and reinstall. In a disposable VM, save three maps. Use `touch -d
'32 days ago'` on one obsolete pair and on the active pair (not the symlink).
Start the service once with `sudo snap start turtlebot3-lyrical.map-cleaner`.
Only the obsolete, aged pair should disappear. Verify that Nav2 can still
load the active map.
````
