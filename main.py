import typer
from typing import List, Optional, cast
from aitodo import core
from rich import print
from aitodo import llm
from rich.table import Table

app = typer.Typer()

@app.command()
def add(
    description: str = typer.Argument(..., help="任务描述"),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="将任务分配给一个项目。"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="为任务分配一个标签。")
):
    """
    添加一个新任务，可以选择性地为其指定项目和标签。
    """
    tasks = core.read_tasks()

    new_id = len(tasks) + 1 

    analysis = llm.get_llm_analysis(description, project=project, tag=tag)

    new_task = {
            "id" : new_id,
            "description": description,
            "done": False,
            "advice": analysis.get("advice", ""),
            "importance": analysis.get("importance", 0),
            "urgency": analysis.get("urgency", 0),
            "project": project,
            "tag": tag
            }
    tasks.append(new_task)
    core.write_tasks(tasks)
    print(f"添加了新任务：'[bold green]{description}[/bold green]'")
    if new_task["advice"]:
        print(f"💡 [bold yellow]建议:[/bold yellow] {new_task['advice']}")


@app.command(name="list")
def list_tasks(
    project: Optional[str] = typer.Option(None, "--project", "-p", help="按项目过滤任务。"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="按标签过滤任务。"),
    ai: bool = typer.Option(False, "--ai", help="获取对任务列表的 AI 宏观分析。")
):
    """
    列出任务，可选择按项目或标签进行过滤。
    """
    tasks = core.read_tasks()

    # 根据 project 和 tag 过滤任务
    filtered_tasks = tasks
    if project:
        filtered_tasks = [task for task in filtered_tasks if task.get("project") == project]
    if tag:
        filtered_tasks = [task for task in filtered_tasks if task.get("tag") == tag]

    if not filtered_tasks:
        print("🎉 没有找到匹配的任务！")
        return
    
    table = Table(title="📝 To-do List", show_header=True, header_style="bold magenta")
    table.add_column("状态", justify="center", width=4)
    table.add_column("ID", justify="right", style="dim")
    table.add_column("Project", style="green", width=15)
    table.add_column("Tag", style="blue", width=15)
    table.add_column("任务描述", style="cyan", no_wrap=False)
    table.add_column("重要性", justify="center")
    table.add_column("紧迫性", justify="center")

    def get_score_color(score: int) -> str:
        if score >= 8:
            return "bold red"
        elif score >= 4:
            return "bold yellow"
        return "bold green"

    for task in filtered_tasks:
        status = "[green]✅[/green]" if task["done"] else "[red]❌[/red]"
        project_str = task.get("project") or ""
        tag_str = task.get("tag") or ""
        importance = task.get("importance", 0)
        urgency = task.get("urgency", 0)
        
        importance_str = f"[{get_score_color(importance)}]{importance}[/]" if importance > 0 else "-"
        urgency_str = f"[{get_score_color(urgency)}]{urgency}[/]" if urgency > 0 else "-"

        table.add_row(status, str(task["id"]), project_str, tag_str, task["description"], importance_str, urgency_str)

    print(table)

    # AI 分析也应该基于过滤后的任务
    pending_tasks = [task for task in filtered_tasks if not task["done"]]
    if ai:
        print("\n🧠 [bold cyan]AI 助理正在分析您的任务...[/bold cyan]")
        if not pending_tasks:
            print("✨ 所有任务都已完成，AI 为你感到骄傲！继续保持！")
            return
            
        summary = llm.get_overall_analysis(pending_tasks)
        if summary:
            print(f"\n[bold]💡 宏观建议:[/bold]\n{summary}")

@app.command()
def done(task_id: int = typer.Argument(..., help="the task id you've done")):
    """
    根据任务id标记一个任务完成
    """
    tasks = core.read_tasks()
    task_found = False
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            task_found = True 
    if not task_found:
        print(f"❌ [bold red]错误: 未找到 ID 为 {task_id} 的任务。[/bold red]")
        raise typer.Exit(code=1)

    core.write_tasks(tasks)
    print(f"🎉 [bold blue]任务 {task_id} 已标记为完成！太棒了！[/bold blue]")


@app.command()
def delete(task_id: int = typer.Argument(..., help="the task id you want to delete")):
    """
    delete a task by its id
    """
    tasks = core.read_tasks()
    
    task_to_delete = None
    for task in tasks:
        if task["id"] == task_id:
            task_to_delete = task
            break

    if not task_to_delete:
        print(f"❌ [bold red]错误: 未找到 ID 为 {task_id} 的任务。[/bold red]")
        raise typer.Exit(code=1)

    tasks.remove(task_to_delete)
    reindexed_tasks = core.reindex_tasks(tasks)
    core.write_tasks(reindexed_tasks)
    print(f"🗑️ [bold]已删除任务 {task_id}: '{task_to_delete['description']}'[/bold]")


@app.command(name="next")
def next_task():
    """
    get the next task to do
    """
    tasks = core.read_tasks()
    pending_tasks = [task for task in tasks if not task["done"]]

    if not pending_tasks:
        print("🎉 所有任务都完成了！好好休息一下！")
        return

    next_task = max(pending_tasks, key=lambda task: task.get("urgency", 0) * 2 + task.get("importance", 0))

    print(f"🔥 [bold]接下来要做:[/bold] {next_task['description']}\n")
    
    # 实时生成鼓励的话语
    encouragement = llm.get_encouragement_for_task(next_task)
    if encouragement:
        print(f"💬 [bold magenta]AI 鼓励师:[/bold magenta] {encouragement}")



if __name__ == "__main__":
    app()
