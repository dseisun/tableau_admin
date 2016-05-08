#!/bin/bash
TABCMD_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
java -Xmx64m -Xss2048k -Djsse.enableSNIExtension=false -Dpid=$$ -Dlog.file="$TABCMD_HOME/tabcmd.log" -Dsession.file="$TABCMD_HOME/tabcmd-session.xml" -Din.progress.dir="$TABCMD_HOME" -Dconsole.codepage=$LANG -Dconsole.cols=$COLUMNS -cp "$TABCMD_HOME/lib/*" com.tableausoftware.tabcmd.Tabcmd "$@"
