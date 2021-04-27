 #!/bin/bash
set +x

installType=$1

print_help() {
    echo "usage: "
    echo "To install the SDK run ./install sdk"
    echo "To install the CLI run ./install cli"
}

if [ -z "$installType" ]; then
    print_help
    exit 1
fi

echo "running install.sh, install type is: $installType"

if [ $installType = 'sdk' ];then
    echo 'installing NVMeshSDK'
    tmpDir='sdk_install'
    projectDir='NVMeshSDK'
elif [ $installType = 'cli' ];then
    echo 'installing NVMeshCLI'
    tmpDir='nvmesh_cli_install'
    projectDir='NVMeshCLI'
else
    echo 'Unknown install type, exiting'
    print_help
    exit 1
fi

for v in 2 3; do
    pushd .
    pythonInterpreter=`which python$v`
    if [ $? -ne 0 ];then
        echo "python$v in not installed"
        continiue
    fi

    echo "------------------------- Installing SDK for python$v"

    mkdir -p /tmp/$tmpDir/$projectDir
    whoami=`whoami`

    echo $whoami
    sudo chown -R $whoami:$whoami /tmp/$tmpDir/

    cd ../$projectDir

    cp ./setup.py /tmp/$tmpDir/setup.py

    cp -r ./* /tmp/$tmpDir/$projectDir

    cd /tmp/$tmpDir/

    echo "" > $projectDir.py

    if [ $whoami = 'root' ];then
        $pythonInterpreter ./setup.py install --prefix /usr
    else
        sudo -E bash -c "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib; $pythonInterpreter ./setup.py install"
    fi

    sudo rm -rf /tmp/$tmpDir
    popd
done