#!/bin/bash

# 更新和升级系统
sudo apt update && sudo apt upgrade -y

# 安装必要的依赖项
sudo apt install build-essential pkg-config libssl-dev git-all cargo -y

# 安装 Nexus Network CLI
curl https://cli.nexus.xyz/ | sh

# 安装 cargo-nexus
cargo install cargo-nexus

# 设置 prover id
PROVER_ID="OtMVKfVMx2h3ti8lT04MR1ADU6q1"
mkdir -p $HOME/.nexus
echo "$PROVER_ID" > $HOME/.nexus/prover-id

# 更改所有权并构建 Nexus 网络客户端
sudo chown -R $USER:$USER /root/.nexus/network-api/clients/cli/Cargo.lock
cd /root/.nexus/network-api/clients/cli
RUSTFLAGS="-Znext-lockfile-bump" cargo build

# 更新 Cargo.lock 文件
sed -i '1c\version = 3' /root/.nexus/network-api/clients/cli/Cargo.lock
rm Cargo.lock
cargo generate-lockfile

# 显示提示信息
echo "Nexus Network CLI 已安装并构建完成。"
