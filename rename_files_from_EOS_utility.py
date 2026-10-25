#!/usr/bin/env python3
"""
照片/视频批量重命名工具
用法:
    python3 rename_files_from_EOS_utility.py          # 预览模式（默认）
    python3 rename_files_from_EOS_utility.py 0        # 预览模式
    python3 rename_files_from_EOS_utility.py 1        # 执行模式（实际重命名）
    python3 rename_files_from_EOS_utility.py dry-run  # 预览模式
    python3 rename_files_from_EOS_utility.py run      # 执行模式
"""

import os
import sys
import subprocess
from collections import defaultdict

# ====== 配置 ======
# 改成你的照片文件夹路径
folder = "/Users/ytian/Pictures/test/"
extensions = [".CR2", ".JPG", ".MOV"]  # 支持的大小写不敏感扩展名

# starting number
seq = 1858



# =================

def get_create_time(filepath):
    """用 exiftool 读取文件的 CreateDate，返回时间戳（秒）"""
    result = subprocess.run(
        ["exiftool", "-DateTimeOriginal", "-d", "%s", "-T", filepath],
        capture_output=True, text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise ValueError(f"无法读取 {filepath} 的创建时间")
    return int(result.stdout.strip())


def set_file_modify_time(filepath, timestamp):
    """设置文件的修改时间为指定时间戳（秒）"""
    subprocess.run(
        ["touch", "-t", timestamp.strftime("%Y%m%d%H%M.%S"), filepath],
        capture_output=True
    )


def main(seq):
    # 解析命令行参数
    mode = "preview"  # 默认预览模式
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["1", "run", "exec", "execute"]:
            mode = "execute"
        elif arg in ["0", "preview", "dry-run", "dry"]:
            mode = "preview"
        else:
            print(f"未知参数: {arg}")
            print("用法: python3 rename_files_from_EOS_utility.py [0|1|preview|dry-run|run|exec]")
            print("  0/preview/dry-run : 预览模式（只显示将执行的操作）")
            print("  1/run/exec        : 执行模式（实际重命名文件）")
            sys.exit(1)
    
    print(f"模式: {'预览模式（不会实际修改文件）' if mode == 'preview' else '执行模式（将实际重命名文件）'}")
    print()
    
    # 1. 收集所有文件
    files = []
    for ext in extensions:
        for f in os.listdir(folder):
            if f.upper().endswith(ext.upper()):
                files.append(os.path.join(folder, f))
    
    if not files:
        print("没有找到任何 CR2、JPG 或 MOV 文件")
        return
    
    # 2. 获取每个文件的创建时间
    file_time = {}
    for f in files:
        try:
            file_time[f] = get_create_time(f)
        except ValueError as e:
            print(f"警告: {e}，跳过该文件")
    
    # 3. 过滤掉无法读取时间的文件
    valid_files = [f for f in files if f in file_time]
    if not valid_files:
        print("没有可用的文件")
        return
    
    # 4. 按创建时间排序
    sorted_files = sorted(valid_files, key=lambda x: file_time[x])
    
    # 5. 分组：同一个基础名（无扩展名）的所有文件视为同一组
    groups = defaultdict(list)
    for f in sorted_files:
        base = os.path.splitext(f)[0]
        groups[base].append(f)
    
    # 6. 按每组的最早时间排序
    sorted_bases = sorted(groups.keys(), key=lambda x: min(file_time[f] for f in groups[x]))
    
    # 7. 生成新文件名并执行重命名
    print("将执行以下操作：")
    print("-" * 60)
    
    operations = []  # 记录所有操作 (old_path, new_path)
    
    for base in sorted_bases:
        files_in_group = groups[base]
        
        for f in files_in_group:
            ext = os.path.splitext(f)[1]
            new_name = f"IMG_{seq:04d}{ext}"
            new_path = os.path.join(folder, new_name)
            operations.append((f, new_path, seq))
        
        seq += 1
    
    # 显示操作
    for old, new, seq_num in operations:
        print(f"  {os.path.basename(old)} -> {os.path.basename(new)}")
    
    print("-" * 60)
    print(f"总计 {len(sorted_bases)} 组，将生成 {seq-1} 个序号")
    
    # 执行重命名
    if mode == "execute":
        print("\n正在执行重命名...")
        
        # 先保存每个文件的原始修改时间（文件系统修改时间）
        original_mtimes = {}
        for old, new, _ in operations:
            if os.path.exists(old):
                stat = os.stat(old)
                original_mtimes[old] = stat.st_mtime
        
        # 执行重命名
        for old, new, _ in operations:
            if os.path.exists(old):
                # 如果目标文件已存在，提示并跳过
                if os.path.exists(new):
                    print(f"  警告: {new} 已存在，跳过 {old}")
                    continue
                os.rename(old, new)
                print(f"  已重命名: {os.path.basename(old)} -> {os.path.basename(new)}")
        
        # 恢复文件的修改时间（使用原始的 st_mtime）
        for old, new, _ in operations:
            if os.path.exists(new) and old in original_mtimes:
                os.utime(new, (original_mtimes[old], original_mtimes[old]))
        
        print("\n重命名完成，文件修改时间已恢复")
    else:
        print("\n预览模式完成。要实际执行重命名，请运行:")
        print("  python3 rename_files_from_EOS_utility.py 1")
        print("或")
        print("  python3 rename_files_from_EOS_utility.py run")


if __name__ == "__main__":
    main(seq)
