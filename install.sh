#!/usr/bin/env bash

python=$1
pypi_index=$2
shift 2


[[ -z $python ]] && python=python3
[[ -z $pypi_index ]] && pypi_index=https://pypi.vnpy.com

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    uv venv --python $python
fi

# Activate virtual environment
source .venv/bin/activate

# Get and build ta-lib
function install-ta-lib()
{
    # install numpy first
    uv pip install numpy==2.2.3 --index-url $pypi_index

    pushd /tmp
    wget https://pip.vnpy.com/colletion/ta-lib-0.6.4-src.tar.gz
    tar -xf ta-lib-0.6.4-src.tar.gz
    cd ta-lib-0.6.4
    ./configure --prefix=/usr/local
    make -j1
    sudo make install
    sudo ldconfig
    popd

    uv pip install ta-lib==0.6.4 --index-url $pypi_index
}
function ta-lib-exists()
{
    pkg-config --exists ta-lib 2>/dev/null || [ -f /usr/local/lib/libta_lib.so ] || [ -f /usr/lib/libta_lib.so ]
}
ta-lib-exists || install-ta-lib

# Install local Chinese language environment (requires sudo)
sudo locale-gen zh_CN.GB18030

# Install VeighNa
uv pip install . --index-url $pypi_index
