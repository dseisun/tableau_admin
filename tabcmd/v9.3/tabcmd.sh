#!/bin/bash
java -Xmx64m -Xss2048k -Djsse.enableSNIExtension=false -Dpid=$$ -Dlog.file=tabcmd.log -Dsession.file=tabcmd-session.xml -Din.progress.dir='./' -Dconsole.codepage=$LANG -Dconsole.cols=$COLUMNS -cp "lib/*" com.tableausoftware.tabcmd.Tabcmd "$@"
