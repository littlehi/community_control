# Community Control - HACS 兼容组件

这个项目是一个Home Assistant自定义组件，用于控制小区门禁系统。该组件已经按照HACS (Home Assistant Community Store) 的要求进行了格式化和结构化，可以通过HACS进行安装和管理。

## 主要修改

为了使组件兼容HACS，我进行了以下修改：

1. 添加了HACS所需的文件：
   - `hacs.json` - HACS配置文件
   - `.github/workflows/` - GitHub Actions工作流程文件
   - `info.md` - HACS信息文件
   - `LICENSE` - MIT许可证文件

2. 更新了组件结构：
   - 完善了`__init__.py`文件，添加了正确的异步设置和卸载函数
   - 更新了`manifest.json`，添加了HACS所需的字段
   - 改进了`switch.py`，添加了设备信息和唯一ID

3. 改进了README.md：
   - 添加了HACS徽章
   - 添加了安装说明
   - 完善了文档结构

## 文件结构

```
community_control/
├── .github/
│   └── workflows/
│       ├── hassfest.yaml
│       └── validate.yaml
├── custom_components/
│   └── community_control/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── manifest.json
│       ├── strings.json
│       ├── switch.py
│       └── translations/
│           └── en.json
├── hacs.json
├── info.md
├── LICENSE
└── README.md
```

## 安装说明

现在用户可以通过两种方式安装此组件：

1. **通过HACS安装**：
   - 在HACS中添加自定义仓库
   - 搜索并安装"Community Control"

2. **手动安装**：
   - 下载仓库
   - 将`custom_components/community_control`文件夹复制到Home Assistant配置目录

## 后续步骤

要完成HACS集成，您需要：

1. 创建一个GitHub仓库
2. 上传所有文件
3. 在HACS中注册您的集成（可选）

这样，您的组件就可以通过HACS轻松安装和更新了。
