from uml_mcp_openai.server import mcp


def main() -> None:
    """
    Entrypoint for running this MCP server directly: `python -m uml_mcp_openai.main`
    """
    mcp.run()


if __name__ == "__main__":
    main()
