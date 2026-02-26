#!/usr/bin/env pwsh
# AI-CLI - Terminal Interactive Launcher
# Version: 2.0

param(
    [switch]$Init,
    [switch]$Config,
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$configDir = Join-Path $env:APPDATA "AI-CLI"
$userConfigPath = Join-Path $configDir "config.json"
$defaultConfigPath = Join-Path $scriptDir "config.json"

# 确保用户配置目录存在
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# ==========================================
# 配置管理
# ==========================================
function Load-Config {
    # 优先读取用户配置目录
    if (Test-Path $userConfigPath) {
        return Get-Content $userConfigPath -Raw | ConvertFrom-Json
    }
    
    # 如果用户配置不存在，读取程序目录的默认配置
    if (Test-Path $defaultConfigPath) {
        return Get-Content $defaultConfigPath -Raw | ConvertFrom-Json
    }
    
    return $null
}

function Save-Config {
    param($config)
    # 始终保存到用户配置目录
    $config | ConvertTo-Json -Depth 10 | Set-Content $userConfigPath -Encoding UTF8
}

function Initialize-Config {
    if (Test-Path $userConfigPath) {
        Write-Host "Config already exists at: $userConfigPath" -ForegroundColor Yellow
        return
    }
    
    # 如果程序目录有默认配置，复制到用户目录
    if (Test-Path $defaultConfigPath) {
        Copy-Item $defaultConfigPath $userConfigPath -Force
        Write-Host "Config copied to: $userConfigPath" -ForegroundColor Green
        return
    }
    
    # 否则创建默认配置
    $defaultConfig = @{
        projects = @()
        tools = @(
            @{name="kiro-cli"; displayName="Kiro CLI"; wslInstall="npm install -g kiro-cli"; checkCommand="kiro-cli --version"}
            @{name="claude"; displayName="Claude Code"; winInstall="npm install -g @anthropic-ai/claude-code"; wslInstall="npm install -g @anthropic-ai/claude-code"; checkCommand="claude --version"}
        )
        settings = @{language="auto"; defaultEnv="wsl"; terminalEmulator="default"}
    }
    
    $defaultConfig | ConvertTo-Json -Depth 10 | Set-Content $userConfigPath -Encoding UTF8
    Write-Host "Config initialized at: $userConfigPath" -ForegroundColor Green
}

# ==========================================
# 路径转换
# ==========================================
function ConvertTo-WslPath {
    param([string]$WinPath)
    $linuxPath = $WinPath -replace '\\', '/'
    if ($linuxPath -match '^([a-zA-Z]):(.*)') {
        $drive = $Matches[1].ToLower()
        return "/mnt/$drive" + $Matches[2]
    }
    return $linuxPath
}

# ==========================================
# 工具检测（优化：批量检测 + 缓存）
# ==========================================
$script:toolCache = $null
$script:cacheTime = $null
$script:cacheTimeout = 300  # 5分钟缓存

function Get-AvailableTools {
    param($config, [switch]$Force)
    
    # 检查缓存
    if (-not $Force -and $script:toolCache -and $script:cacheTime) {
        $elapsed = (Get-Date) - $script:cacheTime
        if ($elapsed.TotalSeconds -lt $script:cacheTimeout) {
            return $script:toolCache
        }
    }
    
    # 批量检测 WSL 工具
    $wslTools = @($config.tools | Where-Object { $_.wslInstall } | ForEach-Object { $_.name })
    $wslAvailable = @{}
    if ($wslTools.Count -gt 0) {
        $toolList = $wslTools -join ' '
        $result = wsl.exe -e bash -ic "for tool in $toolList; do command -v `$tool 2>/dev/null && echo `$tool; done" 2>$null
        if ($result) {
            $result -split "`n" | Where-Object { $_ } | ForEach-Object {
                $wslAvailable[$_] = $true
            }
        }
    }
    
    # 批量检测 Windows 工具
    $winAvailable = @{}
    foreach ($tool in $config.tools) {
        if ($tool.winInstall) {
            $winAvailable[$tool.name] = $null -ne (Get-Command $tool.name -ErrorAction SilentlyContinue)
        }
    }
    
    # 构建结果
    $tools = @()
    foreach ($tool in $config.tools) {
        $tools += [PSCustomObject]@{
            Name = $tool.name
            DisplayName = $tool.displayName
            WinAvailable = $winAvailable[$tool.name] -eq $true
            WslAvailable = $wslAvailable[$tool.name] -eq $true
            WinInstall = $tool.winInstall
            WslInstall = $tool.wslInstall
        }
    }
    
    # 更新缓存
    $script:toolCache = $tools
    $script:cacheTime = Get-Date
    
    return $tools
}

# ==========================================
# 安装工具
# ==========================================
function Install-Tool {
    param($config)
    
    # 获取未安装的工具（强制刷新缓存）
    $allTools = Get-AvailableTools -config $config -Force
    $uninstalledTools = @()
    
    foreach ($tool in $allTools) {
        $hasInstall = $false
        if (-not $tool.WslAvailable -and $tool.WslInstall) {
            $uninstalledTools += [PSCustomObject]@{
                Name = "$($tool.DisplayName) [WSL]"
                Tool = $tool.Name
                Env = "wsl"
                Command = $tool.WslInstall
            }
            $hasInstall = $true
        }
        if (-not $tool.WinAvailable -and $tool.WinInstall) {
            $uninstalledTools += [PSCustomObject]@{
                Name = "$($tool.DisplayName) [Win]"
                Tool = $tool.Name
                Env = "win"
                Command = $tool.WinInstall
            }
            $hasInstall = $true
        }
    }
    
    if ($uninstalledTools.Count -eq 0) {
        Clear-Host
        Write-Host "`nAll tools are already installed!" -ForegroundColor Green
        Start-Sleep -Seconds 2
        return
    }
    
    # 选择要安装的工具
    $result = Get-UserSelection -items $uninstalledTools -title "Select Tool to Install" -allowBack $true
    
    if ($result.Back) { return }
    
    $selectedTool = $uninstalledTools[$result.Index]
    
    Clear-Host
    Write-Host "`nInstalling $($selectedTool.Name)..." -ForegroundColor Cyan
    Write-Host "Command: $($selectedTool.Command)" -ForegroundColor DarkGray
    Write-Host ""
    
    # 执行安装
    if ($selectedTool.Env -eq "wsl") {
        $installCmd = "wsl.exe -e bash -ic `"$($selectedTool.Command)`""
        Invoke-Expression $installCmd
    } else {
        Invoke-Expression $selectedTool.Command
    }
    
    # 清除缓存，下次重新检测
    $script:toolCache = $null
    $script:cacheTime = $null
    
    Write-Host "`nInstallation completed. Press any key to continue..." -ForegroundColor Green
    [Console]::ReadKey($true) | Out-Null
}

# ==========================================
# 终端启动
# ==========================================
function Start-DevSession {
    param(
        [string]$tool,
        [string]$env,
        [string]$projectName,
        [string]$projectPath,
        [hashtable]$envVars = @{},
        [string]$terminalEmulator = "default",
        [bool]$useTab = $false
    )
    
    $title = "$($tool.ToUpper()) - $projectName"
    
    # 构建环境变量设置命令
    $envSetup = ""
    if ($envVars.Count -gt 0) {
        if ($env -eq "wsl") {
            # WSL 环境：检测并转换 Windows 路径
            $envSetup = ($envVars.GetEnumerator() | ForEach-Object { 
                $value = $_.Value
                # 检测是否为 Windows 绝对路径 (C:\... 或 D:\...)
                if ($value -match '^[a-zA-Z]:\\') {
                    $value = ConvertTo-WslPath -WinPath $value
                }
                "export $($_.Key)='$value'"
            }) -join '; '
            $envSetup += "; "
        } else {
            $envSetup = ($envVars.GetEnumerator() | ForEach-Object { "set $($_.Key)=$($_.Value) & " }) -join ''
        }
    }
    
    if ($terminalEmulator -eq "wezterm" -and (Get-Command "wezterm" -ErrorAction SilentlyContinue)) {
        # WezTerm 启动
        if ($env -eq "wsl") {
            $wslPath = ConvertTo-WslPath $projectPath
            $cmd = "wezterm start --cwd `"$wslPath`" -- wsl.exe -e bash -ic `"cd '$wslPath' && $envSetup$tool`""
        } else {
            $cmd = "wezterm start --cwd `"$projectPath`" -- cmd.exe /k `"title $title & cd /d `"$projectPath`" & $envSetup$tool`""
        }
        Invoke-Expression $cmd
    } else {
        # 默认终端
        if ($env -eq "wsl") {
            $wslPath = ConvertTo-WslPath $projectPath
            $wslExe = "C:\Windows\System32\wsl.exe"
            $wslArgs = "-e bash -ic `"cd '$wslPath'; $envSetup$tool; exec bash`""
            
            if ($useTab -and (Get-Command "wt" -ErrorAction SilentlyContinue)) {
                Start-Process "wt" -ArgumentList "-w", "0", "new-tab", "--title", $title, "wsl", "-e", "bash", "-ic", "cd '$wslPath'; $envSetup$tool; exec bash"
            } else {
                Start-Process -FilePath $wslExe -ArgumentList $wslArgs
            }
        } else {
            $cmdArgs = "/k `"title $title & cd /d `"$projectPath`" & $envSetup$tool`""
            
            if ($useTab -and (Get-Command "wt" -ErrorAction SilentlyContinue)) {
                Start-Process "wt" -ArgumentList "-w", "0", "new-tab", "--title", $title, "cmd", "/k", "cd /d `"$projectPath`" & $envSetup$tool"
            } else {
                Start-Process -FilePath "cmd.exe" -ArgumentList $cmdArgs
            }
        }
    }
}

# ==========================================
# 交互式 UI
# ==========================================
function Read-InputWithPlaceholder {
    param(
        [string]$Prompt,
        [string]$Placeholder,
        [bool]$Required = $false
    )
    
    [Console]::CursorVisible = $true
    Write-Host "  $Prompt" -ForegroundColor Cyan -NoNewline
    if (-not [string]::IsNullOrWhiteSpace($Placeholder)) {
        Write-Host " [$Placeholder]" -ForegroundColor DarkGray -NoNewline
    }
    Write-Host ": " -NoNewline
    
    $input = Read-Host
    
    if ([string]::IsNullOrWhiteSpace($input)) {
        if ($Required -and [string]::IsNullOrWhiteSpace($Placeholder)) {
            return $null
        }
        return $Placeholder
    }
    
    return $input.Trim()
}

function Add-NewProject {
    param($config)
    
    Clear-Host
    Write-Host "`n  Add New Project" -ForegroundColor Cyan
    Write-Host ("  " + "=" * 60) -ForegroundColor DarkGray
    Write-Host ""
    
    # 输入项目名称
    $projectName = $null
    while ($null -eq $projectName) {
        $projectName = Read-InputWithPlaceholder -Prompt "Project Name" -Placeholder "" -Required $true
        
        if ([string]::IsNullOrWhiteSpace($projectName)) {
            Write-Host "  Project name is required!" -ForegroundColor Red
            continue
        }
        
        # 检查重复
        $exists = $config.projects | Where-Object { $_.name -eq $projectName }
        if ($exists) {
            Write-Host "  Project name '$projectName' already exists!" -ForegroundColor Red
            $projectName = $null
        }
    }
    
    # 输入项目路径
    $currentPath = (Get-Location).Path
    $projectPath = $null
    while ($null -eq $projectPath) {
        $projectPath = Read-InputWithPlaceholder -Prompt "Project Path" -Placeholder "" -Required $false
        
        # 如果为空，使用当前路径
        if ([string]::IsNullOrWhiteSpace($projectPath)) {
            $projectPath = $currentPath
        }
        
        # 检查路径是否存在
        if (-not (Test-Path $projectPath)) {
            Write-Host "  Path does not exist: $projectPath" -ForegroundColor Yellow
            Write-Host "  Create it? (Y/N): " -NoNewline -ForegroundColor Cyan
            $confirm = Read-Host
            if ($confirm -eq "Y" -or $confirm -eq "y") {
                try {
                    New-Item -ItemType Directory -Path $projectPath -Force | Out-Null
                    Write-Host "  Directory created successfully." -ForegroundColor Green
                } catch {
                    Write-Host "  Failed to create directory: $_" -ForegroundColor Red
                    $projectPath = $null
                }
            } else {
                $projectPath = $null
            }
        }
    }
    
    # 输入环境变量参数（可选）
    Write-Host ""
    Write-Host "  Environment Variables (optional, press Enter to skip)" -ForegroundColor Cyan
    Write-Host "  Format: KEY=VALUE, one per line, empty line to finish" -ForegroundColor DarkGray
    Write-Host ""
    
    $envVars = @{}
    while ($true) {
        Write-Host "  Env Var: " -NoNewline -ForegroundColor Cyan
        $envInput = Read-Host
        
        if ([string]::IsNullOrWhiteSpace($envInput)) {
            break
        }
        
        if ($envInput -match '^([^=]+)=(.*)$') {
            $key = $Matches[1].Trim()
            $value = $Matches[2].Trim()
            $envVars[$key] = $value
            Write-Host "    Added: $key=$value" -ForegroundColor Green
        } else {
            Write-Host "    Invalid format. Use KEY=VALUE" -ForegroundColor Red
        }
    }
    
    # 创建项目对象
    $newProject = @{
        name = $projectName
        path = $projectPath
    }
    
    if ($envVars.Count -gt 0) {
        $newProject.env = $envVars
    }
    
    # 确认添加
    Write-Host ""
    Write-Host "  Project Summary:" -ForegroundColor Cyan
    Write-Host "    Name: $projectName" -ForegroundColor White
    Write-Host "    Path: $projectPath" -ForegroundColor White
    if ($envVars.Count -gt 0) {
        Write-Host "    Env Vars: $($envVars.Count) variable(s)" -ForegroundColor White
        foreach ($key in $envVars.Keys) {
            Write-Host "      $key=$($envVars[$key])" -ForegroundColor DarkGray
        }
    }
    Write-Host ""
    Write-Host "  Add this project? (Y/N): " -NoNewline -ForegroundColor Cyan
    $confirm = Read-Host
    
    if ($confirm -eq "Y" -or $confirm -eq "y") {
        $config.projects += $newProject
        Save-Config -config $config
        Write-Host "  Project added successfully!" -ForegroundColor Green
        Start-Sleep -Seconds 1
        return $true
    } else {
        Write-Host "  Cancelled." -ForegroundColor Yellow
        Start-Sleep -Seconds 1
        return $false
    }
}

function Show-Menu {
    param($items, $title, [int]$selected = 0, [bool]$showTabHint = $false, [bool]$showAddProject = $false)
    
    $maxDisplay = [Math]::Min($items.Count, 15)
    $offset = [Math]::Max(0, $selected - $maxDisplay + 1)
    
    [Console]::CursorVisible = $false
    Clear-Host
    
    Write-Host "`n  $title" -ForegroundColor Cyan
    Write-Host ("  " + "=" * 60) -ForegroundColor DarkGray
    Write-Host ""
    
    for ($i = $offset; $i -lt [Math]::Min($offset + $maxDisplay, $items.Count); $i++) {
        $item = $items[$i]
        $prefix = if ($i -eq $selected) { "  >" } else { "   " }
        $color = if ($i -eq $selected) { "Green" } else { "White" }
        
        if ($item.PSObject.Properties.Name -contains "Description") {
            Write-Host "$prefix $($item.Name)" -ForegroundColor $color -NoNewline
            Write-Host " - $($item.Description)" -ForegroundColor DarkGray
        } elseif ($item.PSObject.Properties.Name -contains "Path") {
            Write-Host "$prefix $($item.Name)" -ForegroundColor $color -NoNewline
            Write-Host " ($($item.Path))" -ForegroundColor DarkGray
        } else {
            Write-Host "$prefix $item" -ForegroundColor $color
        }
    }
    
    Write-Host ""
    if ($showTabHint) {
        Write-Host "  [↑↓] Navigate  [Enter] New Window  [Ctrl+Enter] New Tab  [I] Install  [Esc] Back  [Q] Quit" -ForegroundColor DarkGray
    } elseif ($showAddProject) {
        Write-Host "  [↑↓] Navigate  [Enter] Select  [N] New Project  [Q] Quit" -ForegroundColor DarkGray
    } else {
        Write-Host "  [↑↓] Navigate  [Enter] Select  [Esc] Back  [Q] Quit" -ForegroundColor DarkGray
    }
}

function Get-UserSelection {
    param($items, $title, [bool]$showTabHint = $false, [bool]$allowBack = $false, [bool]$allowAddProject = $false)
    
    $selected = 0
    
    while ($true) {
        Show-Menu -items $items -title $title -selected $selected -showTabHint $showTabHint -showAddProject $allowAddProject
        
        $key = [Console]::ReadKey($true)
        
        # 检测 Ctrl+Enter
        if ($key.Modifiers -eq [ConsoleModifiers]::Control -and $key.Key -eq "Enter") {
            [Console]::CursorVisible = $true
            return @{Index = $selected; UseTab = $true; Back = $false; Install = $false; AddProject = $false}
        }
        
        switch ($key.Key) {
            "UpArrow" { $selected = [Math]::Max(0, $selected - 1) }
            "DownArrow" { $selected = [Math]::Min($items.Count - 1, $selected + 1) }
            "Enter" { 
                [Console]::CursorVisible = $true
                return @{Index = $selected; UseTab = $false; Back = $false; Install = $false; AddProject = $false}
            }
            "I" {
                if (-not $allowAddProject) {
                    [Console]::CursorVisible = $true
                    return @{Index = -1; UseTab = $false; Back = $false; Install = $true; AddProject = $false}
                }
            }
            "N" {
                if ($allowAddProject) {
                    [Console]::CursorVisible = $true
                    return @{Index = -1; UseTab = $false; Back = $false; Install = $false; AddProject = $true}
                }
            }
            "Escape" {
                if ($allowBack) {
                    [Console]::CursorVisible = $true
                    return @{Index = -1; UseTab = $false; Back = $true; Install = $false; AddProject = $false}
                }
            }
            "Q" { 
                [Console]::CursorVisible = $true
                exit 0 
            }
        }
    }
}

# ==========================================
# 主流程
# ==========================================
function Start-InteractiveLauncher {
    $config = Load-Config
    
    if ($null -eq $config) {
        Write-Host "Config not found. Run with -Init to create default config." -ForegroundColor Red
        exit 1
    }
    
    if ($config.projects.Count -eq 0) {
        Write-Host "No projects configured. Edit config.json to add projects." -ForegroundColor Yellow
        exit 1
    }
    
    # 检测是否安装 Windows Terminal
    $hasWindowsTerminal = $null -ne (Get-Command "wt" -ErrorAction SilentlyContinue)
    
    $currentProject = $null
    
    while ($true) {
        # 1. 选择项目（如果未选择或需要重新选择）
        if ($null -eq $currentProject) {
            $result = Get-UserSelection -items $config.projects -title "Select Project" -allowAddProject $true
            
            # 处理新增项目
            if ($result.AddProject) {
                $added = Add-NewProject -config $config
                if ($added) {
                    $config = Load-Config  # 重新加载配置
                }
                continue
            }
            
            $projectIdx = if ($result -is [hashtable]) { $result.Index } else { $result }
            $currentProject = $config.projects[$projectIdx]
        }
        
        # 2. 获取可用工具
        $tools = Get-AvailableTools -config $config
        $availableTools = @()
        
        foreach ($tool in $tools) {
            if ($tool.WslAvailable) {
                $availableTools += [PSCustomObject]@{
                    Name = "$($tool.DisplayName) [WSL]"
                    Tool = $tool.Name
                    Env = "wsl"
                }
            }
            if ($tool.WinAvailable) {
                $availableTools += [PSCustomObject]@{
                    Name = "$($tool.DisplayName) [Win]"
                    Tool = $tool.Name
                    Env = "win"
                }
            }
        }
        
        if ($availableTools.Count -eq 0) {
            Write-Host "No tools available. Install tools first." -ForegroundColor Red
            exit 1
        }
        
        # 3. 选择工具
        $result = Get-UserSelection -items $availableTools -title "Select AI Tool for $($currentProject.name)" -showTabHint $hasWindowsTerminal -allowBack $true
        
        # 处理安装请求
        if ($result.Install) {
            Install-Tool -config $config
            continue
        }
        
        # 处理返回
        if ($result.Back) {
            $currentProject = $null
            continue
        }
        
        $toolIdx = $result.Index
        $useTab = $result.UseTab
        $selectedTool = $availableTools[$toolIdx]
        
        # 4. 启动开发会话
        Clear-Host
        
        [string]$toolName = $selectedTool.Tool
        [string]$toolEnv = $selectedTool.Env
        [string]$projName = $currentProject.name
        [string]$projPath = $currentProject.path
        [hashtable]$projEnv = if ($currentProject.PSObject.Properties.Name -contains "env") { 
            $ht = @{}
            $currentProject.env.PSObject.Properties | ForEach-Object { $ht[$_.Name] = $_.Value }
            $ht
        } else { @{} }
        
        $launchMode = if ($useTab) { "new tab" } else { "new window" }
        Write-Host "`nLaunching $toolName [$($toolEnv.ToUpper())] for $projName ($launchMode)..." -ForegroundColor Green
        
        Start-DevSession -tool $toolName -env $toolEnv -projectName $projName -projectPath $projPath -envVars $projEnv -terminalEmulator $config.settings.terminalEmulator -useTab $useTab
        
        # 5. 显示提示并自动消失
        Write-Host "Session launched. Returning to tool selection..." -ForegroundColor DarkGray
        Start-Sleep -Seconds 2
    }
}

# ==========================================
# 入口
# ==========================================
if ($Init) {
    Initialize-Config
    exit 0
}

if ($Config) {
    $configToEdit = if (Test-Path $userConfigPath) { $userConfigPath } else { $defaultConfigPath }
    if (Test-Path $configToEdit) {
        if (Get-Command "code" -ErrorAction SilentlyContinue) {
            code $configToEdit
        } else {
            notepad $configToEdit
        }
    } else {
        Write-Host "Config not found. Run with -Init first." -ForegroundColor Red
    }
    exit 0
}

if ($Uninstall) {
    Write-Host "Uninstalling AI-CLI..." -ForegroundColor Yellow
    
    $installDir = "$env:LOCALAPPDATA\AI-CLI"
    
    # 删除安装目录
    if (Test-Path $installDir) {
        Remove-Item -Recurse -Force $installDir
        Write-Host "  Removed installation directory" -ForegroundColor Green
    }
    
    # 删除桌面快捷方式
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "AI-CLI.lnk"
    if (Test-Path $shortcutPath) {
        Remove-Item -Force $shortcutPath
        Write-Host "  Removed desktop shortcut" -ForegroundColor Green
    }
    
    # 从 PATH 环境变量中移除
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -like "*$installDir*") {
        $newPath = ($userPath -split ';' | Where-Object { $_ -ne $installDir }) -join ';'
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "  Removed from PATH" -ForegroundColor Green
    }
    
    Write-Host "`nUninstallation complete!" -ForegroundColor Green
    exit 0
}

Start-InteractiveLauncher
