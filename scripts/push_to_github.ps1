# Script auxiliar para enviar o repositório local ao GitHub
# Use este script no PowerShell a partir da raiz do projeto.
# Ele vai:
#  - inicializar git se necessário
#  - criar um commit com todas as alterações
#  - adicionar o remote que você informou
#  - dar push para a branch main
# Observação: o push pedirá autenticação (usuário/senha ou token) ou usará suas chaves SSH se configuradas.

param(
    [string]$RemoteUrl = 'https://github.com/Cavera360JM/Tela.git',
    [string]$CommitMessage = 'Atualização: Bloco de Notas Interativo - temas e CRUD listas'
)

Write-Host "Executando em: $(Get-Location)" -ForegroundColor Cyan

if (-not (Test-Path .git)) {
    Write-Host "Inicializando repositório Git local..." -ForegroundColor Yellow
    git init
} else {
    Write-Host "Repositório Git já inicializado." -ForegroundColor Green
}

Write-Host "Adicionando todos os arquivos..." -ForegroundColor Yellow
git add -A

Write-Host "Criando commit (se houver mudanças)..." -ForegroundColor Yellow
# commit apenas se mudanças existirem
$changes = git status --porcelain
if ($changes) {
    git commit -m "$CommitMessage"
} else {
    Write-Host "Nenhuma mudança a commitar." -ForegroundColor Green
}

# Define branch principal como main
Write-Host "Definindo branch principal 'main'..." -ForegroundColor Yellow
git branch -M main

# Adiciona remote (se já existir, pergunta se quer sobrescrever)
$existing = git remote get-url origin 2>$null
if ($existing) {
    Write-Host "Remote 'origin' já existe com URL: $existing" -ForegroundColor Yellow
    $answer = Read-Host "Deseja sobrescrever o remote 'origin' com $RemoteUrl ? (s/N)"
    if ($answer -match '^[sS]') {
        git remote remove origin
        git remote add origin $RemoteUrl
    } else {
        Write-Host "Mantendo remote existente." -ForegroundColor Green
    }
} else {
    git remote add origin $RemoteUrl
}

Write-Host "Fazendo push para origin/main (pode pedir autenticação)..." -ForegroundColor Yellow
try {
    git push -u origin main
    Write-Host "Push completo com sucesso." -ForegroundColor Green
} catch {
    Write-Host "Push falhou. Verifique suas credenciais, conexão e permissões do repositório." -ForegroundColor Red
}

Write-Host "Fim do script." -ForegroundColor Cyan
