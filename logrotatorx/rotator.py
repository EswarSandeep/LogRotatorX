"""
rotator.py

Size-based log rotation.
"""

# -----------------------------------------------------------------------------
# Standard Library
# -----------------------------------------------------------------------------

import shutil
from pathlib import Path

# -----------------------------------------------------------------------------
# Local Imports
# -----------------------------------------------------------------------------

from logrotatorx.exceptions import RotationError
from logrotatorx.logger import get_logger
from logrotatorx.utils import (
    ensure_directory,
    size_mb,
    timestamp,
)

logger = get_logger()


# -----------------------------------------------------------------------------
# Log Rotation
# -----------------------------------------------------------------------------

def rotate_log(
    log_file: str | Path,
    destination_dir: str | Path,
    max_size_mb: int,
) -> Path | None:
    """
    Rotate a log file when it exceeds the configured size.

    Parameters
    ----------
    log_file
        Active log file.

    destination_dir
        Directory where the rotated file will be created.

    max_size_mb
        Rotation threshold.

    Returns
    -------
    Path | None

        Path to the rotated file if rotation occurred,
        otherwise None.
    """

    source = Path(log_file)
    destination = Path(destination_dir)

    if not source.exists():
        return None

    if not source.is_file():
        return None

    current_size = size_mb(source)

    if current_size < max_size_mb:
        return None

    ensure_directory(destination)

    rotated_file = (
        destination
        / f"{source.name}.{timestamp()}"
    )

    logger.info(
        "Rotating %s",
        source,
    )

    try:

        #
        # Copy current log
        #

        shutil.copy2(
            source,
            rotated_file,
        )

        #
        # Copy-truncate
        #

        with open(
            source,
            "r+b",
        ) as file:

            file.truncate(0)

    except Exception as exc:

        #
        # Remove partial rotated file.
        #

        if rotated_file.exists():

            try:
                rotated_file.unlink()
            except Exception:
                pass

        raise RotationError(
            f"Failed to rotate '{source}'."
        ) from exc

    logger.info(
        "Rotation completed: %s",
        rotated_file,
    )

    return rotated_file
