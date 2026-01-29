import os
import sys
import subprocess
import ctypes
import urllib.request
import zipfile
import shutil
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

class TerminalInterface:
    def __init__(self):
        self.cwd = os.getcwd()
        self.tools_dir = os.path.join(self.cwd, "tools")
        self.nsudo_path = os.path.join(self.tools_dir, "NSudoLC.exe")
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def colorize(self, text, color):
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'reset': '\033[0m'
        }
        return f"{colors.get(color, '')}{text}{colors['reset']}"
    
    def run_powershell(self, command):
        try:
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', command],
                capture_output=True,
                text=True
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return None, str(e), 1
    
    def download_nsudo(self):
        if os.path.exists(self.nsudo_path):
            return True
            
        print(self.colorize("\n📥 Downloading NSudoLC...", 'yellow'))
        
        try:
            import io
            os.makedirs(self.tools_dir, exist_ok=True)
            
            url = "https://github.com/M2TeamArchived/NSudo/releases/download/9.0-Preview1/NSudo_9.0_Preview1_9.0.2676.0.zip"
            
            # Download to memory
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context
            
            with urllib.request.urlopen(url) as response:
                zip_data = io.BytesIO(response.read())
            
            print(self.colorize("✅ Downloaded", 'green'))
            
            # Extract from memory
            print(self.colorize("📦 Extracting...", 'yellow'))
            
            with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    if 'NSudoLC.exe' in member and 'x64' in member:
                        # Read file content and write directly
                        content = zip_ref.read(member)
                        with open(self.nsudo_path, 'wb') as f:
                            f.write(content)
                        print(self.colorize("✅ NSudoLC ready", 'green'))
                        return True
            
            print(self.colorize("❌ NSudoLC.exe not found in archive", 'red'))
            return False
            
        except Exception as e:
            print(self.colorize(f"❌ Error: {e}", 'red'))
            return False
    
    def disable_tamper_protection(self):
        print(self.colorize("\n⚡ Bypassing Tamper Protection with TrustedInstaller...", 'yellow'))
        
        if not self.download_nsudo():
            print(self.colorize("❌ Cannot proceed without NSudoLC", 'red'))
            return False
        
        try:
            # Multiple registry keys to disable defender
            registry_commands = [
                # Disable Tamper Protection
                'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Features" /v TamperProtection /t REG_DWORD /d 0 /f',
                # Disable Anti Spyware
                'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f',
                # Disable Real-time Monitoring via registry
                'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f',
                'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableBehaviorMonitoring /t REG_DWORD /d 1 /f',
                'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableOnAccessProtection /t REG_DWORD /d 1 /f',
                'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableScanOnRealtimeEnable /t REG_DWORD /d 1 /f',
                # Disable via Windows Defender key
                'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f',
            ]
            
            success_count = 0
            for reg_cmd in registry_commands:
                cmd = f'"{self.nsudo_path}" -U:T -P:E -Wait cmd /c "{reg_cmd}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    success_count += 1
            
            if success_count > 0:
                print(self.colorize(f"✅ Applied {success_count}/{len(registry_commands)} registry changes", 'green'))
                print(self.colorize("⚠️  Restart mungkin diperlukan untuk efek penuh", 'yellow'))
                return True
            else:
                print(self.colorize("❌ Failed to apply registry changes", 'red'))
                return False
                
        except Exception as e:
            print(self.colorize(f"❌ Error: {e}", 'red'))
            return False
    
    def enable_tamper_protection(self):
        print(self.colorize("\n⚡ Enabling Tamper Protection...", 'yellow'))
        
        if not os.path.exists(self.nsudo_path):
            if not self.download_nsudo():
                return False
        
        try:
            # Re-enable all defender settings
            registry_commands = [
                'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Features" /v TamperProtection /t REG_DWORD /d 5 /f',
                'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /f',
                'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableRealtimeMonitoring /f',
                'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableBehaviorMonitoring /f',
                'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableOnAccessProtection /f',
                'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableScanOnRealtimeEnable /f',
                'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 0 /f',
            ]
            
            for reg_cmd in registry_commands:
                cmd = f'"{self.nsudo_path}" -U:T -P:E -Wait cmd /c "{reg_cmd}"'
                subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            print(self.colorize("✅ Tamper Protection ENABLED!", 'green'))
            return True
            
        except Exception as e:
            print(self.colorize(f"❌ Error: {e}", 'red'))
            return False
    
    def show_banner(self):
        banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ███╗   ███╗ ██████╗██████╗  ██████╗    ██████╗ ██╗   ██╗██████╗ ║
║   ████╗ ████║██╔════╝██╔══██╗██╔════╝    ██╔══██╗╚██╗ ██╔╝██╔══██╗║
║   ██╔████╔██║██║     ██████╔╝██║         ██████╔╝ ╚████╔╝ ██████╔╝║
║   ██║╚██╔╝██║██║     ██╔═══╝ ██║         ██╔══██╗  ╚██╔╝  ██╔═══╝ ║
║   ██║ ╚═╝ ██║╚██████╗██║     ╚██████╗    ██████╔╝   ██║   ██║     ║
║   ╚═╝     ╚═╝ ╚═════╝╚═╝      ╚═════╝    ╚═════╝    ╚═╝   ╚═╝     ║
║                                                                   ║
║              MINECRAFT BEDROCK BYPASS TOOL v1.0                   ║
║                    [RUNNING AS ADMINISTRATOR]                     ║
║                              BY WLKR                              ║
╚═══════════════════════════════════════════════════════════════════╝
        """
        self.clear_screen()
        print(self.colorize(banner, 'cyan'))
    
    def show_main_menu(self):
        menu = """
╔═══════════════════════════════════════════════════════════════════╗
║                          MAIN MENU                                ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║   [1] 🎮 Unlock Minecraft (New Version)                           ║
║                                                                   ║
║   [2] 🎮 Unlock Minecraft (Old Version)                           ║
║                                                                   ║
║   [0] 🚪 Exit                                                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
        """
        print(self.colorize(menu, 'green'))
    
    def show_new_version_menu(self):
        menu = """
╔═══════════════════════════════════════════════════════════════════╗
║               UNLOCK MINECRAFT (NEW VERSION)                      ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║   [1] 🛡️  Turn Off Microsoft Antivirus                            ║
║                                                                   ║
║   [2] ⚡ Bypass                                                   ║
║                                                                   ║
║   [0] ↩️  Back to Main Menu                                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
        """
        print(self.colorize(menu, 'yellow'))
    
    def show_antivirus_menu(self):
        menu = """
╔═══════════════════════════════════════════════════════════════════╗
║               MICROSOFT DEFENDER SETTINGS                         ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║   [1] ⚡ Disable Tamper Protection (BYPASS)                       ║
║                                                                   ║
║   [2] 🔴 Disable Real-time Protection                             ║
║                                                                   ║
║   [3] ☁️  Disable Cloud-delivered Protection                       ║
║                                                                   ║
║   [4] 📤 Disable Automatic Sample Submission                      ║
║                                                                   ║
║   [5] 💀 Disable ALL Protections (Auto)                           ║
║                                                                   ║
║   [6] ✅ Re-enable ALL Protections                                ║
║                                                                   ║
║   [7] 📊 Check Current Status                                     ║
║                                                                   ║
║   [0] ↩️  Back                                                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
        """
        print(self.colorize(menu, 'red'))
    
    def show_old_version_menu(self):
        menu = """
╔═══════════════════════════════════════════════════════════════════╗
║               UNLOCK MINECRAFT (OLD VERSION)                      ║
╠═══════════════════════════════════════════════════════════════════╣
║  ⚠️  WARNING: WAJIB DOWNLOAD IOBIT UNLOCKER TERLEBIH DAHULU!       ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║   [1] � IObit Download (!)                                       ║
║                                                                   ║
║   [2] �🔧 Bypass with System                                       ║
║                                                                   ║
║   [0] ↩️  Back to Main Menu                                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
        """
        print(self.colorize(menu, 'magenta'))
    
    def iobit_workflow(self):
        print(self.colorize("\n📥 Membuka halaman download IObit Unlocker...", 'yellow'))
        url = "https://iobit-unlocker.softonic-id.com/"
        os.system(f"start {url}")
        print(self.colorize(f"Link: {url}", 'cyan'))
        
        print(self.colorize("\nLakukan instalasi IObit Unlocker sekarang.", 'white'))
        input(self.colorize("Tekan Enter jika instalasi SUDAH SELESAI...", 'green'))
        
        print(self.colorize("\n🗑️  INSTRUKSI PENGHAPUSAN FILE SYSTEM", 'red'))
        print(self.colorize("----------------------------------------", 'white'))
        
        sys32_target = os.path.join(os.environ['WINDIR'], 'System32', 'Windows.ApplicationModel.Store.dll')
        syswow_target = os.path.join(os.environ['WINDIR'], 'SysWOW64', 'Windows.ApplicationModel.Store.dll')
        
        targets = [
            ("System32", sys32_target),
            ("SysWOW64", syswow_target)
        ]
        
        for name, path in targets:
            print(self.colorize(f"\n📁 Target {name}:", 'yellow'))
            print(self.colorize(f"   {path}", 'cyan'))
            
            # Open explorer to the file if it exists
            if os.path.exists(path):
                subprocess.run(f'explorer /select,"{path}"')
                print(self.colorize(f"   👉 Explorer dibuka. Klik kanan file ini > IObit Unlocker", 'white'))
                print(self.colorize(f"   👉 Pilih opsi 'Unlock & Delete'", 'red'))
                input(self.colorize("   Tekan Enter jika sudah dihapus...", 'green'))
            else:
                print(self.colorize("   ✅ File tidak ditemukan (Sudah dihapus/aman).", 'green'))
        
        print(self.colorize("\n✅ Semua file target sudah diproses. Silakan lanjut ke menu Bypass.", 'green'))
    
    def disable_realtime_protection(self):
        print(self.colorize("\n⏳ Disabling Real-time Protection...", 'yellow'))
        cmd = "Set-MpPreference -DisableRealtimeMonitoring $true"
        stdout, stderr, code = self.run_powershell(cmd)
        if code == 0 and not stderr:
            print(self.colorize("✅ Real-time Protection DISABLED", 'green'))
        else:
            print(self.colorize(f"❌ Error: {stderr}", 'red'))
            print(self.colorize("💡 Tip: Jalankan opsi 1 dulu untuk bypass Tamper Protection", 'yellow'))
    
    def disable_cloud_protection(self):
        print(self.colorize("\n⏳ Disabling Cloud-delivered Protection...", 'yellow'))
        cmd = "Set-MpPreference -MAPSReporting Disabled"
        stdout, stderr, code = self.run_powershell(cmd)
        if code == 0 and not stderr:
            print(self.colorize("✅ Cloud-delivered Protection DISABLED", 'green'))
        else:
            print(self.colorize(f"❌ Error: {stderr}", 'red'))
    
    def disable_sample_submission(self):
        print(self.colorize("\n⏳ Disabling Automatic Sample Submission...", 'yellow'))
        cmd = "Set-MpPreference -SubmitSamplesConsent 2"
        stdout, stderr, code = self.run_powershell(cmd)
        if code == 0 and not stderr:
            print(self.colorize("✅ Automatic Sample Submission DISABLED", 'green'))
        else:
            print(self.colorize(f"❌ Error: {stderr}", 'red'))
    
    def disable_all_protections(self):
        print(self.colorize("\n💀 Disabling ALL Protections (Full Auto)...\n", 'red'))
        
        # Step 1: Bypass Tamper Protection
        self.disable_tamper_protection()
        
        # Step 2: Disable all other protections
        print(self.colorize("\n⏳ Disabling remaining protections...", 'yellow'))
        self.disable_realtime_protection()
        self.disable_cloud_protection()
        self.disable_sample_submission()
        
        print(self.colorize("\n✅ ALL Protections DISABLED!", 'green'))
    
    def enable_all_protections(self):
        print(self.colorize("\n⏳ Enabling ALL Protections...", 'yellow'))
        
        cmd1 = "Set-MpPreference -DisableRealtimeMonitoring $false"
        stdout, stderr, code = self.run_powershell(cmd1)
        if code == 0 and not stderr:
            print(self.colorize("✅ Real-time Protection ENABLED", 'green'))
        
        cmd2 = "Set-MpPreference -MAPSReporting Advanced"
        stdout, stderr, code = self.run_powershell(cmd2)
        if code == 0 and not stderr:
            print(self.colorize("✅ Cloud-delivered Protection ENABLED", 'green'))
        
        cmd3 = "Set-MpPreference -SubmitSamplesConsent 1"
        stdout, stderr, code = self.run_powershell(cmd3)
        if code == 0 and not stderr:
            print(self.colorize("✅ Automatic Sample Submission ENABLED", 'green'))
        
        self.enable_tamper_protection()
        
        print(self.colorize("\n✅ ALL Protections ENABLED", 'green'))
    
    def check_status(self):
        print(self.colorize("\n📊 Checking Defender Status...\n", 'cyan'))
        
        # Check Tamper Protection from registry
        cmd_tamper = 'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Features" /v TamperProtection'
        result = subprocess.run(cmd_tamper, shell=True, capture_output=True, text=True)
        if "0x0" in result.stdout:
            print(self.colorize("TamperProtection         : DISABLED (Bypassed)", 'green'))
        elif "0x5" in result.stdout:
            print(self.colorize("TamperProtection         : ENABLED", 'red'))
        else:
            print(f"TamperProtection         : Unknown")
        
        cmd = "Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, IoavProtectionEnabled, AntispywareEnabled, BehaviorMonitorEnabled | Format-List"
        stdout, stderr, code = self.run_powershell(cmd)
        if stdout:
            print(self.colorize(stdout, 'white'))
        if stderr:
            print(self.colorize(f"Error: {stderr}", 'red'))
    
    def bypass_new_version(self):
        print(self.colorize("\n⏳ Running bypass for new version...", 'yellow'))
        
        confirm = input(self.colorize("❓ Yakin ingin melanjutkan? (y/n): ", 'cyan')).strip().lower()
        if confirm != 'y':
            print(self.colorize("🚫 Operasi dibatalkan.", 'red'))
            return
        
        while True:
            drive = input(self.colorize("\n📂 Dimana letak XboxGames? (Masukan C atau D): ", 'cyan')).strip().upper()
            if drive in ['C', 'D']:
                break
            print(self.colorize("❌ Harap masukan C atau D!", 'red'))
        
        print(self.colorize(f"\n🔍 Auto indexing di Disk {drive}...", 'yellow'))
        
        target_path = f"{drive}:\\XboxGames\\Minecraft for Windows\\Content"
        
        if os.path.exists(target_path):
            print(self.colorize(f"✅ Index ditemukan: {target_path}", 'green'))
            
            # Define source folder using cwd
            source_folder = os.path.join(self.cwd, "Minecraft FIX - NEW", "Minecraft FIX")
            
            files_to_copy = [
                "dlllist.txt",
                "OnlineFix.url",
                "winmm.dll",
                "OnlineFix.ini"
            ]
            
            print(self.colorize("\n📦 Menyalin file bypass...", 'yellow'))
            
            if not os.path.exists(source_folder):
                print(self.colorize(f"❌ Folder sumber tidak ditemukan: {source_folder}", 'red'))
                print(self.colorize("Pastikan folder 'Minecraft FIX - NEW' ada di lokasi script ini.", 'white'))
                return

            all_success = True
            for filename in files_to_copy:
                src_file = os.path.join(source_folder, filename)
                dst_file = os.path.join(target_path, filename)
                
                if os.path.exists(dst_file):
                    print(self.colorize(f"⚠️  File sudah ada: {filename} (Skipped)", 'yellow'))
                    continue

                try:
                    if os.path.exists(src_file):
                        shutil.copy2(src_file, dst_file)
                        print(self.colorize(f"✅ Copied: {filename}", 'green'))
                    else:
                        print(self.colorize(f"❌ Source file not found: {filename}", 'red'))
                        all_success = False
                except Exception as e:
                    print(self.colorize(f"❌ Failed to copy {filename}: {e}", 'red'))
                    all_success = False
            
            if all_success:
                print(self.colorize("\n🎉 Selesai! Bypass berhasil dipasang.", 'green'))
            else:
                print(self.colorize("\n⚠️  Selesai dengan error. Beberapa file gagal disalin.", 'yellow'))
                
        else:
            print(self.colorize("❌ Folder XboxGames\\Minecraft for Windows\\Content tidak ditemukan!", 'red'))
            print(self.colorize(f"Checked: {target_path}", 'white'))
    
    def bypass_with_system(self):
        print(self.colorize("\n⏳ Running bypass with system...", 'yellow'))
        
        confirm = input(self.colorize("❓ Yakin ingin melanjutkan? (y/n): ", 'cyan')).strip().lower()
        if confirm != 'y':
            print(self.colorize("🚫 Operasi dibatalkan.", 'red'))
            return
        
        system32_path = os.path.join(os.environ['WINDIR'], 'System32')
        syswow64_path = os.path.join(os.environ['WINDIR'], 'SysWOW64')
        
        # Source paths
        src_sys32 = os.path.join(self.cwd, "Minecraft - OLD", "System32", "Windows.ApplicationModel.Store.dll")
        src_syswow = os.path.join(self.cwd, "Minecraft - OLD", "SysWOW64", "Windows.ApplicationModel.Store.dll")
        
        tasks = [
            (src_sys32, os.path.join(system32_path, "Windows.ApplicationModel.Store.dll"), "System32"),
            (src_syswow, os.path.join(syswow64_path, "Windows.ApplicationModel.Store.dll"), "SysWOW64")
        ]
        
        print(self.colorize("\n📦 Menyalin file System DLL...", 'yellow'))
        
        for src, dst, label in tasks:
            if os.path.exists(dst):
                print(self.colorize(f"⚠️  File {label} sudah exist: {dst} (Aborted)", 'red'))
                continue
                
            if not os.path.exists(src):
                print(self.colorize(f"❌ Source file not found for {label}: {src}", 'red'))
                continue
            
            try:
                # Need trusted installer/high privs for system folders, try normal copy first
                shutil.copy2(src, dst)
                print(self.colorize(f"✅ Success copy to {label}", 'green'))
            except PermissionError:
                print(self.colorize(f"❌ Permission denied for {label}. Need NSudo/TrustedInstaller context.", 'red'))
            except Exception as e:
                print(self.colorize(f"❌ Failed copy to {label}: {e}", 'red'))
        
        print(self.colorize("\nℹ️  Operasi selesai.", 'cyan'))
    
    def handle_antivirus_menu(self):
        while True:
            self.clear_screen()
            self.show_banner()
            self.show_antivirus_menu()
            
            choice = input(self.colorize("\n❯ Pilih menu [0-7]: ", 'cyan')).strip()
            
            if choice == '1':
                self.disable_tamper_protection()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '2':
                self.disable_realtime_protection()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '3':
                self.disable_cloud_protection()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '4':
                self.disable_sample_submission()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '5':
                self.disable_all_protections()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '6':
                self.enable_all_protections()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '7':
                self.check_status()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '0':
                break
            else:
                print(self.colorize("\n❌ Pilihan tidak valid!", 'red'))
                input(self.colorize("Tekan Enter untuk melanjutkan...", 'white'))
    
    def handle_new_version_menu(self):
        while True:
            self.clear_screen()
            self.show_banner()
            self.show_new_version_menu()
            
            choice = input(self.colorize("\n❯ Pilih menu [0-2]: ", 'cyan')).strip()
            
            if choice == '1':
                self.handle_antivirus_menu()
            elif choice == '2':
                self.bypass_new_version()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '0':
                break
            else:
                print(self.colorize("\n❌ Pilihan tidak valid!", 'red'))
                input(self.colorize("Tekan Enter untuk melanjutkan...", 'white'))
    
    def handle_old_version_menu(self):
        while True:
            self.clear_screen()
            self.show_banner()
            self.show_old_version_menu()
            
            choice = input(self.colorize("\n❯ Pilih menu [0-2]: ", 'cyan')).strip()
            
            if choice == '1':
                self.iobit_workflow()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '2':
                self.bypass_with_system()
                input(self.colorize("\nTekan Enter untuk melanjutkan...", 'white'))
            elif choice == '0':
                break
            else:
                print(self.colorize("\n❌ Pilihan tidak valid!", 'red'))
                input(self.colorize("Tekan Enter untuk melanjutkan...", 'white'))
    
    def run(self):
        while True:
            self.clear_screen()
            self.show_banner()
            self.show_main_menu()
            
            choice = input(self.colorize("\n❯ Pilih menu [0-2]: ", 'cyan')).strip()
            
            if choice == '1':
                self.handle_new_version_menu()
            elif choice == '2':
                self.handle_old_version_menu()
            elif choice == '0':
                print(self.colorize("\n👋 Goodbye!\n", 'yellow'))
                break
            else:
                print(self.colorize("\n❌ Pilihan tidak valid!", 'red'))
                input(self.colorize("Tekan Enter untuk melanjutkan...", 'white'))


if __name__ == "__main__":
    run_as_admin()
    terminal = TerminalInterface()
    terminal.run()
