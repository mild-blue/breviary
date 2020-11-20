#!/bin/bash
set -e

echo "Redeploying staging."
ssh "images@206.189.248.138" "cd /srv/breviary && ./redeploy.sh"
echo "Done."