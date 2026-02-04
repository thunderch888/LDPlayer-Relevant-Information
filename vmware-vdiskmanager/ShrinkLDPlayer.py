#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShrinkLDPlayer - LDPlayer 磁碟壓縮工具（全自動版）
需要將 vmware-vdiskmanager.exe 放在同目錄
"""

import subprocess
import os
import sys
import time

def find_ldplayer():
    paths = [
        r"C:\LDPlayer\LDPlayer9",
        r"C:\LDPlayer\LDPlayer4.0", 
        r"C:\LDPlayer\LDPlayer3.0",
        r"D:\LDPlayer\LDPlayer9",
        r"D:\LDPlayer\LDPlayer4.0",
        r"D:\LDPlayer\LDPlayer3.0",
    ]
    for p in paths:
        if os.path.exists(os.path.join(p, "ld.exe")):
            return p
    return None

def list_instances(ld_path):
    vms = os.path.join(ld_path, "vms")
    instances = []
    if not os.path.exists(vms):
        return instances
    for name in os.listdir(vms):
        if name.startswith("leidian"):
            try:
                idx = int(name.replace("leidian", ""))
                instance_dir = os.path.join(vms, name)
                
                sdcard_path = os.path.join(instance_dir, "sdcard.vmdk")
                data_path = os.path.join(instance_dir, "data.vmdk")
                
                sdcard_size = os.path.getsize(sdcard_path) / 1024 / 1024 if os.path.exists(sdcard_path) else 0
                data_size = os.path.getsize(data_path) / 1024 / 1024 if os.path.exists(data_path) else 0
                
                if sdcard_size > 0 or data_size > 0:
                    instances.append((idx, sdcard_size, data_size))
            except: pass
    return sorted(instances)

def set_root(ldconsole, idx, enable):
    """啟用/關閉 Root"""
    subprocess.run([ldconsole, "modify", "--index", str(idx), "--root", "1" if enable else "0"], 
                   capture_output=True)

def launch_instance(ldconsole, idx):
    """啟動模擬器"""
    subprocess.run([ldconsole, "launch", "--index", str(idx)], capture_output=True)

def quit_instance(ldconsole, idx):
    """關閉模擬器"""
    subprocess.run([ldconsole, "quit", "--index", str(idx)], capture_output=True)

def is_running(ldconsole, idx):
    """檢查模擬器是否運行中"""
    result = subprocess.run([ldconsole, "isrunning", "--index", str(idx)], 
                           capture_output=True, text=True)
    return "running" in result.stdout.lower()

def wait_for_boot(ldconsole, ld_exe, idx, timeout=120):
    """等待模擬器啟動完成"""
    # 先等待模擬器進程啟動
    for _ in range(timeout):
        if is_running(ldconsole, idx):
            break
        time.sleep(1)
    
    # 再等待系統啟動完成
    for _ in range(timeout):
        result = subprocess.run([ld_exe, "-s", str(idx), "getprop sys.boot_completed"], 
                               capture_output=True, text=True)
        if "1" in result.stdout:
            return True
        time.sleep(2)
    return False

def wait_for_shutdown(ldconsole, idx, timeout=60):
    """等待模擬器完全關閉"""
    for _ in range(timeout):
        if not is_running(ldconsole, idx):
            return True
        time.sleep(1)
    return False

def zero_fill(ld_exe, idx, partition, count_mb=4096):
    """零填充（分段執行以顯示進度）"""
    fill_path = f"/{partition}/fillfile"
    
    # 寫入零檔案
    dd_cmd = f"su -c 'dd if=/dev/zero of={fill_path} bs=1048576 count={count_mb}'"
    subprocess.run([ld_exe, "-s", str(idx), dd_cmd], capture_output=True, text=True)
    
    # 刪除零檔案
    rm_cmd = f"su -c 'rm {fill_path}'"
    return subprocess.run([ld_exe, "-s", str(idx), rm_cmd], capture_output=True, text=True)

def main():
    print("=" * 55)
    print("  ShrinkLDPlayer - LDPlayer 磁碟壓縮工具（全自動版）")
    print("=" * 55)
    print()
    
    # 檢查 vdiskmanager
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    vdisk = os.path.join(script_dir, "vmware-vdiskmanager.exe")
    if not os.path.exists(vdisk):
        print("錯誤：請將 vmware-vdiskmanager.exe 放在同目錄")
        input("按 Enter 結束...")
        return
    
    # 找 LDPlayer
    ld_path = find_ldplayer()
    if not ld_path:
        ld_path = input("找不到 LDPlayer，請輸入安裝路徑: ").strip().strip('"')
    
    ld_exe = os.path.join(ld_path, "ld.exe")
    ldconsole = os.path.join(ld_path, "ldconsole.exe")
    
    if not os.path.exists(ld_exe):
        print("錯誤：找不到 ld.exe")
        input("按 Enter 結束...")
        return
    
    if not os.path.exists(ldconsole):
        print("錯誤：找不到 ldconsole.exe")
        input("按 Enter 結束...")
        return
    
    print(f"LDPlayer 路徑: {ld_path}\n")
    
    # 列出實例
    instances = list_instances(ld_path)
    if not instances:
        print("找不到任何模擬器實例")
        input("按 Enter 結束...")
        return
    
    print("可用的模擬器實例：")
    print("-" * 55)
    for idx, sdcard_size, data_size in instances:
        total = sdcard_size + data_size
        print(f"  [{idx}] leidian{idx} - sdcard: {sdcard_size:.0f} MB, data: {data_size:.0f} MB (共 {total:.0f} MB)")
    print("-" * 55)
    
    # 選擇實例
    choice = input("\n輸入實例 ID (多個用逗號分隔，或 all): ").strip().lower()
    if choice == "all":
        selected = [i[0] for i in instances]
    else:
        try:
            selected = [int(x.strip()) for x in choice.split(",")]
        except ValueError:
            print("輸入錯誤")
            input("按 Enter 結束...")
            return
    
    # 選擇模式
    print("\n選擇模式：")
    print("  [1] 只壓縮（快，效果差，需先手動關閉模擬器）")
    print("  [2] 全自動（啟用Root→啟動→零填充→關閉→壓縮）")
    mode = input("選擇 (1/2): ").strip()
    
    vms = os.path.join(ld_path, "vms")
    total_saved = 0
    
    if mode == "2":
        # ===== 全自動模式（並行處理） =====
        import threading
        
        print("\n請確保已手動開啟所有實例的 Root 權限")
        input("確認後按 Enter 開始...\n")
        
        # 1. 依序啟動所有模擬器（每秒啟動一個）
        print("[1/4] 啟動所有模擬器...")
        for idx in selected:
            print(f"      啟動實例 {idx}...", flush=True)
            launch_instance(ldconsole, idx)
            time.sleep(1)
        
        # 2. 等待所有模擬器啟動完成
        print("\n[2/4] 等待所有模擬器啟動完成...")
        for idx in selected:
            print(f"      等待實例 {idx}...", end=" ", flush=True)
            if wait_for_boot(ldconsole, ld_exe, idx, timeout=120):
                print("就緒")
            else:
                print("超時，繼續")
        
        time.sleep(3)  # 額外等待穩定
        
        # 3. 並行執行零填充
        print("\n[3/4] 並行零填充所有模擬器（請耐心等待）...")
        
        def do_zero_fill(idx):
            print(f"      實例 {idx}: 開始零填充...", flush=True)
            zero_fill(ld_exe, idx, "sdcard", 8192)
            zero_fill(ld_exe, idx, "data", 8192)
            print(f"      實例 {idx}: 零填充完成", flush=True)
        
        threads = []
        for idx in selected:
            t = threading.Thread(target=do_zero_fill, args=(idx,))
            threads.append(t)
            t.start()
        
        # 等待所有零填充完成
        for t in threads:
            t.join()
        
        print("\n      所有零填充完成！")
        
        # 4. 關閉所有模擬器
        print("\n[4/4] 關閉所有模擬器...")
        subprocess.run([ldconsole, "quitall"], capture_output=True)
        print("      等待 5 秒...")
        time.sleep(5)
        
        # 壓縮 VMDK
        print("\n開始壓縮 VMDK...")
        for idx in selected:
            print(f"\n實例 {idx}:")
            instance_dir = os.path.join(vms, f"leidian{idx}")
            
            for vmdk in ["sdcard.vmdk", "data.vmdk"]:
                vmdk_path = os.path.join(instance_dir, vmdk)
                if os.path.exists(vmdk_path):
                    before = os.path.getsize(vmdk_path) / 1024 / 1024
                    print(f"  {vmdk}: {before:.0f} MB")
                    
                    print(f"    碎片整理...", end=" ", flush=True)
                    subprocess.run([vdisk, "-d", vmdk_path], capture_output=True)
                    print("完成")
                    
                    print(f"    壓縮...", end=" ", flush=True)
                    result = subprocess.run([vdisk, "-k", vmdk_path], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        after = os.path.getsize(vmdk_path) / 1024 / 1024
                        saved = before - after
                        total_saved += saved
                        print(f"完成 → {after:.0f} MB (省 {saved:.0f} MB)")
                    else:
                        print(f"失敗")
    
    else:
        # ===== 只壓縮模式 =====
        print("\n請確保所有模擬器已完全關閉")
        input("確認後按 Enter 開始壓縮...")
        
        for idx in selected:
            print(f"\n實例 {idx}:")
            instance_dir = os.path.join(vms, f"leidian{idx}")
            
            if not os.path.exists(instance_dir):
                print(f"  找不到，跳過")
                continue
            
            for vmdk in ["sdcard.vmdk", "data.vmdk"]:
                vmdk_path = os.path.join(instance_dir, vmdk)
                if os.path.exists(vmdk_path):
                    before = os.path.getsize(vmdk_path) / 1024 / 1024
                    print(f"  {vmdk}: {before:.0f} MB")
                    
                    print(f"    碎片整理...", end=" ", flush=True)
                    subprocess.run([vdisk, "-d", vmdk_path], capture_output=True)
                    print("完成")
                    
                    print(f"    壓縮...", end=" ", flush=True)
                    result = subprocess.run([vdisk, "-k", vmdk_path], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        after = os.path.getsize(vmdk_path) / 1024 / 1024
                        saved = before - after
                        total_saved += saved
                        print(f"完成 → {after:.0f} MB (省 {saved:.0f} MB)")
                    else:
                        print(f"失敗")
    
    print("\n" + "=" * 55)
    print(f"  全部完成！總共節省: {total_saved:.0f} MB")
    print("=" * 55)
    input("\n按 Enter 結束...")

if __name__ == "__main__":
    main()
