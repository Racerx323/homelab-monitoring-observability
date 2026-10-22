#!/bin/bash
# File location - /opt/munin
# Exit immediately if a command exits with a non-zero status.
set -e
# Treat unset variables as an error when substituting.
set -u
# Pipe failures should be treated as errors.
set -o pipefail

TARGET_SCRIPT="/usr/share/munin/plugins/unbound_munin_"
PLUGIN_DIR="/etc/munin/plugins/"

# List all the suffixes for your symlinks
SUFFIXES=("hits" "queue" "memory" "by_type" "by_class" "by_opcode" "by_rcode" "by_flags" "histogram")

# Ensure the target script exists
if [ ! -f "${TARGET_SCRIPT}" ] && [ ! -L "${TARGET_SCRIPT}" ]; then
    echo "Error: Target script ${TARGET_SCRIPT} does not exist or is not a regular file/symlink." >&2
    exit 1
fi

# Ensure the plugin directory exists
if [ ! -d "${PLUGIN_DIR}" ]; then
    echo "Error: Plugin directory ${PLUGIN_DIR} does not exist or is not a directory." >&2
    # Optionally, you could try to create it: sudo mkdir -p "${PLUGIN_DIR}"
    exit 1
fi

for suffix in "${SUFFIXES[@]}"; do
    LINK_NAME="${PLUGIN_DIR}unbound_munin_${suffix}"
    echo "Creating symlink: ${LINK_NAME} -> ${TARGET_SCRIPT}"
    sudo ln -s "${TARGET_SCRIPT}" "${LINK_NAME}"
done

echo "Symlinks processed. All done!"

# Restart the munin-node service to apply changes
echo "Restarting munin-node service..."
sudo service munin-node restart
echo "Munin-node service restarted."
