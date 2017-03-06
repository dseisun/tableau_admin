#!/bin/bash
TABCMD_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
java -Xmx64m -Xss2048k -Djsse.enableSNIExtension=false -Dpid=$$ -Dlog.file=$TABCMD_HOME/.tabcmd/tabcmd.log -Dsession.file=$TABCMD_HOME/.tabcmd/tabcmd-session.xml -Din.progress.dir=$TABCMD_HOME/.tabcmd -Dconsole.codepage=$LANG -Dconsole.cols=$COLUMNS -jar $TABCMD_HOME/app-tabcmd-latest-jar.jar  "$@"