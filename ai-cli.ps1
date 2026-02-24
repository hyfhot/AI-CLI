Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

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
    [System.Windows.Forms.MessageBox]::Show("未找到环境变量 AI_PROJECTS！`n请按格式设置：Name1=Path1;Name2=Path2;", "缺少配置", 0, 16)
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
$form.Text = "AI 编程工作台"
$form.Size = New-Object System.Drawing.Size(520, 360) # 进一步增加高度以容纳新控件
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false

$fontBold = New-Object System.Drawing.Font("Microsoft YaHei", 10, [System.Drawing.FontStyle]::Bold)
$fontNormal = New-Object System.Drawing.Font("Microsoft YaHei", 9, [System.Drawing.FontStyle]::Regular)

# --- 新增：工具选择区域 ---
$lblTool = New-Object System.Windows.Forms.Label
$lblTool.Text = "AI 编程工具："
$lblTool.Location = New-Object System.Drawing.Point(15, 18)
$lblTool.AutoSize = $true
$lblTool.Font = $fontBold
$form.Controls.Add($lblTool)

$cmbTool = New-Object System.Windows.Forms.ComboBox
$cmbTool.Location = New-Object System.Drawing.Point(120, 16)
$cmbTool.Size = New-Object System.Drawing.Size(365, 25)
$cmbTool.Font = $fontNormal
$cmbTool.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDown 

# 将探测到的工具加入下拉菜单
foreach ($tool in $availableTools) {
    $cmbTool.Items.Add($tool) | Out-Null
}
if ($cmbTool.Items.Count -gt 0) {
    $cmbTool.SelectedIndex = 0
} else {
    $cmbTool.Text = "[WSL] kiro-cli" # 如果都没探测到，给个默认值
}
$form.Controls.Add($cmbTool)

# --- 原有：项目选择区域 ---
$lblProject = New-Object System.Windows.Forms.Label
$lblProject.Text = "选择目标项目："
$lblProject.Location = New-Object System.Drawing.Point(15, 60)
$lblProject.AutoSize = $true
$lblProject.Font = $fontBold
$form.Controls.Add($lblProject)

$listView = New-Object System.Windows.Forms.ListView
$listView.Location = New-Object System.Drawing.Point(15, 85)
$listView.Size = New-Object System.Drawing.Size(470, 160)
$listView.View = [System.Windows.Forms.View]::Details
$listView.FullRowSelect = $true
$listView.MultiSelect = $false
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
$btnOk.Text = "启动工作台"
$btnOk.Location = New-Object System.Drawing.Point(200, 265)
$btnOk.Size = New-Object System.Drawing.Size(100, 35)
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