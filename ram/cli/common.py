"""Common utilities for CLI commands."""

from pathlib import Path

from ram.storage.config import Config
from ram.storage.context import ProjectContext
from ram.storage.scope import StorageScope


def get_active_scope(
    global_flag: bool = False,
    local_flag: bool = False,
    config: Config | None = None,
    context: ProjectContext | None = None,
) -> StorageScope:
    """Determine the active storage scope based on flags and context.

    Scope resolution order:
    1. Explicit --global flag → GLOBAL
    2. Explicit --local flag → LOCAL
    3. Project detected → LOCAL (default)
    4. No project → GLOBAL (fallback)

    Args:
        global_flag: True if --global flag was passed
        local_flag: True if --local flag was passed
        config: Configuration instance (loaded if None)
        context: Project context (detected if None)

    Returns:
        StorageScope (LOCAL or GLOBAL)

    Raises:
        ValueError: If both --global and --local flags are specified
    """
    # Check for conflicting flags
    if global_flag and local_flag:
        raise ValueError("Cannot specify both --global and --local flags")

    # Explicit flag overrides
    if global_flag:
        return StorageScope.GLOBAL
    if local_flag:
        return StorageScope.LOCAL

    # Load config and context if not provided
    if config is None:
        config = Config.load()
    if context is None:
        context = ProjectContext()

    # Check if in project directory
    if context.project_root is not None:
        return StorageScope.LOCAL

    # Fallback to global
    return StorageScope.GLOBAL


def format_scope_indicator(scope: StorageScope, context: ProjectContext | None = None) -> str:
    """Format a scope indicator for display in command output.

    Args:
        scope: The active storage scope
        context: Project context (for showing project name)

    Returns:
        Formatted string like "[local: my-project]" or "[global]"
    """
    if scope == StorageScope.LOCAL:
        if context and context.project_root:
            project_name = context.project_root.name
            return f"[cyan][local: {project_name}][/cyan]"
        return "[cyan][local][/cyan]"
    else:
        return "[magenta][global][/magenta]"
