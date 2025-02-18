#!/bin/bash

# 设置 web prover id
PROVER_ID="OtMVKfVMx2h3ti8lT04MR1ADU6q1"

# 安装依赖项
sudo apt update && sudo apt upgrade -y
sudo apt install build-essential pkg-config libssl-dev git-all protobuf-compiler -y

# 安装 Nexus Network CLI
curl https://cli.nexus.xyz/ | sh

# 设置 prover id
mkdir -p $HOME/.nexus
echo "$PROVER_ID" > $HOME/.nexus/prover-id

# 启动一个新的 screen 会话并运行 CLI 工具
screen -dmS nexus_cli_session bash -c "cargo nexus --release -- beta.orchestrator.nexus.xyz; exec bash"

# 显示提示信息
echo "Nexus Network CLI 已安装并在新的 screen 会话中运行。使用 'screen -r nexus_cli_session' 查看运行情况。"
