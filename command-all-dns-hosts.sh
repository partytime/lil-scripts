hosts=$(cat /dns_host_list.txt|grep -v CNAME|egrep '10.0.100|10.0.101'|sort -ru|awk '{print $1}')

for i in $hosts
do
        ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no  -o ConnectTimeout=1 $i "(uptime)"
done
