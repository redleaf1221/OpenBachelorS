# OBS Console Manual

## What is OBS Console

Open Bachelor Server implements a console to modify player data on the fly. You don't have to relogin to make changes take effect.

## How to Start OBS Console

1. Run `run_console.cmd`.

## OBS Console Commands

Command help can be found by issuing `some_command --help`.

> WARN: `-p`/`--player-id` takes phone number as argument, not uid (which is always `1`).

### `char` Command

Example:

```
char -p some_fake_phone_number -c char_1035_wisdel --level 1
```

