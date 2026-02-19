<#
Interactive PowerShell helper to initialize a local git repository,
create an initial commit, and set a remote URL for pushing to GitHub.

Usage: open PowerShell in the repo root and run:
  ./scripts/git_setup.ps1

This script will NOT push automatically without confirmation.
#>

param()

Set-StrictMode -Version Latest

function Read-YesNo($prompt){
    $r = Read-Host "$prompt (y/n)"
    return $r -match '^[Yy]'
}

Write-Host "Git setup helper — will initialize repo and create first commit." -ForegroundColor Cyan

if (-not (Test-Path .git)){
    git init
    Write-Host "Initialized empty git repository." -ForegroundColor Green
} else {
    Write-Host "Repository already initialized." -ForegroundColor Yellow
}

git add .
git commit -m "chore: initial commit" -q 2>$null || Write-Host "No changes to commit or commit failed." -ForegroundColor Yellow

$remote = Read-Host "Enter remote URL (e.g. git@github.com:username/repo.git or https://github.com/username/repo.git). Leave empty to skip"
if ($remote){
    git remote add origin $remote 2>$null || git remote set-url origin $remote
    Write-Host "Remote set to: $remote" -ForegroundColor Green

    if (Read-YesNo "Push to remote 'origin' now and create branch 'main'? "){
        $branch = Read-Host "Enter branch name (default: main)"
        if (-not $branch) { $branch = 'main' }
        git branch -M $branch
        git push -u origin $branch
        Write-Host "Pushed to origin/$branch" -ForegroundColor Green
    } else {
        Write-Host "Skipping push. Run 'git push -u origin main' when ready." -ForegroundColor Yellow
    }
} else {
    Write-Host "No remote provided. You can add one later with: git remote add origin <url>" -ForegroundColor Yellow
}

Write-Host "Done." -ForegroundColor Cyan
