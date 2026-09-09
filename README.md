# Bina MCP Server

Cross-platform MCP server for image/video workflows with an independent runtime from Dana.

## One-click
- Linux: `./install.sh`, then `./run.sh`
- macOS: `./install.command`, then `./run.command`
- Windows: `install.bat`, then `run.bat`

## Runtime
`python runner.py start|stop|restart|status|doctor|connection`

The runner detects an existing Bina process and avoids duplicate startup. If the configured port is occupied by another service, Bina automatically selects the next free port.

## Installer
`python installer.py --check|--repair|--update|--force`

## CLI
`bina doctor`, `bina status`, `bina connection`, `bina stop`, `bina restart`, `bina rotate-token`

Dana is never modified. Bina has independent data, runtime state, token and port management.
