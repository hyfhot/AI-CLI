Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# ==========================================
# 参数解析
# ==========================================
param(
    [switch]$Uninstall
)

# 如果指定了 --uninstall 参数，执行卸载
if ($Uninstall) {
    $installDir = "$env:LOCALAPPDATA\AI-CLI"

    # 删除安装目录
    if (Test-Path $installDir) {
        Remove-Item -Recurse -Force $installDir
        Write-Host "已删除安装目录: $installDir" -ForegroundColor Green
    }

    # 删除桌面快捷方式
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "AI-CLI.lnk"
    if (Test-Path $shortcutPath) {
        Remove-Item -Force $shortcutPath
        Write-Host "已删除桌面快捷方式" -ForegroundColor Green
    }

    # 删除开始菜单快捷方式
    $startMenuPath = Join-Path ([Environment]::GetFolderPath("StartMenu")) "Programs"
    $startShortcutPath = Join-Path $startMenuPath "AI-CLI.lnk"
    if (Test-Path $startShortcutPath) {
        Remove-Item -Force $startShortcutPath
        Write-Host "已删除开始菜单快捷方式" -ForegroundColor Green
    }

    Write-Host "卸载完成！" -ForegroundColor Green
    exit 0
}

# ==========================================
# 全局变量
# ==========================================
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$configPath = Join-Path $scriptDir "tools-config.json"

# ==========================================
# 多语言支持
# ==========================================
$langDir = Join-Path $scriptDir "lang"

function Get-SystemLanguage {
    $culture = [System.Globalization.CultureInfo]::CurrentUICulture
    $name = $culture.Name
    if ($name.StartsWith("zh")) { return "zh-CN" }
    if ($name.StartsWith("ja")) { return "ja-JP" }
    if ($name.StartsWith("de")) { return "de-DE" }
    return "en-US"
}

function Load-Language {
    param([string]$langCode)
    $langFile = Join-Path $langDir "$langCode.ps1"
    if (Test-Path $langFile) {
        . $langFile
        return $lang
    }
    # Fallback to Chinese
    $fallback = Join-Path $langDir "zh-CN.ps1"
    if (Test-Path $fallback) {
        . $fallback
        return $lang
    }
    return $null
}

$currentLangCode = Get-SystemLanguage
$lang = Load-Language $currentLangCode
if ($null -eq $lang) {
    [System.Windows.Forms.MessageBox]::Show("Failed to load language files!", "Error", 0, 16)
    exit
}

# ==========================================
# 辅助函数：Windows路径转WSL路径
# ==========================================
function ConvertTo-WslPath {
    param([string]$WinPath)
    $linuxPath = $WinPath -replace '\\', '/'
    if ($linuxPath -match '^([a-zA-Z]):(.*)') {
        $drive = $Matches[1].ToLower()
        $linuxPath = "/mnt/$drive" + $Matches[2]
    }
    return $linuxPath
}

# ==========================================
# 工具配置加载
# ==========================================
function Load-ToolsConfig {
    if (Test-Path $configPath) {
        $content = Get-Content $configPath -Raw -Encoding UTF8
        return $content | ConvertFrom-Json
    }
    return $null
}

# ==========================================
# 检查工具是否已安装
# ==========================================
function Test-ToolInstalled {
    param([string]$checkCommand, [string]$envType)

    if ($envType -eq "Win") {
        $cmd = $checkCommand.Split(' ')[0]
        return $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
    } else {
        $cmd = $checkCommand.Split(' ')[0]
        $result = wsl.exe -e bash -lc "command -v $cmd" 2>$null
        return -not [string]::IsNullOrWhiteSpace($result)
    }
}

# ==========================================
# 安装工具
# ==========================================
function Install-Tool {
    param([PSCustomObject]$tool, [string]$envType)

    $installCmd = if ($envType -eq "Win") { $tool.winInstall } else { $tool.wslInstall }

    if ([string]::IsNullOrWhiteSpace($installCmd)) {
        return $false
    }

    try {
        if ($envType -eq "Win") {
            $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/k", $installCmd -Wait -PassThru
            return $process.ExitCode -eq 0
        } else {
            $result = wsl.exe -e bash -lc $installCmd 2>&1
            return $LASTEXITCODE -eq 0
        }
    } catch {
        return $false
    }
}

# ==========================================
# 显示工具安装对话框
# ==========================================
function Show-ToolInstallDialog {
    param($parentForm, $toolsConfig, $currentLang)

    $dialog = New-Object System.Windows.Forms.Form
    $dialog.Text = $currentLang["InstallTool"]
    $dialog.Size = New-Object System.Drawing.Size(550, 420)
    $dialog.StartPosition = "CenterParent"
    $dialog.FormBorderStyle = "FixedDialog"
    $dialog.MaximizeBox = $false

    $fontBold = New-Object System.Drawing.Font("Microsoft YaHei", 10, [System.Drawing.FontStyle]::Bold)
    $fontNormal = New-Object System.Drawing.Font("Microsoft YaHei", 9, [System.Drawing.FontStyle]::Regular)

    # 标签
    $lblTitle = New-Object System.Windows.Forms.Label
    $lblTitle.Text = $currentLang["InstallTool"]
    $lblTitle.Location = New-Object System.Drawing.Point(15, 15)
    $lblTitle.AutoSize = $true
    $lblTitle.Font = $fontBold
    $dialog.Controls.Add($lblTitle)

    # 环境选择
    $lblEnv = New-Object System.Windows.Forms.Label
    $lblEnv.Text = $currentLang["EnvLabel"]
    $lblEnv.Location = New-Object System.Drawing.Point(15, 50)
    $lblEnv.AutoSize = $true
    $dialog.Controls.Add($lblEnv)

    $cmbEnv = New-Object System.Windows.Forms.ComboBox
    $cmbEnv.Location = New-Object System.Drawing.Point(120, 47)
    $cmbEnv.Size = New-Object System.Drawing.Size(100, 25)
    $cmbEnv.Items.AddRange(@("Win", "WSL"))
    $cmbEnv.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDownList
    $cmbEnv.SelectedIndex = 0
    $dialog.Controls.Add($cmbEnv)

    # 使用 Panel + FlowLayoutPanel 来显示工具列表，每个工具一行
    $toolsPanel = New-Object System.Windows.Forms.Panel
    $toolsPanel.Location = New-Object System.Drawing.Point(15, 85)
    $toolsPanel.Size = New-Object System.Drawing.Size(505, 220)
    $toolsPanel.AutoScroll = $true
    $dialog.Controls.Add($toolsPanel)

    # 存储工具行的引用
    $toolRows = @{}

    # 函数：刷新工具列表
    function Refresh-ToolList {
        $toolsPanel.Controls.Clear()
        $script:toolRows = @{}

        $allTools = @()
        if ($toolsConfig -and $toolsConfig.tools) {
            $allTools += $toolsConfig.tools
        }

        $yPos = 0
        foreach ($tool in $allTools) {
            $envType = $cmbEnv.Text

            # 检查当前环境是否支持该工具
            $isSupported = $true
            if ($envType -eq "Win" -and $null -eq $tool.winInstall) {
                $isSupported = $false
            } elseif ($envType -eq "WSL" -and $null -eq $tool.wslInstall) {
                $isSupported = $false
            }

            $installed = $false
            if ($isSupported) {
                $installed = Test-ToolInstalled -checkCommand $tool.checkCommand -envType $envType
            }

            # 工具行面板
            $rowPanel = New-Object System.Windows.Forms.Panel
            $rowPanel.Location = New-Object System.Drawing.Point(0, $yPos)
            $rowPanel.Size = New-Object System.Drawing.Size(490, 40)
            $rowPanel.Tag = $tool

            # 工具名称
            $lblName = New-Object System.Windows.Forms.Label
            $lblName.Text = $tool.displayName
            $lblName.Location = New-Object System.Drawing.Point(10, 10)
            $lblName.Size = New-Object System.Drawing.Size(150, 20)
            $lblName.Font = $fontNormal
            $rowPanel.Controls.Add($lblName)

            # 状态
            $lblStatus = New-Object System.Windows.Forms.Label
            if (-not $isSupported) {
                $lblStatus.Text = $currentLang["NotSupported"]
                $lblStatus.ForeColor = [System.Drawing.Color]::Red
            } elseif ($installed) {
                $lblStatus.Text = $currentLang["Installed"]
                $lblStatus.ForeColor = [System.Drawing.Color]::Green
            } else {
                $lblStatus.Text = $currentLang["NotInstalled"]
                $lblStatus.ForeColor = [System.Drawing.Color]::Gray
            }
            $lblStatus.Location = New-Object System.Drawing.Point(170, 10)
            $lblStatus.Size = New-Object System.Drawing.Size(100, 20)
            $lblStatus.Font = $fontNormal
            $rowPanel.Controls.Add($lblStatus)

            # 安装按钮（仅支持且未安装时显示）
            if ($isSupported -and -not $installed) {
                $btnInstall = New-Object System.Windows.Forms.Button
                $btnInstall.Text = $currentLang["InstallTool"]
                $btnInstall.Location = New-Object System.Drawing.Point(280, 5)
                $btnInstall.Size = New-Object System.Drawing.Size(80, 28)
                $btnInstall.Font = $fontNormal
                $rowPanel.Controls.Add($btnInstall)

                # 安装按钮事件
                $btnInstall.Add_Click({
                    $toolObj = $this.Parent.Tag
                    $envType = $cmbEnv.Text

                    # 更新状态为安装中
                    $statusLabel = $this.Parent.Controls | Where-Object { $_.Name -eq "StatusLabel" }
                    if ($statusLabel) {
                        $statusLabel.Text = $currentLang["Installing"]
                        $statusLabel.ForeColor = [System.Drawing.Color]::Blue
                    }

                    # 执行安装
                    $result = Install-Tool -tool $toolObj -envType $envType

                    if ($result) {
                        $statusLabel.Text = $currentLang["InstallSuccess"]
                        $statusLabel.ForeColor = [System.Drawing.Color]::Green
                        $this.Visible = $false
                        [System.Windows.Forms.MessageBox]::Show($parentForm, $currentLang["InstallSuccess"], $currentLang["InstallResult"], 0, 64)
                    } else {
                        $statusLabel.Text = $currentLang["InstallFailed"]
                        $statusLabel.ForeColor = [System.Drawing.Color]::Red
                        [System.Windows.Forms.MessageBox]::Show($parentForm, $currentLang["InstallFailed"], $currentLang["InstallResult"], 0, 16)
                    }
                })
            }

            # URL 链接
            $lblUrl = New-Object System.Windows.Forms.Label
            $lblUrl.Text = $tool.url
            $lblUrl.Location = New-Object System.Drawing.Point(370, 10)
            $lblUrl.Size = New-Object System.Drawing.Size(120, 20)
            $lblUrl.ForeColor = [System.Drawing.Color]::Blue
            $lblUrl.Font = $fontNormal
            $lblUrl.Cursor = [System.Windows.Forms.Cursors]::Hand
            $lblUrl.Name = "UrlLabel"

            # 点击打开URL
            $lblUrl.Add_Click({
                if ($this.Text) {
                    Start-Process $this.Text
                }
            })
            $rowPanel.Controls.Add($lblUrl)

            $toolsPanel.Controls.Add($rowPanel)
            $yPos += 45
        }
    }

    # 初始加载工具列表
    Refresh-ToolList

    # 添加自定义工具按钮
    $btnAddCustom = New-Object System.Windows.Forms.Button
    $btnAddCustom.Text = $currentLang["AddCustom"]
    $btnAddCustom.Location = New-Object System.Drawing.Point(15, 320)
    $btnAddCustom.Size = New-Object System.Drawing.Size(140, 35)
    $btnAddCustom.Font = $fontNormal
    $dialog.Controls.Add($btnAddCustom)

    # 添加自定义工具事件
    $btnAddCustom.Add_Click({
        $customDialog = New-Object System.Windows.Forms.Form
        $customDialog.Text = $currentLang["AddCustom"]
        $customDialog.Size = New-Object System.Drawing.Size(400, 250)
        $customDialog.StartPosition = "CenterParent"
        $customDialog.FormBorderStyle = "FixedDialog"

        $lblName = New-Object System.Windows.Forms.Label
        $lblName.Text = $currentLang["ToolName"]
        $lblName.Location = New-Object System.Drawing.Point(15, 20)
        $lblName.AutoSize = $true
        $customDialog.Controls.Add($lblName)

        $txtName = New-Object System.Windows.Forms.TextBox
        $txtName.Location = New-Object System.Drawing.Point(15, 45)
        $txtName.Size = New-Object System.Drawing.Size(350, 25)
        $customDialog.Controls.Add($txtName)

        $lblInstall = New-Object System.Windows.Forms.Label
        $lblInstall.Text = $currentLang["InstallCmd"]
        $lblInstall.Location = New-Object System.Drawing.Point(15, 80)
        $lblInstall.AutoSize = $true
        $customDialog.Controls.Add($lblInstall)

        $txtInstall = New-Object System.Windows.Forms.TextBox
        $txtInstall.Location = New-Object System.Drawing.Point(15, 105)
        $txtInstall.Size = New-Object System.Drawing.Size(350, 25)
        $customDialog.Controls.Add($txtInstall)

        $lblCheck = New-Object System.Windows.Forms.Label
        $lblCheck.Text = $currentLang["CheckCmd"]
        $lblCheck.Location = New-Object System.Drawing.Point(15, 140)
        $lblCheck.AutoSize = $true
        $customDialog.Controls.Add($lblCheck)

        $txtCheck = New-Object System.Windows.Forms.TextBox
        $txtCheck.Location = New-Object System.Drawing.Point(15, 165)
        $txtCheck.Size = New-Object System.Drawing.Size(350, 25)
        $customDialog.Controls.Add($txtCheck)

        $btnOk = New-Object System.Windows.Forms.Button
        $btnOk.Text = $currentLang["Add"]
        $btnOk.Location = New-Object System.Drawing.Point(150, 180)
        $btnOk.Size = New-Object System.Drawing.Size(80, 30)
        $btnOk.DialogResult = [System.Windows.Forms.DialogResult]::OK
        $customDialog.Controls.Add($btnOk)

        if ($customDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            if ([string]::IsNullOrWhiteSpace($txtName.Text) -or [string]::IsNullOrWhiteSpace($txtInstall.Text)) {
                [System.Windows.Forms.MessageBox]::Show($dialog, $currentLang["RequiredFieldsError"], "Error", 0, 16)
                return
            }

            $newTool = [PSCustomObject]@{
                name = $txtName.Text
                displayName = $txtName.Text
                winInstall = $txtInstall.Text
                wslInstall = $txtInstall.Text
                checkCommand = if ($txtCheck.Text) { $txtCheck.Text } else { "$($txtName.Text) --version" }
                url = ""
            }

            # 添加到配置
            if ($toolsConfig -and $toolsConfig.tools) {
                $toolsConfig.tools += $newTool
            }

            # 刷新列表
            Refresh-ToolList
        }
    })

    # 关闭按钮
    $btnClose = New-Object System.Windows.Forms.Button
    $btnClose.Text = $currentLang["Close"]
    $btnClose.Location = New-Object System.Drawing.Point(435, 320)
    $btnClose.Size = New-Object System.Drawing.Size(85, 35)
    $btnClose.Font = $fontNormal
    $btnClose.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    $dialog.Controls.Add($btnClose)

    # 环境切换刷新列表
    $cmbEnv.Add_SelectedIndexChanged({
        Refresh-ToolList
    })

    $dialog.ShowDialog() | Out-Null
}

# ==========================================
# 1. 自动探测已安装的 AI 工具
# ==========================================
# 在这里配置你想自动探测的常见指令名
$toolsToCheck = @("kiro-cli", "claude", "kimi", "opencode", "gemini", "cursor", "code")
$availableTools = @()

# 1.1 探测 Windows 原生环境
foreach ($t in $toolsToCheck) {
    if (Get-Command $t -ErrorAction SilentlyContinue) {
        $availableTools += "[Win] $t"
    }
}

# 1.2 探测 WSL 环境 (合并为单次调用以加快启动速度)
$wslCheckScript = "for cmd in $($toolsToCheck -join ' '); do if command -v `$cmd >/dev/null 2>&1; then echo `$cmd; fi; done"
$wslOutput = wsl.exe -e bash -lc $wslCheckScript 2>$null
if ($wslOutput) {
    foreach ($t in $wslOutput) {
        if (-not [string]::IsNullOrWhiteSpace($t)) {
            $availableTools += "[WSL] $($t.Trim())"
        }
    }
}

# ==========================================
# 2. 读取项目环境变量
# ==========================================
$envString = [Environment]::GetEnvironmentVariable("AI_PROJECTS", "User")
if ([string]::IsNullOrWhiteSpace($envString)) {
    $envString = [Environment]::GetEnvironmentVariable("AI_PROJECTS", "Machine")
}

if ([string]::IsNullOrWhiteSpace($envString)) {
    [System.Windows.Forms.MessageBox]::Show($lang["EnvVarError"], $lang["ConfigError"], 0, 16)
    exit
}

$items = @()
foreach ($item in $envString.Split(';', [System.StringSplitOptions]::RemoveEmptyEntries)) {
    $parts = $item.Split('=', 2)
    if ($parts.Length -eq 2) {
        $items += [PSCustomObject]@{ Name = $parts[0].Trim(); Path = $parts[1].Trim() }
    }
}

# ==========================================
# 3. 构建 UI 界面 (跨环境升级版)
# ==========================================
$form = New-Object System.Windows.Forms.Form
$form.Text = $lang["AppTitle"]
$form.Size = New-Object System.Drawing.Size(520, 400)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false

$fontBold = New-Object System.Drawing.Font("Microsoft YaHei", 10, [System.Drawing.FontStyle]::Bold)
$fontNormal = New-Object System.Drawing.Font("Microsoft YaHei", 9, [System.Drawing.FontStyle]::Regular)

# --- 第1行：工具标签 ---
$lblTool = New-Object System.Windows.Forms.Label
$lblTool.Text = $lang["ToolLabel"]
$lblTool.Location = New-Object System.Drawing.Point(15, 20)
$lblTool.AutoSize = $true
$lblTool.Font = $fontBold
$form.Controls.Add($lblTool)

# --- 第2行：工具下拉框 + 管理按钮 ---
$cmbTool = New-Object System.Windows.Forms.ComboBox
$cmbTool.Location = New-Object System.Drawing.Point(15, 48)
$cmbTool.Size = New-Object System.Drawing.Size(400, 25)
$cmbTool.Font = $fontNormal
$cmbTool.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDown

# 将探测到的工具加入下拉菜单
foreach ($tool in $availableTools) {
    $cmbTool.Items.Add($tool) | Out-Null
}
if ($cmbTool.Items.Count -gt 0) {
    $cmbTool.SelectedIndex = 0
} else {
    $cmbTool.Text = $lang["DefaultTool"]
}
$form.Controls.Add($cmbTool)

# --- 管理按钮 (带图标) ---
$btnManage = New-Object System.Windows.Forms.Button
$btnManage.Location = New-Object System.Drawing.Point(420, 45)
$btnManage.Size = New-Object System.Drawing.Size(32, 30)
$btnManage.FlatStyle = [System.Windows.Forms.FlatStyle]::Flat
$btnManage.FlatAppearance.BorderSize = 0
# 使用齿轮符号 (Unicode)
$btnManage.Text = [char]0x2699
$btnManage.Font = New-Object System.Drawing.Font("Segoe UI Symbol", 14, [System.Drawing.FontStyle]::Regular)
$btnManage.TextAlign = [System.Drawing.ContentAlignment]::MiddleCenter

# 加载工具配置
$toolsConfig = Load-ToolsConfig

$btnManage.Add_Click({
    Show-ToolInstallDialog -parentForm $form -toolsConfig $toolsConfig -currentLang $lang
    # 刷新工具列表
    $script:availableTools = @()
    $cmbTool.Items.Clear()

    foreach ($t in $toolsToCheck) {
        if (Get-Command $t -ErrorAction SilentlyContinue) {
            $script:availableTools += "[Win] $t"
        }
    }

    $wslCheckScript = "for cmd in $($toolsToCheck -join ' '); do if command -v `$cmd >/dev/null 2>&1; then echo `$cmd; fi; done"
    $wslOutput = wsl.exe -e bash -lc $wslCheckScript 2>$null
    if ($wslOutput) {
        foreach ($t in $wslOutput) {
            if (-not [string]::IsNullOrWhiteSpace($t)) {
                $script:availableTools += "[WSL] $($t.Trim())"
            }
        }
    }

    foreach ($tool in $script:availableTools) {
        $cmbTool.Items.Add($tool) | Out-Null
    }
    if ($cmbTool.Items.Count -gt 0) {
        $cmbTool.SelectedIndex = 0
    }
})
$form.Controls.Add($btnManage)

# --- 项目选择区域 ---
$lblProject = New-Object System.Windows.Forms.Label
$lblProject.Text = $lang["ProjectLabel"]
$lblProject.Location = New-Object System.Drawing.Point(15, 85)
$lblProject.AutoSize = $true
$lblProject.Font = $fontBold
$form.Controls.Add($lblProject)

$listView = New-Object System.Windows.Forms.ListView
$listView.Location = New-Object System.Drawing.Point(15, 110)
$listView.Size = New-Object System.Drawing.Size(470, 150)
$listView.View = [System.Windows.Forms.View]::Details
$listView.FullRowSelect = $true
$listView.MultiSelect = $false
$listView.HideSelection = $false  # 保持选中高亮，即使失去焦点
$listView.HeaderStyle = [System.Windows.Forms.ColumnHeaderStyle]::None 

$imageList = New-Object System.Windows.Forms.ImageList
$imageList.ImageSize = New-Object System.Drawing.Size(1, 32)
$listView.SmallImageList = $imageList

$listView.Columns.Add("Name", 150) | Out-Null
$listView.Columns.Add("Path", 300) | Out-Null

foreach ($i in $items) {
    $lvi = New-Object System.Windows.Forms.ListViewItem($i.Name)
    $lvi.UseItemStyleForSubItems = $false
    $lvi.Font = $fontBold
    
    $sub = $lvi.SubItems.Add($i.Path)
    $sub.ForeColor = [System.Drawing.Color]::Gray
    $sub.Font = $fontNormal
    
    $lvi.Tag = $i.Path
    $listView.Items.Add($lvi)
}
$form.Controls.Add($listView)

$btnOk = New-Object System.Windows.Forms.Button
$btnOk.Text = $lang["LaunchBtn"]
$btnOk.Location = New-Object System.Drawing.Point(200, 280)
$btnOk.Size = New-Object System.Drawing.Size(120, 45)
$btnOk.Font = $fontBold
$btnOk.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $btnOk
$form.Controls.Add($btnOk)

$listView.add_DoubleClick({
    if ($listView.SelectedItems.Count -gt 0) {
        $form.DialogResult = [System.Windows.Forms.DialogResult]::OK
        $form.Close()
    }
})

if ($listView.Items.Count -gt 0) {
    $listView.Items[0].Selected = $true
}

# ==========================================
# 4. 显示 UI 并捕获结果
# ==========================================
$result = $form.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK -and $listView.SelectedItems.Count -gt 0) {
    $projectName = $listView.SelectedItems[0].Text
    $rawWinPath = $listView.SelectedItems[0].Tag
    $selectedToolText = $cmbTool.Text
    
    # 智能解析用户选择的工具和环境
    $env = "WSL" # 默认当作 WSL 处理
    $actualTool = $selectedToolText
    
    if ($selectedToolText -match "^\[Win\]\s*(.*)") {
        $env = "Win"
        $actualTool = $matches[1]
    } elseif ($selectedToolText -match "^\[WSL\]\s*(.*)") {
        $env = "WSL"
        $actualTool = $matches[1]
    }
    
    $titlePrefix = $actualTool.ToUpper()

    # ==========================================
    # 5. 动态分发执行 (Win vs WSL)
    # ==========================================
    if ($env -eq "WSL") {
        # 处理 WSL 环境
        $wslPath = ConvertTo-WslPath -WinPath $rawWinPath
        $wslExe = "C:\Windows\System32\wsl.exe"
        $wslArgs = "-e bash -ic `"echo -ne '\033]0;$titlePrefix $projectName\007'; cd '$wslPath'; $actualTool; exec bash`""
        Start-Process -FilePath $wslExe -ArgumentList $wslArgs
    } else {
        # 处理 Windows 原生环境
        # /k 参数表示执行完保留窗口，title 设置标题，cd /d 跨盘符切换路径
        $cmdArgs = "/k `"title $titlePrefix $projectName & cd /d `"$rawWinPath`" & $actualTool`""
        Start-Process -FilePath "cmd.exe" -ArgumentList $cmdArgs
    }
}