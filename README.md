# Community Control

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

这是一个Home Assistant自定义组件，用于控制小区门禁系统。该组件通过向指定IP地址发送UDP数据包来开启门禁，数据包内容为用户指定的十六进制字符串。

## 功能

- 通过Home Assistant控制小区门禁
- 支持自定义UDP命令（十六进制格式）
- 可配置目标IP地址和端口
- 提供开关实体用于触发门禁开启

## 安装方法

### HACS安装（推荐）

1. 确保已经安装了[HACS](https://hacs.xyz/)
2. 在HACS中点击"集成"
3. 点击右上角的"+"按钮
4. 搜索"Community Control"并安装
5. 重启Home Assistant

### 手动安装

1. 将`custom_components/community_control`文件夹复制到您的Home Assistant配置目录下的`custom_components`文件夹中
2. 重启Home Assistant

## 配置方法

### 通过UI配置（推荐）

1. 在Home Assistant中，转到"配置" -> "集成"
2. 点击右下角的"添加集成"按钮
3. 搜索并选择"Community Control"
4. 填写以下信息:
   - 名称：为此门禁控制器指定一个名称
   - IP地址：门禁控制系统的IP地址
   - 端口：门禁控制系统的UDP端口（默认为8888）
   - 十六进制命令：用于开启门禁的十六进制命令字符串

### 通过YAML配置（传统方式）

在`configuration.yaml`文件中添加以下配置：

```yaml
switch:
  - platform: community_control
    name: "小区大门"
    host: "192.168.1.100"
    port: 8888
    command: "A1B2C3D4E5F6"
```

## 使用方法

安装并配置完成后，您将在Home Assistant中看到一个名为"小区大门"（或您自定义的名称）的开关实体。点击此开关即可发送命令开启门禁。

由于门禁控制通常是瞬时操作，开关会在激活后自动返回到关闭状态。

## 故障排除

如果遇到问题，请检查Home Assistant日志中是否有相关错误信息。常见问题包括：

- IP地址或端口配置错误
- 十六进制命令格式不正确
- 网络连接问题

## 注意事项

- 此组件仅发送UDP命令，不会接收任何确认信息
- 请确保您有权限操作门禁系统
- 建议在本地网络中使用，避免通过互联网远程控制门禁系统

## 贡献

欢迎提交问题和功能请求。如果您想贡献代码，请先开一个issue讨论您想要更改的内容。

[license-shield]: https://img.shields.io/github/license/yourusername/community_control.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/yourusername/community_control.svg?style=for-the-badge
[releases]: https://github.com/yourusername/community_control/releases
