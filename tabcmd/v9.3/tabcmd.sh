#!/bin/bash
java -Xmx64m -Xss2048k -Djsse.enableSNIExtension=false -Dpid=$$ -Dlog.file=$HOME/.tabcmd/tabcmd.log -Dsession.file=$HOME/.tabcmd/tabcmd-session.xml -Din.progress.dir=/home/dseisun/Novasyte/tabcmd/ -Dconsole.codepage=$LANG -Dconsole.cols=$COLUMNS -cp "/home/dseisun/Novasyte/tabcmd/lib/*" com.tableausoftware.tabcmd.Tabcmd "$@"
