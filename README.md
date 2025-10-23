# aitodo 🚀

一个基于 AI 的人性化命令行 To-Do List 工具，仿照 Taskwarrior，但拥有“灵魂”。

`aitodo` 不仅能帮你管理任务，还能在你添加任务时提供建议、在你需要动力时给予鼓励。它就像一个住在你终端里的效率伙伴。

## ✨ 功能特性

- **智能分析**：添加任务时，AI 会根据时间管理理论（艾森豪威尔矩阵）评估其重要性和紧迫性，并给出建议。
- **情绪价值**：使用 `next` 命令时，AI 会为你加油打气，提供个性化的鼓励。
- **宏观洞察**：使用 `list --ai`，AI 会分析你的整个任务列表，提供战略性建议。
- **强大组织**：支持 `project` 和 `tag` 对任务进行分类和过滤。
- **美观界面**：使用 `rich` 库，以清晰、美观的表格展示任务。
- **纯命令行**：所有操作都在你最熟悉的终端中完成，流畅高效。

## ⚙️ 安装与配置

**1. 克隆项目**

```bash
git clone <你的项目git仓库地址>
cd aitodo
```

**2. 设置 API 密钥**

`aitodo` 使用 Google Gemini API。你需要获取一个 API 密钥并将其设置为环境变量。

```bash
# 将下面这行命令添加到你的 .bashrc, .zshrc 或其他 shell 配置文件中
export GEMINI_API_KEY="你的Google_API_密钥"

# 然后重新加载你的 shell 配置
source ~/.zshrc 
# 或者 source ~/.bashrc
```

**3. 安装项目**

在项目的根目录（即包含 `pyproject.toml` 的目录）下，运行以下命令：

```bash
pip install .
```

这个命令会自动处理所有依赖项，并将 `aitodo` 命令安装到你的系统中，使其全局可用。

## 🚀 使用指南

现在你可以在任何路径下使用 `aitodo` 命令了！

---

### `add` - 添加新任务

添加一个任务，并可以选择性地指定项目和标签。

```bash
# 添加一个简单任务
aitodo add "写一篇关于aitodo的博客"

# 添加任务并指定项目和标签
aitodo add "完成词法分析作业" --project "编译原理" --tag "学习"
aitodo add "修复登录页的bug" -p "WebApp" -t "紧急"
```

---

### `list` - 列出任务

显示所有任务，或根据项目/标签进行过滤。

```bash
# 列出所有任务
aitodo list

# 按项目过滤
aitodo list --project "编译原理"

# 按标签过滤
aitodo list -t "紧急"

# 获取 AI 对当前列表的宏观分析
aitodo list --ai
```

---

### `done` - 完成任务

根据任务 ID 将其标记为完成。

```bash
aitodo done 3
```

---

### `delete` - 删除任务

```bash
aitodo delete 5
```

---

### `next` - 获取下一个建议任务

`aitodo` 会根据任务的紧迫性和重要性计算出下一个建议执行的任务，并给你一句鼓励！

```bash
aitodo next
```
