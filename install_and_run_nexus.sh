#!/bin/bash

# 第一步: 安装依赖项
echo "正在安装依赖项..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git build-essential pkg-config libssl-dev unzip

# 第二步: 安装 Cargo 和 Rust
echo "正在安装 Cargo 和 Rust..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# 第三步: 检查版本
echo "检查版本..."
rustc --version
cargo --version
rustup update

# 第四步: 安装 Protobuf
echo "正在安装 Protobuf..."
wget https://github.com/protocolbuffers/protobuf/releases/download/v21.12/protoc-21.12-linux-x86_64.zip
unzip protoc-21.12-linux-x86_64.zip -d $HOME/.local
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 安装额外的组件
echo "安装额外的组件..."
cargo install protobuf-codegen
rustup target add riscv32i-unknown-none-elf
rustup component add rust-src

# 第五步: 安装 Nexus
echo "正在安装 Nexus..."
mkdir -p $HOME/.nexus
cd $HOME/.nexus
git clone https://github.com/nexus-xyz/network-api
cd network-api

# 检出新版本
git fetch --tags
git checkout $(git rev-list --tags --max-count=1)

# CLI 和构建
cd clients/cli
cargo clean
cargo build --release

# 完成提示
echo "Nexus CLI 安装成功。你现在可以手动运行它。"
