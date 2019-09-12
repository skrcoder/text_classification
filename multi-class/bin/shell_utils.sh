#!/bin/bash

function check_ret()
{
    ret=$?
    commands=$1
    if [[ "" == "$commands" ]]; then
        echo "log command is NULL"
        exit 1
    fi

    if [[ 0 -ne $ret ]]; then
        echo "[${commands}] failed!"
        exit 1
    fi
}


function WriteLog()
{
    msg_date=`date +%Y-%m-%d" "%H:%M:%S`
    msg_begin=""
    msg_end=""
    if [ $# -eq 1 ]; then
        msg=$1
        echo "[${msg_date}]${msg}" >> ${LOG_PATH}/${LOG_FILE}
    elif [ $# -eq 2 ]
    then
        msg=$2
        runstat=$1
        if [ ${runstat} -eq 0 ]; then
            msg_begin="Success"
            msg_end="ok!"
        else
            msg_begin="Error"
            msg_end="fail!"
        fi
        echo "[${msg_date}][${msg_begin}]${msg} ${msg_end}" >> ${LOG_PATH}/${LOG_FILE}
        if [ ${runstat} -ne 0 ]; then
            echo "error when Task ${msg} runs at ${msg_date}" 
            exit 1
        fi
    else
        return
    fi
}
