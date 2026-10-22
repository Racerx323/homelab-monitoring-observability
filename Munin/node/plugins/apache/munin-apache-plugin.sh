#!/bin/bash

# --- Version History ---
# v1.0.0 - 2025-05-21 - Initial script creation:
#                      - Munin config file for Apache status.
#                      - Symlinks for apache_accesses, apache_processes, apache_volume.
#                      - Restart munin-node.
#                      - Apache vhost for localhost with mod_status config.
#                      - Enable Apache site and restart Apache.
#                      - Optional directory creation for robustness.
# v1.0.1 - 2025-05-21 - Added automated check and enablement for Apache's mod_status.
# v1.0.2 - 2025-05-21 - Added check and enforcement of 755 permissions for /etc/munin/plugin-conf.d.
# v1.0.3 - 2025-05-21 - Corrected Apache VHost config: removed ExtendedStatus from <VirtualHost> block.
# v1.0.4 - 2025-05-21 - Added dependency check and auto-install for libparse-http-useragent-perl.
# --- Assumptions ---
# This script assumes apache2 and munin-node are installed via apt from standard Debian/Ubuntu repositories.

# Exit immediately if a command exits with a non-zero status.
set -e
# Treat unset variables as an error when substituting.
set -u
# Pipelines return the exit status of the last command to fail, or 0 if all succeed.
set -o pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Please use sudo." >&2
    exit 1
fi

# --- Dependency Check: libparse-http-useragent-perl ---
PACKAGE_TO_CHECK="libparse-http-useragent-perl"
echo "Info: Checking if $PACKAGE_TO_CHECK is installed..."
if ! dpkg -s "$PACKAGE_TO_CHECK" &>/dev/null; then
    echo "Info: $PACKAGE_TO_CHECK is not installed. Attempting to install it..."
    echo "Info: Running apt update..."
    apt update # If this fails, 'set -e' will cause the script to exit immediately.
    echo "Info: Installing $PACKAGE_TO_CHECK..."
    apt install -y "$PACKAGE_TO_CHECK" # If this fails, 'set -e' will cause the script to exit immediately.
    echo "Info: $PACKAGE_TO_CHECK installed successfully."
else
    echo "Info: $PACKAGE_TO_CHECK is already installed."
fi
# --- End of Dependency Check ---

echo "" # Add a blank line for better readability

# Define the target directory for the Munin plugin configuration
TARGET_DIR="/etc/munin/plugin-conf.d"
# Define the filename for the Apache plugin configuration
FILENAME="apache"
# Construct the full, absolute path to the configuration file
FULL_PATH="$TARGET_DIR/$FILENAME"

# --- Optional: Create the target directory if it doesn't exist ---
# This section is a good practice for script robustness.
# Note: Creating directories under /etc typically requires root privileges (sudo).
if [ ! -d "$TARGET_DIR" ]; then
    echo "Info: Target directory '$TARGET_DIR' does not exist. Attempting to create it..."
    # Create the directory and any necessary parent directories.
    # This command requires root privileges, which the script should have due to the initial check.
    mkdir -p "$TARGET_DIR" # If this command fails, 'set -e' will cause the script to exit immediately.
    # The check for $? -eq 0 and the else branch with exit 1 are redundant.
    echo "Info: Directory '$TARGET_DIR' created successfully."
fi
# --- End of Optional Directory Creation ---

# --- Ensure correct permissions for target directory ---
echo "Info: Checking permissions for directory '$TARGET_DIR'..."
current_perms=$(stat -c "%a" "$TARGET_DIR")
if [ "$current_perms" != "755" ]; then
    echo "Info: Permissions for directory '$TARGET_DIR' are '$current_perms'. Setting to 755."
    chmod 755 "$TARGET_DIR" # If this command fails, 'set -e' will cause the script to exit immediately.
    echo "Info: Permissions for '$TARGET_DIR' set to 755."
else
    echo "Info: Permissions for directory '$TARGET_DIR' are already 755."
fi
# --- End of Permission Check ---

echo "Attempting to create file '$FULL_PATH'..."

# Create the file and write the content using a here-document.
# Writing to this location typically requires root privileges (sudo).
cat <<EOF >"$FULL_PATH"
# Munin-node apache plugin configuration file
# file location: /etc/munin/plugin-conf.d/apache

# For Apache:
[apache*]
env.url http://localhost/server-status?auto
EOF

# Check if the file was created successfully
if [ -f "$FULL_PATH" ]; then # A more direct check that the file exists after cat
    echo "Success: File '$FULL_PATH' created with the specified content."
    echo "Info: Ensure file permissions and ownership are correct for Munin (e.g., chown munin:munin '$FULL_PATH')."
else
    # If 'cat' or redirection failed, 'set -e' should have exited. This is an extra safeguard.
    echo "Error: File '$FULL_PATH' was not created as expected." >&2
    exit 1
fi

# --- Create Plugin Symlinks ---
echo "" # Add a blank line for better readability
echo "Attempting to create Munin plugin symlinks for Apache..."

PLUGIN_SOURCE_DIR="/usr/share/munin/plugins"
PLUGIN_TARGET_DIR="/etc/munin/plugins"
PLUGINS_TO_LINK=(
    "apache_accesses"
    "apache_processes"
    "apache_volume"
)

# Ensure the plugin target directory exists (optional, similar to conf.d)
if [ ! -d "$PLUGIN_TARGET_DIR" ]; then
    echo "Info: Plugin target directory '$PLUGIN_TARGET_DIR' does not exist. Attempting to create it..."
    mkdir -p "$PLUGIN_TARGET_DIR" # If this command fails, 'set -e' will cause the script to exit immediately.
    # The check for $? -ne 0 and exit 1 are redundant.
    echo "Info: Directory '$PLUGIN_TARGET_DIR' created successfully."
fi

for plugin_name in "${PLUGINS_TO_LINK[@]}"; do
    source_plugin_path="$PLUGIN_SOURCE_DIR/$plugin_name"
    target_link_path="$PLUGIN_TARGET_DIR/$plugin_name"

    if [ ! -e "$source_plugin_path" ]; then
        echo "Warning: Source plugin '$source_plugin_path' does not exist. Skipping symlink creation for $plugin_name." >&2
        continue
    fi

    if [ -L "$target_link_path" ] && [ "$(readlink "$target_link_path")" = "$source_plugin_path" ]; then
        echo "Info: Symlink '$target_link_path' already exists and points to the correct source. Skipping."
    elif [ -e "$target_link_path" ]; then
        echo "Warning: '$target_link_path' already exists but is not the expected symlink or points elsewhere. Please check manually. Skipping." >&2
    else
        echo "Creating symlink: $target_link_path -> $source_plugin_path"
        ln -s "$source_plugin_path" "$target_link_path"
        # If 'ln -s' fails, 'set -e' will cause the script to exit immediately.
        # The success message is good.
        echo "Success: Symlink '$target_link_path' created."
    fi
done

echo "Plugin symlink creation process complete."

# --- Restart Munin-Node Service ---
echo ""
echo "Attempting to restart munin-node service..."
# Using systemctl as it's standard on modern systems
if command -v systemctl &>/dev/null; then
    systemctl restart munin-node
    # If 'systemctl restart' fails, 'set -e' will cause the script to exit immediately.
    echo "Success: munin-node service restarted."
else
    echo "Warning: 'systemctl' command not found. Please restart munin-node service manually (e.g., 'sudo service munin-node restart')." >&2
fi

# --- Create Apache Virtual Host for localhost ---
echo ""
echo "Attempting to create Apache virtual host for localhost..."

# Adjust this path if your Apache configuration directory is different
APACHE_SITES_AVAILABLE_DIR="/etc/apache2/sites-available"
VHOST_FILENAME="002-munin-localhost.conf" # Or 000-default.conf if you intend to modify the default
VHOST_FULL_PATH="$APACHE_SITES_AVAILABLE_DIR/$VHOST_FILENAME"

# Ensure the Apache sites-available directory exists (optional)
if [ ! -d "$APACHE_SITES_AVAILABLE_DIR" ]; then
    echo "Info: Apache sites-available directory '$APACHE_SITES_AVAILABLE_DIR' does not exist. Attempting to create it..."
    mkdir -p "$APACHE_SITES_AVAILABLE_DIR" # If this command fails, 'set -e' will cause the script to exit immediately.
    # The check for $? -ne 0 and exit 1 are redundant.
    echo "Info: Directory '$APACHE_SITES_AVAILABLE_DIR' created successfully."
fi

echo "Creating Apache virtual host file: $VHOST_FULL_PATH"
cat <<EOF >"$VHOST_FULL_PATH"
<VirtualHost *:80>
  ServerName localhost

  <IfModule mod_status.c>
    <Location /server-status>
        SetHandler server-status
        Order deny,allow
        Deny from all
        Allow from 127.0.0.1 localhost ::1 ip6-localhost
    </Location>
  </IfModule>
</VirtualHost>
EOF

if [ -f "$VHOST_FULL_PATH" ]; then # Check if file was actually created
    echo "Success: Apache virtual host file '$VHOST_FULL_PATH' created."
else
    # If 'cat' or redirection failed, 'set -e' should have exited. This is an extra safeguard.
    echo "Error: Apache virtual host file '$VHOST_FULL_PATH' was not created as expected." >&2
    exit 1
fi

# --- Ensure Apache mod_status is enabled ---
# Check if apache2ctl command is available
if command -v apache2ctl &>/dev/null; then
    # Check if mod_status is already loaded/enabled
    if ! apache2ctl -M 2>/dev/null | grep -q 'status_module'; then
        echo "Info: Apache mod_status module not detected as enabled. Attempting to enable it (this often sets ExtendedStatus On globally)..."
        a2enmod status # If this command fails, 'set -e' will cause the script to exit immediately.
        echo "Info: mod_status enabled. Apache restart (next step) will load it."
    else
        echo "Info: Apache mod_status module is already enabled."
    fi
else
    echo "Warning: 'apache2ctl' command not found. Cannot automatically check or enable mod_status. Please ensure it is enabled manually." >&2
fi

# --- Enable Apache Virtual Host and Restart Apache ---
echo ""
echo "Attempting to enable Apache virtual host '$VHOST_FILENAME'..."
# The a2ensite command might not be available on all systems (e.g., RHEL/CentOS based)
# This assumes a Debian/Ubuntu-like system.
if command -v a2ensite &>/dev/null; then
    a2ensite "$VHOST_FILENAME"
    # If 'a2ensite' fails, 'set -e' will cause the script to exit immediately.
    echo "Success: Apache site '$VHOST_FILENAME' enabled."

    echo "Attempting to restart Apache service..."
    # Using systemctl as it's standard on modern systems
    systemctl restart apache2
    # If 'systemctl restart' fails, 'set -e' will cause the script to exit immediately.
    echo "Success: Apache service restarted."
else
    echo "Warning: 'a2ensite' command not found. Please enable the site '$VHOST_FILENAME' and restart Apache manually." >&2
    echo "Info: For example, on RHEL/CentOS, you might just need to restart httpd if conf.d was used: 'sudo systemctl restart httpd'" >&2
fi

exit 0
