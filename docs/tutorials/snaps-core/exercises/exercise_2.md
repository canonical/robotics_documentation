(tutorials-snaps-core-exercises-exercise-2)=

# Part-2 - exercise: Clean old unused maps over time

> This exercise requires having followed the {ref}`Tutorial 2: <tutorials-snaps-core-packaging-complex-robotics-software-with-snaps>`.

This exercise is meant for developers to train on solving a problem with snaps.
One can apply the freshly learned knowledge to a practical problem.

## Assignment

With the `mapping` daemon we might create a lot of maps.
Over time, this could become an issue.
All the maps image might take too much space on our disk and
if they are old they are most probably not necessary any more.
Our snap could embed another application that would check once in a while
if there is any old map that we don’t need any more.

The assignment is to add a new background process that runs every day.
This process must identify maps that are no longer used and older than one month.
Finally, we must delete those old maps.

We might want to have a look at the `timer` feature of daemons,
presented [in the documentation](https://snapcraft.io/docs/how-to-guides/manage-snaps/control-services/).

## Outcome

Our snap must have one more daemon called `map-cleaner`.
We shouldn’t have to call this application manually.
The `map-cleaner` daemon should clean up our old and unused maps once a day.

## Solution

````{dropdown} Click here for the solution

First we must create a script that cleans up the maps.
Our maps are located in `$SNAP_COMMON/map`.
Every map consists of two files, the `PGM` and the `YAML`.
Since our map symlink points to the `YAML` we will use
these files to identify the maps to delete.

Our `scripts/map-cleaner` script will look like:

```bash
#!/bin/sh
set -eu
dir="$SNAP_COMMON/map"
test -d "$dir" || exit 0
active=$(readlink -e "$dir/current_map.yaml")
find "$dir" -maxdepth 1 -type f -mtime +30 -name 'map-*.yaml' ! -path "$active" \
    -exec sh -ec '
        for yaml do
            rm -f -- "$yaml" "${yaml%.yaml}.pgm"
        done
    ' sh {} +
```

After making `scripts/map-cleaner` executable,
we can add the following to our `snapcraft.yaml`:

```yaml
  map-cleaner:
    command: map-cleaner
    daemon: oneshot
    timer: "04:00" # runs every day at 4 am
```

In order to “speed up” the tests,
we can of course replace the timer: `04:00` with timer: `00:00-24:00/288`
to run it every 5 minutes and remove the `-mtime +30` option in the find command.
````
