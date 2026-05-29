# APMF — Azure VM Deployment
# Ruleaza o singura data pentru a crea infrastructura

$RG = "apmf-rg"
$VM = "apmf-vm"
$LOCATION = "germanywestcentral"   # cel mai aproape de Bucuresti

Write-Host "[1/4] Creare Resource Group..." -ForegroundColor Cyan
az group create --name $RG --location $LOCATION

Write-Host "[2/4] Creare VM Ubuntu (B1s ~8$/luna)..." -ForegroundColor Cyan
az vm create `
  --resource-group $RG `
  --name $VM `
  --image Ubuntu2204 `
  --size Standard_B1s `
  --admin-username azureuser `
  --generate-ssh-keys `
  --custom-data cloud-init.yml `
  --output table

Write-Host "[3/4] Deschidere porturi (80=dashboard, 1883=MQTT)..." -ForegroundColor Cyan
az vm open-port --resource-group $RG --name $VM --port 80   --priority 100
az vm open-port --resource-group $RG --name $VM --port 1883 --priority 101

Write-Host "[4/4] IP public VM..." -ForegroundColor Cyan
az vm show --resource-group $RG --name $VM --show-details --query publicIps -o tsv

Write-Host ""
Write-Host "VM gata! Pasii urmatori:" -ForegroundColor Green
Write-Host "  1. ssh azureuser@<IP>" -ForegroundColor Green
Write-Host "  2. cd /app && nano .env  (pune TELEGRAM_BOT_TOKEN si TELEGRAM_CHAT_ID)" -ForegroundColor Green
Write-Host "  3. docker compose -f docker-compose.prod.yml up -d --build" -ForegroundColor Green
Write-Host "  4. Dashboard: http://<IP>" -ForegroundColor Green
