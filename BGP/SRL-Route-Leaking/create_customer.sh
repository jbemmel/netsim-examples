#!/bin/bash

#
# environment alias "create customer {name}" "bash ~/create_customer.sh {name}"
#

NAME="${1}"

LAST=`sr_cli "show /interface ethernet-1/1"`
regex='.*[.]([0-9]+) is .*'
[[ $LAST =~ $regex ]]
ID="$((${BASH_REMATCH[1]}+1))"

sr_cli --candidate-mode --commit-at-end --echo --debug << EOF
/network-instance ${NAME}
description "Test ${ID}"
type ip-vrf
# ...
EOF

exit $?
