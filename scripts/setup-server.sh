#!/bin/bash

# Server setup script for Internal Sea Core deployment
# Run this script on your Ubuntu server to prepare it for deployment

set -e

echo "🚀 Setting up Ubuntu server for Internal Sea Core deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "📦 Installing required packages..."
sudo apt-get install -y \
    curl \
    wget \
    git \
    docker.io \
    docker-compose \
    nginx \
    certbot \
    python3-certbot-nginx \
    ufw \
    fail2ban

# Start and enable Docker
echo "🐳 Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
echo "👤 Adding current user to docker group..."
sudo usermod -aG docker $USER

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22

# Configure fail2ban
echo "🛡️ Configuring fail2ban..."
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# Create deployment directory
echo "📁 Creating deployment directory..."
DEPLOY_PATH="/opt/internal-sea-core"
sudo mkdir -p $DEPLOY_PATH
sudo chown $USER:$USER $DEPLOY_PATH

# Create SSL directory
echo "🔒 Creating SSL directory..."
sudo mkdir -p /etc/nginx/ssl
sudo chown $USER:$USER /etc/nginx/ssl

# Create nginx configuration directory
echo "🌐 Creating nginx configuration..."
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled

# Create application logs directory
echo "📝 Creating logs directory..."
sudo mkdir -p /var/log/internal-sea-core
sudo chown $USER:$USER /var/log/internal-sea-core

# Create backup directory
echo "💾 Creating backup directory..."
sudo mkdir -p /opt/backups/internal-sea-core
sudo chown $USER:$USER /opt/backups/internal-sea-core

# Configure system limits
echo "⚙️ Configuring system limits..."
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Configure Docker daemon
echo "🐳 Configuring Docker daemon..."
sudo tee /etc/docker/daemon.json > /dev/null <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

# Restart Docker
sudo systemctl restart docker

# Create deployment script
echo "📜 Creating deployment script..."
cat > $DEPLOY_PATH/deploy.sh << 'EOF'
#!/bin/bash

set -e

echo "🚀 Starting deployment..."

# Navigate to deployment directory
cd /opt/internal-sea-core

# Stop existing containers
docker-compose -f docker-compose.prod.yml down --remove-orphans

# Pull latest changes
git pull origin main

# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Run database migrations
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

# Check service status
docker-compose -f docker-compose.prod.yml ps

echo "✅ Deployment completed successfully!"
EOF

chmod +x $DEPLOY_PATH/deploy.sh

# Create backup script
echo "📜 Creating backup script..."
cat > $DEPLOY_PATH/backup.sh << 'EOF'
#!/bin/bash

set -e

BACKUP_DIR="/opt/backups/internal-sea-core"
DATE=$(date +%Y%m%d_%H%M%S)

echo "💾 Starting backup..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U user internal_sea_core > $BACKUP_DIR/db_backup_$DATE.sql

# Backup application files
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz --exclude=node_modules --exclude=__pycache__ .

# Keep only last 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "✅ Backup completed: $BACKUP_DIR"
EOF

chmod +x $DEPLOY_PATH/backup.sh

# Create monitoring script
echo "📜 Creating monitoring script..."
cat > $DEPLOY_PATH/monitor.sh << 'EOF'
#!/bin/bash

echo "📊 System Status:"
echo "=================="

# Docker containers status
echo "🐳 Docker Containers:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "💾 Disk Usage:"
df -h

echo ""
echo "🧠 Memory Usage:"
free -h

echo ""
echo "🔥 CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}'

echo ""
echo "🌐 Network Connections:"
netstat -tuln | grep -E ':(80|443|8000|3000)'
EOF

chmod +x $DEPLOY_PATH/monitor.sh

# Create systemd service for auto-restart
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/internal-sea-core.service > /dev/null <<EOF
[Unit]
Description=Internal Sea Core Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$DEPLOY_PATH
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
sudo systemctl enable internal-sea-core.service

# Create log rotation
echo "📝 Configuring log rotation..."
sudo tee /etc/logrotate.d/internal-sea-core > /dev/null <<EOF
/var/log/internal-sea-core/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
    postrotate
        systemctl reload internal-sea-core
    endscript
}
EOF

echo "✅ Server setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Clone your repository to $DEPLOY_PATH"
echo "2. Configure environment variables"
echo "3. Set up SSL certificates with certbot"
echo "4. Configure your domain in nginx"
echo "5. Run the deployment script: $DEPLOY_PATH/deploy.sh"
echo ""
echo "🔧 Useful commands:"
echo "- Monitor: $DEPLOY_PATH/monitor.sh"
echo "- Backup: $DEPLOY_PATH/backup.sh"
echo "- Deploy: $DEPLOY_PATH/deploy.sh"
echo "- View logs: docker-compose -f $DEPLOY_PATH/docker-compose.prod.yml logs -f" 