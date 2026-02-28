#!/usr/bin/env pwsh
# AI-CLI - Terminal Interactive Launcher
# Version: 2.2

param(
    [switch]$Init,
    [switch]$Config,
    [switch]$Uninstall,
    [switch]$Help
)

# 参数兼容处理：支持 -- 前缀（转换为 PowerShell 的 - 前缀）
$rawArgs = $args
foreach ($arg in $rawArgs) {
    if ($arg -match '^--(.+)$') {
        $paramName = $matches[1]
        switch ($paramName.ToLower()) {
            'init' { $Init = $true }
            'config' { $Config = $true }
            'uninstall' { $Uninstall = $true }
            'help' { $Help = $true }
        }
    }
}

# 显示帮助信息
if ($Help) {
    Write-Host "`nAI-CLI - Terminal Interactive Launcher v2.2" -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor DarkGray
    Write-Host "`nUsage:" -ForegroundColor Yellow
    Write-Host "  ai-cli [options]`n"
    
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Init, --init         Initialize configuration file" -ForegroundColor Green
    Write-Host "                        Creates config in %APPDATA%\AI-CLI\config.json"
    Write-Host ""
    Write-Host "  -Config, --config     Edit configuration file" -ForegroundColor Green
    Write-Host "                        Opens config in VS Code or Notepad"
    Write-Host ""
    Write-Host "  -Uninstall, --uninstall" -ForegroundColor Green
    Write-Host "                        Uninstall AI-CLI"
    Write-Host "                        Removes program files, shortcuts, and PATH entry"
    Write-Host ""
    Write-Host "  -Help, --help         Show this help message" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  ai-cli                Start interactive launcher"
    Write-Host "  ai-cli -Init          Initialize configuration"
    Write-Host "  ai-cli --config       Edit configuration"
    Write-Host "  ai-cli --uninstall    Uninstall program"
    Write-Host ""
    
    Write-Host "Configuration:" -ForegroundColor Yellow
    Write-Host "  User Config:    %APPDATA%\AI-CLI\config.json"
    Write-Host "  Default Config: %LOCALAPPDATA%\AI-CLI\config.json"
    Write-Host ""
    
    exit 0
}


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
function Migrate-ConfigToTree {
    param($config)
    
    $needsMigration = $false
    $migratedProjects = @()
    
    foreach ($proj in $config.projects) {
        if (-not ($proj.PSObject.Properties.Name -contains "type")) {
            $needsMigration = $true
            $migratedProj = @{
                type = "project"
                name = $proj.name
                path = $proj.path
            }
            if ($proj.PSObject.Properties.Name -contains "env") {
                $migratedProj.env = $proj.env
            }
            $migratedProjects += $migratedProj
        } else {
            $migratedProjects += $proj
        }
    }
    
    if ($needsMigration) {
        $config.projects = $migratedProjects
        Save-Config -config $config
    }
    
    return $config
}

function Load-Config {
    $loadedConfig = $null
    
    # 优先读取用户配置目录
    if (Test-Path $userConfigPath) {
        $loadedConfig = Get-Content $userConfigPath -Raw | ConvertFrom-Json
    }
    # 如果用户配置不存在，读取程序目录的默认配置
    elseif (Test-Path $defaultConfigPath) {
        $loadedConfig = Get-Content $defaultConfigPath -Raw | ConvertFrom-Json
    }
    
    if ($null -ne $loadedConfig) {
        $loadedConfig = Migrate-ConfigToTree -config $loadedConfig
    }
    
    return $loadedConfig
}

function Normalize-ConfigArrays {
    param($obj)
    
    if ($obj -is [System.Collections.ArrayList]) {
        $arr = @()
        foreach ($item in $obj) {
            $arr += Normalize-ConfigArrays -obj $item
        }
        return $arr
    }
    
    if ($obj -is [hashtable]) {
        $normalized = @{}
        foreach ($key in $obj.Keys) {
            if ($key -eq "children") {
                $normalized[$key] = @($(Normalize-ConfigArrays -obj $obj[$key]))
            } else {
                $normalized[$key] = Normalize-ConfigArrays -obj $obj[$key]
            }
        }
        return $normalized
    }
    
    if ($obj.PSObject.Properties.Name -contains "children") {
        $normalized = @{}
        foreach ($prop in $obj.PSObject.Properties) {
            if ($prop.Name -eq "children") {
                $normalized[$prop.Name] = @($(Normalize-ConfigArrays -obj $prop.Value))
            } else {
                $normalized[$prop.Name] = Normalize-ConfigArrays -obj $prop.Value
            }
        }
        return $normalized
    }
    
    return $obj
}

function Save-Config {
    param($config)

    # 防御性检查
    if (-not $config) {
        Write-Host "Warning: Cannot save null config" -ForegroundColor Yellow
        return
    }

    # 规范化数组结构
    $normalized = @{
        projects = if ($config.projects) { @($(Normalize-ConfigArrays -obj $config.projects)) } else { @() }
        tools = if ($config.tools) { $config.tools } else { @() }
        settings = if ($config.settings) { $config.settings } else { @{} }
    }

    # 确保配置目录存在
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }

    # 使用原子写入避免数据丢失：先写入临时文件，再移动替换
    $tempPath = "$userConfigPath.tmp"
    $backupPath = "$userConfigPath.bak"

    try {
        # 写入临时文件
        $normalized | ConvertTo-Json -Depth 10 | Set-Content $tempPath -Encoding UTF8

        # 备份现有配置（如果存在）
        if (Test-Path $userConfigPath) {
            Copy-Item $userConfigPath $backupPath -Force -ErrorAction SilentlyContinue
        }

        # 原子替换：移动临时文件到目标位置
        Move-Item -Path $tempPath -Destination $userConfigPath -Force

        # 成功后删除备份
        if (Test-Path $backupPath) {
            Remove-Item $backupPath -Force -ErrorAction SilentlyContinue
        }
    } catch {
        # 写入失败，尝试从备份恢复
        Write-Host "Warning: Failed to save config: $_" -ForegroundColor Yellow
        if (Test-Path $backupPath) {
            try {
                Move-Item -Path $backupPath -Destination $userConfigPath -Force -ErrorAction SilentlyContinue
                Write-Host "Config restored from backup" -ForegroundColor Yellow
            } catch {}
        }
        # 清理临时文件
        if (Test-Path $tempPath) {
            Remove-Item $tempPath -Force -ErrorAction SilentlyContinue
        }
    }
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
# 工具检测（后台异步 + 前台按需）
# ==========================================
$script:bgDetectionJob = $null

function Get-AvailableTools {
    param($config, [switch]$Force)

    if (-not $config -or -not $config.tools) {
        return @()
    }

    # 如果强制检测，停止后台Job并执行前台检测
    if ($Force) {
        if ($script:bgDetectionJob -and $script:bgDetectionJob.State -eq 'Running') {
            Stop-Job $script:bgDetectionJob -ErrorAction SilentlyContinue
            Remove-Job $script:bgDetectionJob -ErrorAction SilentlyContinue
            $script:bgDetectionJob = $null
        }
        
        $detectedTools = Invoke-ToolDetection -config $config
        Update-ToolCacheInConfig -config $config -tools $detectedTools
    }

    # 从配置构建工具列表
    $tools = @()
    foreach ($tool in $config.tools) {
        $tools += [PSCustomObject]@{
            Name = $tool.name
            DisplayName = if ($tool.PSObject.Properties.Name -contains "displayName") { $tool.displayName } else { $tool.name }
            WinAvailable = if ($tool.PSObject.Properties.Name -contains "winAvailable") { $tool.winAvailable -eq $true } else { $false }
            WslAvailable = if ($tool.PSObject.Properties.Name -contains "wslAvailable") { $tool.wslAvailable -eq $true } else { $false }
            WinInstall = if ($tool.PSObject.Properties.Name -contains "winInstall") { $tool.winInstall } else { $null }
            WslInstall = if ($tool.PSObject.Properties.Name -contains "wslInstall") { $tool.wslInstall } else { $null }
        }
    }

    return $tools
}

function Start-BackgroundDetection {
    param($configPath)
    
    # 如果已有后台Job在运行，不重复启动
    if ($script:bgDetectionJob -and $script:bgDetectionJob.State -eq 'Running') {
        return
    }
    
    # 清理已完成的Job
    if ($script:bgDetectionJob) {
        Remove-Job $script:bgDetectionJob -ErrorAction SilentlyContinue
    }
    
    # 启动后台检测Job
    $script:bgDetectionJob = Start-Job -ScriptBlock {
        param($configPath)
        
        # 加载配置
        $config = Get-Content $configPath -Encoding UTF8 | ConvertFrom-Json
        
        # 批量检测 WSL 工具
        $wslTools = @($config.tools | Where-Object { $_.wslInstall } | ForEach-Object { $_.name })
        $wslAvailable = @{}
        if ($wslTools.Count -gt 0) {
            $toolListInline = $wslTools -join ' '
            $checkScript = "for t in $toolListInline; do if command -v `$t >/dev/null 2>&1; then echo `$t; fi; done"
            try {
                $result = wsl.exe -e bash -ic $checkScript 2>$null
                if ($result) {
                    $result -split "`n" | Where-Object { $_ -and $_.Trim() } | ForEach-Object {
                        $wslAvailable[$_.Trim()] = $true
                    }
                }
            } catch {}
        }
        
        # 批量检测 Windows 工具
        $winAvailable = @{}
        $winTools = @($config.tools | Where-Object { $_.winInstall })
        foreach ($tool in $winTools) {
            try {
                $winAvailable[$tool.name] = $null -ne (Get-Command $tool.name -ErrorAction SilentlyContinue)
            } catch {
                $winAvailable[$tool.name] = $false
            }
        }
        
        # 更新配置
        for ($i = 0; $i -lt $config.tools.Count; $i++) {
            $tool = $config.tools[$i]
            $config.tools[$i] | Add-Member -NotePropertyName "winAvailable" -NotePropertyValue ($winAvailable[$tool.name] -eq $true) -Force
            $config.tools[$i] | Add-Member -NotePropertyName "wslAvailable" -NotePropertyValue ($wslAvailable[$tool.name] -eq $true) -Force
        }
        
        # 原子写入配置文件
        $tempPath = "$configPath.tmp"
        $backupPath = "$configPath.bak"
        
        try {
            $config | ConvertTo-Json -Depth 10 | Set-Content $tempPath -Encoding UTF8
            if (Test-Path $configPath) {
                Copy-Item $configPath $backupPath -Force -ErrorAction SilentlyContinue
            }
            Move-Item -Path $tempPath -Destination $configPath -Force
            if (Test-Path $backupPath) {
                Remove-Item $backupPath -Force -ErrorAction SilentlyContinue
            }
        } catch {
            if (Test-Path $backupPath) {
                Move-Item -Path $backupPath -Destination $configPath -Force -ErrorAction SilentlyContinue
            }
            if (Test-Path $tempPath) {
                Remove-Item $tempPath -Force -ErrorAction SilentlyContinue
            }
        }
    } -ArgumentList $configPath
}

function Invoke-ToolDetection {
    param($config)

    # 防御性检查
    if (-not $config -or -not $config.tools) {
        return @()
    }

    # 批量检测 WSL 工具 (单次 WSL 启动 + 交互式 shell)
    $wslTools = @($config.tools | Where-Object { $_.wslInstall } | ForEach-Object { $_.name })
    $wslAvailable = @{}
    if ($wslTools.Count -gt 0) {
        $toolListInline = $wslTools -join ' '
        $checkScript = "for t in $toolListInline; do if command -v `$t >/dev/null 2>&1; then echo `$t; fi; done"
        try {
            $result = wsl.exe -e bash -ic $checkScript 2>$null
            if ($result) {
                $result -split "`n" | Where-Object { $_ -and $_.Trim() } | ForEach-Object {
                    $wslAvailable[$_.Trim()] = $true
                }
            }
        } catch {
            # WSL 不可用，忽略错误
        }
    }

    # 批量检测 Windows 工具（Get-Command 在 PowerShell 中更快）
    $winAvailable = @{}
    $winTools = @($config.tools | Where-Object { $_.winInstall })

    foreach ($tool in $winTools) {
        try {
            # Get-Command 是 PowerShell 内置命令，比 where.exe 快约 4 倍
            $winAvailable[$tool.name] = $null -ne (Get-Command $tool.name -ErrorAction SilentlyContinue)
        } catch {
            $winAvailable[$tool.name] = $false
        }
    }

    # 构建结果
    $tools = @()
    foreach ($tool in $config.tools) {
        $tools += [PSCustomObject]@{
            Name = $tool.name
            DisplayName = if ($tool.PSObject.Properties.Name -contains "displayName") { $tool.displayName } else { $tool.name }
            WinAvailable = $winAvailable[$tool.name] -eq $true
            WslAvailable = $wslAvailable[$tool.name] -eq $true
            WinInstall = if ($tool.PSObject.Properties.Name -contains "winInstall") { $tool.winInstall } else { $null }
            WslInstall = if ($tool.PSObject.Properties.Name -contains "wslInstall") { $tool.wslInstall } else { $null }
        }
    }

    return $tools
}

function Update-ToolCacheInConfig {
    param($config, $tools)

    if (-not $config -or -not $config.tools) {
        return
    }

    # 直接更新内存中的config对象属性
    for ($i = 0; $i -lt $config.tools.Count; $i++) {
        $tool = $config.tools[$i]
        $detected = $tools | Where-Object { $_.Name -eq $tool.name } | Select-Object -First 1
        
        if ($detected) {
            # 使用Add-Member强制更新属性值
            $config.tools[$i] | Add-Member -NotePropertyName "winAvailable" -NotePropertyValue $detected.WinAvailable -Force
            $config.tools[$i] | Add-Member -NotePropertyName "wslAvailable" -NotePropertyValue $detected.WslAvailable -Force
        } else {
            $config.tools[$i] | Add-Member -NotePropertyName "winAvailable" -NotePropertyValue $false -Force
            $config.tools[$i] | Add-Member -NotePropertyName "wslAvailable" -NotePropertyValue $false -Force
        }
    }

    # 持久化到磁盘
    Save-Config -config $config
}



# ==========================================
# 安装工具
# ==========================================
function Install-Tool {
    param($config)

    # 获取未安装的工具（强制刷新检测）
    $allTools = Invoke-ToolDetection -config $config
    $uninstalledTools = @()

    foreach ($tool in $allTools) {
        $hasInstall = $false
        if (-not $tool.WslAvailable -and $tool.WslInstall) {
            $uninstalledTools += [PSCustomObject]@{
                Name = "[WSL] $($tool.DisplayName)"
                Tool = $tool.Name
                Env = "wsl"
                Command = $tool.WslInstall
            }
            $hasInstall = $true
        }
        if (-not $tool.WinAvailable -and $tool.WinInstall) {
            $uninstalledTools += [PSCustomObject]@{
                Name = "[Win] $($tool.DisplayName)"
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

    # 强制刷新配置文件中的工具状态
    $config = Load-Config
    $newTools = Invoke-ToolDetection -config $config
    Update-ToolCacheInConfig -config $config -tools $newTools

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

# ==========================================
# 树状结构辅助函数
# ==========================================
function Get-FlattenedItems {
    param($items, $parentPath = @(), $level = 0)
    
    $result = @()
    foreach ($item in $items) {
        $result += [PSCustomObject]@{
            Item = $item
            Level = $level
            ParentPath = $parentPath
            IsFolder = ($item.type -eq "folder")
        }
        
        if ($item.type -eq "folder" -and $item.children) {
            $newPath = $parentPath + @($item.name)
            $result += Get-FlattenedItems -items $item.children -parentPath $newPath -level ($level + 1)
        }
    }
    return $result
}

function Get-ItemsAtPath {
    param($projects, [array]$path)
    
    $current = $projects
    foreach ($segment in $path) {
        $folder = $current | Where-Object { $_.type -eq "folder" -and $_.name -eq ([string]$segment) }
        if ($folder) {
            $current = $folder.children
            if ($null -eq $current) {
                $current = @()
            }
        } else {
            return , @()
        }
    }
    # 强制返回数组，使用逗号操作符防止解包
    return , @($current)
}

function Add-ItemToPath {
    param($projects, [array]$path, $item)
    
    if ($null -eq $projects) {
        $projects = @()
    }
    
    if ($path.Count -eq 0) {
        $result = [System.Collections.ArrayList]::new()
        foreach ($p in $projects) {
            [void]$result.Add($p)
        }
        [void]$result.Add($item)
        return $result
    }
    
    $result = [System.Collections.ArrayList]::new()
    $targetSegment = [string]$path[0]
    
    foreach ($proj in $projects) {
        if ($proj.type -eq "folder" -and $proj.name -eq $targetSegment) {
            $remainingPath = if ($path.Count -gt 1) { , $path[1..($path.Count-1)] } else { @() }
            $currentChildren = if ($proj.children) { $proj.children } else { @() }
            $newChildren = Add-ItemToPath -projects $currentChildren -path $remainingPath -item $item
            
            $newFolder = @{
                type = "folder"
                name = $proj.name
                children = $newChildren
            }
            [void]$result.Add($newFolder)
        } else {
            [void]$result.Add($proj)
        }
    }
    return $result
}

function Remove-ItemFromPath {
    param($projects, [array]$path, $itemName)
    
    if ($null -eq $projects) {
        return @()
    }
    
    if ($path.Count -eq 0) {
        $result = [System.Collections.ArrayList]::new()
        foreach ($p in $projects) {
            if ($p.name -ne $itemName) {
                [void]$result.Add($p)
            }
        }
        return $result
    }
    
    $result = [System.Collections.ArrayList]::new()
    $targetSegment = [string]$path[0]
    
    foreach ($proj in $projects) {
        if ($proj.type -eq "folder" -and $proj.name -eq $targetSegment) {
            $remainingPath = if ($path.Count -gt 1) { , $path[1..($path.Count-1)] } else { @() }
            $currentChildren = if ($proj.children) { $proj.children } else { @() }
            $newChildren = Remove-ItemFromPath -projects $currentChildren -path $remainingPath -itemName $itemName
            
            $newFolder = @{
                type = "folder"
                name = $proj.name
                children = $newChildren
            }
            [void]$result.Add($newFolder)
        } else {
            [void]$result.Add($proj)
        }
    }
    return $result
}

function Get-ItemCountRecursive {
    param($item)
    
    if ($item.type -ne "folder") {
        return 1
    }
    
    $count = 0
    if ($item.children) {
        foreach ($child in $item.children) {
            $count += Get-ItemCountRecursive -item $child
        }
    }
    return $count
}

function Add-NewProject {
    param($config, $currentPath = @())
    
    Clear-Host
    Write-Host "`n  Add New Item" -ForegroundColor Cyan
    Write-Host ("  " + "=" * 60) -ForegroundColor DarkGray
    Write-Host ""
    
    # 选择类型
    $types = @(
        [PSCustomObject]@{ Name = "📄 Project"; Type = "project" }
        [PSCustomObject]@{ Name = "📁 Folder"; Type = "folder" }
    )
    
    $typeResult = Get-UserSelection -items $types -title "Select Type" -allowBack $true
    if ($typeResult.Back) {
        return $false
    }
    
    $itemType = $types[$typeResult.Index].Type
    
    Clear-Host
    Write-Host "`n  Add New $($itemType.ToUpper())" -ForegroundColor Cyan
    Write-Host ("  " + "=" * 60) -ForegroundColor DarkGray
    Write-Host ""
    
    # 输入名称
    $itemName = $null
    while ($null -eq $itemName) {
        $itemName = Read-InputWithPlaceholder -Prompt "Name" -Placeholder "" -Required $true
        
        if ([string]::IsNullOrWhiteSpace($itemName)) {
            Write-Host "  Name is required!" -ForegroundColor Red
            continue
        }
        
        # 检查当前层级是否重复
        $currentItems = Get-ItemsAtPath -projects $config.projects -path $currentPath
        $exists = $currentItems | Where-Object { $_.name -eq $itemName }
        if ($exists) {
            Write-Host "  Name '$itemName' already exists in current location!" -ForegroundColor Red
            $itemName = $null
        }
    }
    
    if ($itemType -eq "folder") {
        # 文件夹只需要名称
        $newItem = @{
            type = "folder"
            name = $itemName
            children = @()
        }
        
        Write-Host ""
        Write-Host "  Folder Summary:" -ForegroundColor Cyan
        Write-Host "    Name: $itemName" -ForegroundColor White
        Write-Host ""
        Write-Host "  Add this folder? (Y/N): " -NoNewline -ForegroundColor Yellow
        $confirm = Read-Host
        
        if ($confirm -eq "Y" -or $confirm -eq "y") {
            $config.projects = Add-ItemToPath -projects $config.projects -path $currentPath -item $newItem
            Save-Config -config $config
            Write-Host "  Folder added successfully!" -ForegroundColor Green
            Start-Sleep -Seconds 1
            return $true
        }
        return $false
    }
    
    # 项目需要路径
    $currentDir = (Get-Location).Path
    $projectPath = $null
    while ($null -eq $projectPath) {
        $projectPath = Read-InputWithPlaceholder -Prompt "Project Path" -Placeholder "" -Required $false
        
        if ([string]::IsNullOrWhiteSpace($projectPath)) {
            $projectPath = $currentDir
        }
        
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
    
    # 输入环境变量
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
        type = "project"
        name = $itemName
        path = $projectPath
    }
    
    if ($envVars.Count -gt 0) {
        $newProject.env = $envVars
    }
    
    # 确认添加
    Write-Host ""
    Write-Host "  Project Summary:" -ForegroundColor Cyan
    Write-Host "    Name: $itemName" -ForegroundColor White
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
        $config.projects = Add-ItemToPath -projects $config.projects -path $currentPath -item $newProject
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

function Remove-ProjectOrFolder {
    param($config, $currentPath, $item)
    
    Clear-Host
    Write-Host "`n  Delete Confirmation" -ForegroundColor Red
    Write-Host ("  " + "=" * 60) -ForegroundColor DarkGray
    Write-Host ""
    
    $icon = if ($item.type -eq "folder") { "📁" } else { "📄" }
    Write-Host "  Item to delete: $icon $($item.name)" -ForegroundColor Yellow
    
    if ($item.type -eq "folder") {
        $count = Get-ItemCountRecursive -item $item
        Write-Host "  Contains: $count item(s)" -ForegroundColor Yellow
    } else {
        Write-Host "  Path: $($item.path)" -ForegroundColor DarkGray
    }
    
    Write-Host ""
    Write-Host "  ⚠️  WARNING: This action cannot be undone!" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Type the name to confirm deletion: " -NoNewline -ForegroundColor Cyan
    $confirmation = Read-Host
    
    if ($confirmation -eq $item.name) {
        $config.projects = Remove-ItemFromPath -projects $config.projects -path $currentPath -itemName $item.name
        Save-Config -config $config
        Write-Host "  Deleted successfully!" -ForegroundColor Green
        Start-Sleep -Seconds 1
        return $true
    } else {
        Write-Host "  Name mismatch. Deletion cancelled." -ForegroundColor Yellow
        Start-Sleep -Seconds 1
        return $false
    }
}

function Show-Menu {
    param($items, $title, [int]$selected = 0, [bool]$showTabHint = $false, [bool]$showAddProject = $false, [bool]$showDelete = $false, [bool]$showInstall = $false, $breadcrumb = @())
    
    $maxDisplay = [Math]::Min($items.Count, 15)
    $offset = [Math]::Max(0, $selected - $maxDisplay + 1)
    
    [Console]::CursorVisible = $false
    Clear-Host
    
    # 显示面包屑导航
    if ($breadcrumb.Count -gt 0) {
        Write-Host "`n  " -NoNewline
        Write-Host "Home" -ForegroundColor DarkGray -NoNewline
        foreach ($crumb in $breadcrumb) {
            Write-Host " > " -ForegroundColor DarkGray -NoNewline
            Write-Host $crumb -ForegroundColor Cyan -NoNewline
        }
        Write-Host ""
    }
    
    Write-Host "`n  $title" -ForegroundColor Cyan
    Write-Host ("  " + "=" * 60) -ForegroundColor DarkGray
    Write-Host ""
    
    for ($i = $offset; $i -lt [Math]::Min($offset + $maxDisplay, $items.Count); $i++) {
        $item = $items[$i]
        $prefix = if ($i -eq $selected) { "  >" } else { "   " }
        $color = if ($i -eq $selected) { "Green" } else { "White" }
        
        # 判断是否为文件夹或项目
        $isFolder = ($item.PSObject.Properties.Name -contains "type" -and $item.type -eq "folder")
        $icon = if ($isFolder) { "📁" } else { "📄" }
        
        Write-Host "$prefix $icon $($item.Name)" -ForegroundColor $color -NoNewline
        
        if ($item.PSObject.Properties.Name -contains "Path") {
            Write-Host " ($($item.Path))" -ForegroundColor DarkGray
        } elseif ($isFolder -and $item.children) {
            $count = $item.children.Count
            Write-Host " ($count item(s))" -ForegroundColor DarkGray
        } else {
            Write-Host ""
        }
    }
    
    Write-Host ""
    if ($showTabHint) {
        Write-Host "  [↑↓] Navigate  [Enter] New Window  [Ctrl+Enter] New Tab  [I] Install  [Esc] Back  [Q] Quit" -ForegroundColor DarkGray
    } elseif ($showInstall) {
        Write-Host "  [↑↓] Navigate  [Enter] Launch  [I] Install  [Esc] Back  [Q] Quit" -ForegroundColor DarkGray
    } elseif ($showAddProject) {
        $hint = "  [↑↓] Navigate  [Enter] Select  [N] New  [D] Delete"
        if ($breadcrumb.Count -gt 0) {
            $hint += "  [Esc] Back"
        }
        $hint += "  [Q] Quit"
        Write-Host $hint -ForegroundColor DarkGray
    } else {
        Write-Host "  [↑↓] Navigate  [Enter] Select  [Esc] Back  [Q] Quit" -ForegroundColor DarkGray
    }
}

function Get-UserSelection {
    param($items, $title, [bool]$showTabHint = $false, [bool]$allowBack = $false, [bool]$allowAddProject = $false, [bool]$allowDelete = $false, [bool]$showInstall = $false, $breadcrumb = @())
    
    $selected = 0
    
    while ($true) {
        Show-Menu -items $items -title $title -selected $selected -showTabHint $showTabHint -showAddProject $allowAddProject -showDelete $allowDelete -showInstall $showInstall -breadcrumb $breadcrumb
        
        $key = [Console]::ReadKey($true)
        
        # 检测 Ctrl+Enter
        if ($key.Modifiers -eq [ConsoleModifiers]::Control -and $key.Key -eq "Enter") {
            [Console]::CursorVisible = $true
            return @{Index = $selected; UseTab = $true; Back = $false; Install = $false; AddProject = $false; Delete = $false}
        }
        
        switch ($key.Key) {
            "UpArrow" { $selected = [Math]::Max(0, $selected - 1) }
            "DownArrow" { $selected = [Math]::Min($items.Count - 1, $selected + 1) }
            "Enter" { 
                [Console]::CursorVisible = $true
                return @{Index = $selected; UseTab = $false; Back = $false; Install = $false; AddProject = $false; Delete = $false}
            }
            "I" {
                if (-not $allowAddProject) {
                    [Console]::CursorVisible = $true
                    return @{Index = -1; UseTab = $false; Back = $false; Install = $true; AddProject = $false; Delete = $false}
                }
            }
            "N" {
                if ($allowAddProject) {
                    [Console]::CursorVisible = $true
                    return @{Index = -1; UseTab = $false; Back = $false; Install = $false; AddProject = $true; Delete = $false}
                }
            }
            "D" {
                if ($allowDelete) {
                    [Console]::CursorVisible = $true
                    return @{Index = $selected; UseTab = $false; Back = $false; Install = $false; AddProject = $false; Delete = $true}
                }
            }
            "Escape" {
                if ($allowBack -or $breadcrumb.Count -gt 0) {
                    [Console]::CursorVisible = $true
                    return @{Index = -1; UseTab = $false; Back = $true; Install = $false; AddProject = $false; Delete = $false}
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

    # 启动后台工具检测
    Start-BackgroundDetection -configPath $userConfigPath

    # 检测是否安装 Windows Terminal
    $hasWindowsTerminal = $null -ne (Get-Command "wt" -ErrorAction SilentlyContinue)

    $currentProject = $null
    $currentPath = @()  # 当前文件夹路径
    
    while ($true) {
        # 检查后台检测是否完成
        if ($script:bgDetectionJob -and $script:bgDetectionJob.State -eq 'Completed') {
            $config = Load-Config  # 重新加载配置
            Remove-Job $script:bgDetectionJob -ErrorAction SilentlyContinue
            $script:bgDetectionJob = $null
        }
        
        # 1. 选择项目（如果未选择或需要重新选择）
        if ($null -eq $currentProject) {
            $currentItems = Get-ItemsAtPath -projects $config.projects -path $currentPath
            
            # 如果当前位置为空，显示提示但允许新增
            if ($currentItems.Count -eq 0) {
                $breadcrumbTitle = if ($currentPath.Count -eq 0) { "Select Project" } else { "Select Project" }
                
                Clear-Host
                if ($currentPath.Count -gt 0) {
                    Write-Host "`n  " -NoNewline
                    Write-Host "Home" -ForegroundColor DarkGray -NoNewline
                    foreach ($crumb in $currentPath) {
                        Write-Host " > " -ForegroundColor DarkGray -NoNewline
                        Write-Host $crumb -ForegroundColor Cyan -NoNewline
                    }
                    Write-Host ""
                }
                Write-Host "`n  $breadcrumbTitle" -ForegroundColor Cyan
                Write-Host ("  " + "=" * 60) -ForegroundColor DarkGray
                Write-Host ""
                Write-Host "  (Empty folder)" -ForegroundColor DarkGray
                Write-Host ""
                
                $hint = "  [N] New"
                if ($currentPath.Count -gt 0) {
                    $hint += "  [Esc] Back"
                }
                $hint += "  [Q] Quit"
                Write-Host $hint -ForegroundColor DarkGray
                
                $key = [Console]::ReadKey($true)
                switch ($key.Key) {
                    "N" {
                        $added = Add-NewProject -config $config -currentPath $currentPath
                        if ($added) {
                            $config = Load-Config
                        }
                    }
                    "Escape" {
                        if ($currentPath.Count -gt 0) {
                            if ($currentPath.Count -eq 1) {
                                $currentPath = @()
                            } else {
                                $currentPath = $currentPath[0..($currentPath.Count - 2)]
                            }
                        }
                    }
                    "Q" { exit 0 }
                }
                continue
            }
            
            $breadcrumbTitle = if ($currentPath.Count -eq 0) { "Select Project" } else { "Select Project" }
            $result = Get-UserSelection -items $currentItems -title $breadcrumbTitle -allowAddProject $true -allowDelete $true -breadcrumb $currentPath
            
            # 处理新增
            if ($result.AddProject) {
                $added = Add-NewProject -config $config -currentPath $currentPath
                if ($added) {
                    $config = Load-Config
                }
                continue
            }
            
            # 处理删除
            if ($result.Delete) {
                $itemToDelete = $currentItems[$result.Index]
                $deleted = Remove-ProjectOrFolder -config $config -currentPath $currentPath -item $itemToDelete
                if ($deleted) {
                    $config = Load-Config
                }
                continue
            }
            
            # 处理返回上级
            if ($result.Back) {
                if ($currentPath.Count -gt 0) {
                    if ($currentPath.Count -eq 1) {
                        $currentPath = @()
                    } else {
                        $currentPath = $currentPath[0..($currentPath.Count - 2)]
                    }
                }
                continue
            }
            
            $selectedItem = $currentItems[$result.Index]
            
            # 如果是文件夹，进入文件夹
            if ($selectedItem.type -eq "folder") {
                $currentPath += @($selectedItem.name)
                continue
            }
            
            # 如果是项目，选中
            $currentProject = $selectedItem
        }

        # 2. 获取可用工具
        $tools = Get-AvailableTools -config $config
        $availableTools = @()

        foreach ($tool in $tools) {
            if ($tool.WslAvailable) {
                $availableTools += [PSCustomObject]@{
                    Name = "[WSL] $($tool.DisplayName)"
                    Tool = $tool.Name
                    Env = "wsl"
                }
            }
            if ($tool.WinAvailable) {
                $availableTools += [PSCustomObject]@{
                    Name = "[Win] $($tool.DisplayName)"
                    Tool = $tool.Name
                    Env = "win"
                }
            }
        }

        # 如果没有可用工具，进行前台检测
        if ($availableTools.Count -eq 0) {
            Write-Host "`nDetecting available tools..." -ForegroundColor Yellow

            # 执行强制检测
            $tools = Get-AvailableTools -config $config -Force
            $availableTools = @()

            foreach ($tool in $tools) {
                if ($tool.WslAvailable) {
                    $availableTools += [PSCustomObject]@{
                        Name = "[WSL] $($tool.DisplayName)"
                        Tool = $tool.Name
                        Env = "wsl"
                    }
                }
                if ($tool.WinAvailable) {
                    $availableTools += [PSCustomObject]@{
                        Name = "[Win] $($tool.DisplayName)"
                        Tool = $tool.Name
                        Env = "win"
                    }
                }
            }

            # 清除提示行
            Write-Host -NoNewline "`r" + (" " * 50) + "`r"

            # 检测后仍无可用工具
            if ($availableTools.Count -eq 0) {
                Write-Host "No tools available. Install tools first." -ForegroundColor Red
                Install-Tool -config $config
                continue
            }
        }

        # 3. 选择工具
        $result = Get-UserSelection -items $availableTools -title "Select AI Tool for $($currentProject.name)" -showTabHint $hasWindowsTerminal -showInstall $true -allowBack $true -breadcrumb @()

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

# 注册退出时清理后台Job
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action {
    if ($script:bgDetectionJob) {
        Stop-Job $script:bgDetectionJob -ErrorAction SilentlyContinue
        Remove-Job $script:bgDetectionJob -ErrorAction SilentlyContinue
    }
}

Start-InteractiveLauncher
