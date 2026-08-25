"""Simple Calculator entry point."""

def main() -> None:
    """Run the command‑line interface."""
    from .cli import run
    run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")