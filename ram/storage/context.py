"""Project context detection for Ragged Memory."""

from pathlib import Path


class ProjectContext:
    """Represents the current project directory and its associated local store.

    Attributes:
        project_root: Root directory of the project, or None if no project detected
        store_path: Path to the local .ragged_memory/ directory
    """

    def __init__(self, start_dir: Path | None = None):
        """Initialize project context.

        Args:
            start_dir: Directory to start searching from. Defaults to current working directory.
        """
        if start_dir is None:
            start_dir = Path.cwd()
        self.project_root = self._detect_project_root(start_dir)
        self.store_path = (
            self.project_root / ".ragged_memory" if self.project_root else None
        )

    def _detect_project_root(self, start_dir: Path) -> Path | None:
        """Search upward for .ragged_memory/ or .git/ to find project root.

        This traverses upward from start_dir looking for markers that indicate
        a project root. Returns the first directory containing either marker.

        Args:
            start_dir: Directory to start searching from

        Returns:
            Path to project root if found, None otherwise
        """
        current = start_dir.absolute()
        while current != current.parent:
            # Check for .ragged_memory/ marker (explicit project marker)
            if (current / ".ragged_memory").exists():
                return current
            # Check for .git/ marker (git repository root)
            if (current / ".git").exists():
                return current
            # Move up one directory
            current = current.parent
        return None

    def has_local_store(self) -> bool:
        """Check if project has local store initialized.

        Returns:
            True if .ragged_memory/ exists in project root, False otherwise
        """
        return self.store_path is not None and self.store_path.exists()
