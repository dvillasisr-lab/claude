# Sussek directory audit (READ-ONLY)
# Every command here only reads (Get-*). Nothing is changed, blocked or deleted.
# Output: SussekDirectoryAudit.csv on the Desktop, one row per account, plus a summary on screen.
#
# One-time setup (PowerShell as the admin user):
#   Install-Module Microsoft.Graph -Scope CurrentUser
#   Install-Module ExchangeOnlineManagement -Scope CurrentUser

Connect-MgGraph -Scopes "User.Read.All", "Directory.Read.All", "AuditLog.Read.All" -NoWelcome
Connect-ExchangeOnline -ShowBanner:$false

# 1. Entra ID accounts
$base = "id,displayName,givenName,surname,mail,userPrincipalName,userType,accountEnabled,department,jobTitle,companyName,officeLocation,employeeId,employeeHireDate,createdDateTime,onPremisesSyncEnabled,assignedLicenses"
try {
    $users = Get-MgUser -All -Property "$base,signInActivity" -ErrorAction Stop
    $hasSignIn = $true
} catch {
    Write-Warning "Last sign-in is not available (needs Entra ID P1). Continuing without it."
    $users = Get-MgUser -All -Property $base
    $hasSignIn = $false
}
$byId = @{}
foreach ($u in $users) { $byId[$u.Id] = $u }

# 2. Managers
$mgrOf = @{}
foreach ($u in $users) {
    try { $mgrOf[$u.Id] = (Get-MgUserManager -UserId $u.Id -ErrorAction Stop).Id } catch { $mgrOf[$u.Id] = $null }
}

# 3. Exchange mailboxes (hidden from GAL, mailbox type, forwarding)
$mbx = @{}
Get-EXOMailbox -ResultSize Unlimited -Properties ExternalDirectoryObjectId, RecipientTypeDetails, PrimarySmtpAddress, HiddenFromAddressListsEnabled, ForwardingSmtpAddress, ForwardingAddress |
    ForEach-Object { $mbx[$_.ExternalDirectoryObjectId] = $_ }

# 4. One row per account
$cutoff = (Get-Date).AddDays(-90)
$rows = foreach ($u in $users) {
    $m = $mbx[$u.Id]
    $mgr = if ($mgrOf[$u.Id]) { $byId[$mgrOf[$u.Id]] } else { $null }
    $reports = @($mgrOf.Keys | Where-Object { $mgrOf[$_] -eq $u.Id })
    $activeReports = @($reports | Where-Object { $byId[$_].AccountEnabled })

    $ar = $null
    if ($m) { try { $ar = Get-MailboxAutoReplyConfiguration -Identity $m.PrimarySmtpAddress -ErrorAction Stop } catch {} }
    $arText = if ($ar -and $ar.AutoReplyState -ne "Disabled") { (($ar.InternalMessage -replace '<[^>]+>', ' ') -replace '\s+', ' ').Trim() } else { "" }
    if ($arText.Length -gt 300) { $arText = $arText.Substring(0, 300) }

    $last = if ($hasSignIn) { $u.SignInActivity.LastSignInDateTime } else { $null }
    $licenses = @($u.AssignedLicenses).Count
    $hidden = if ($m) { $m.HiddenFromAddressListsEnabled } else { $null }
    $type = if ($m) { "$($m.RecipientTypeDetails)" } else { "No mailbox" }

    # Flags: what is inconsistent on this account
    $flags = @()
    if ($u.AccountEnabled -and $hidden)                         { $flags += "Hidden from GAL but sign-in enabled" }
    if ($u.AccountEnabled -and $type -eq "SharedMailbox")       { $flags += "Shared mailbox but sign-in enabled" }
    if ($u.AccountEnabled -and $arText)                         { $flags += "Auto-reply on, sign-in enabled" }
    if ($u.AccountEnabled -and $hasSignIn -and (-not $last -or $last -lt $cutoff)) { $flags += "No sign-in in 90+ days" }
    if (-not $u.AccountEnabled -and $licenses -gt 0)            { $flags += "Blocked but still licensed (cost)" }
    if (-not $u.AccountEnabled -and $activeReports.Count -gt 0) { $flags += "Blocked but still has direct reports" }
    if ($u.AccountEnabled -and $mgr -and -not $mgr.AccountEnabled) { $flags += "Manager is blocked" }
    if ($u.AccountEnabled -and $u.UserType -eq "Member" -and $type -eq "UserMailbox" -and -not $mgr) { $flags += "No manager" }
    if ($u.AccountEnabled -and $type -eq "UserMailbox" -and -not $u.Department) { $flags += "No department" }
    if ($u.AccountEnabled -and $type -eq "UserMailbox" -and -not $u.JobTitle)   { $flags += "No job title" }
    if ($m -and ($m.ForwardingSmtpAddress -or $m.ForwardingAddress))            { $flags += "Mail forwarded" }

    [pscustomobject]@{
        DisplayName                   = $u.DisplayName
        Mail                          = $u.Mail
        UserPrincipalName             = $u.UserPrincipalName
        UserType                      = $u.UserType
        AccountEnabled                = $u.AccountEnabled
        LastSignIn                    = if ($hasSignIn) { $last } else { "n/a" }
        Created                       = $u.CreatedDateTime
        SyncedFromOnPremAD            = $u.OnPremisesSyncEnabled
        Licenses                      = $licenses
        MailboxType                   = $type
        HiddenFromAddressListsEnabled = $hidden
        ForwardingTo                  = if ($m) { "$($m.ForwardingSmtpAddress)$($m.ForwardingAddress)" } else { "" }
        AutoReplyState                = if ($ar) { $ar.AutoReplyState } else { "" }
        AutoReplyMessage              = $arText
        Department                    = $u.Department
        JobTitle                      = $u.JobTitle
        CompanyName                   = $u.CompanyName
        OfficeLocation                = $u.OfficeLocation
        EmployeeId                    = $u.EmployeeId
        HireDate                      = $u.EmployeeHireDate
        Manager                       = if ($mgr) { $mgr.DisplayName } else { "" }
        ManagerEnabled                = if ($mgr) { $mgr.AccountEnabled } else { "" }
        DirectReportsActive           = $activeReports.Count
        DirectReportsTotal            = $reports.Count
        Flags                         = $flags -join "; "
    }
}

$path = Join-Path ([Environment]::GetFolderPath("Desktop")) "SussekDirectoryAudit.csv"
$rows | Sort-Object DisplayName | Export-Csv $path -NoTypeInformation -Encoding UTF8

# 5. Summary on screen
Write-Host "`nAccounts: $($rows.Count)   Enabled: $(@($rows | ? AccountEnabled).Count)   Blocked: $(@($rows | ? { -not $_.AccountEnabled }).Count)`n"
Write-Host "Flags:"
$rows | ForEach-Object { $_.Flags -split "; " } | Where-Object { $_ } | Group-Object | Sort-Object Count -Descending |
    Format-Table @{n = "Flag"; e = { $_.Name } }, Count -AutoSize
Write-Host "Hidden from GAL, by mailbox type and AD sync (shows what hides accounts automatically):"
$rows | Where-Object { $_.HiddenFromAddressListsEnabled } | Group-Object MailboxType, SyncedFromOnPremAD, AccountEnabled |
    Format-Table @{n = "MailboxType, SyncedFromAD, AccountEnabled"; e = { $_.Name } }, Count -AutoSize
Write-Host "Saved: $path"
