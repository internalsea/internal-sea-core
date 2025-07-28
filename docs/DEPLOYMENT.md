# Deployment Guide

This guide covers the complete deployment process for Internal Sea Core, including server setup, CI/CD configuration, and production deployment.

## Prerequisites

- Ubuntu 20.04+ server
- Domain name pointing to your server
- GitHub repository with the project
- SSH access to the server

## 1. Server Setup

### 1.1 Initial Server Configuration

Run the server setup script on your Ubuntu server:

```bash
# Download and run the setup script
curl -fsSL https://raw.githubusercontent.com/your-org/internal-sea-core/main/scripts/setup-server.sh | bash
```

This script will:
- Update system packages
- Install Docker, Docker Compose, Nginx, and other required tools
- Configure firewall and security settings
- Create necessary directories and scripts
- Set up systemd service for auto-restart

### 1.2 Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y docker.io docker-compose

# Install Nginx and SSL tools
sudo apt-get install -y nginx certbot python3-certbot-nginx

# Install security tools
sudo apt-get install -y ufw fail2ban

# Start and enable services
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl start nginx
sudo systemctl enable nginx
```

## 2. GitHub Repository Setup

### 2.1 Required Secrets

Add the following secrets to your GitHub repository (Settings > Secrets and variables > Actions):

- `SONAR_TOKEN`: Your SonarCloud authentication token
- `DEPLOY_HOST`: Your server's IP address or domain
- `DEPLOY_USER`: SSH username for the server
- `DEPLOY_KEY`: Private SSH key for server access
- `DEPLOY_PATH`: Deployment directory on server (e.g., `/opt/internal-sea-core`)

### 2.2 SonarCloud Setup

1. Create a SonarCloud account and organization
2. Create a new project for your repository
3. Get your authentication token from SonarCloud
4. Update `sonar-project.properties` with your organization and project key

## 3. Environment Configuration

### 3.1 Backend Environment

Create `.env` file on the server:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@postgres:5432/internal_sea_core

# Security
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Configuration
REDIS_URL=redis://redis:6379

# Environment
ENVIRONMENT=production
DEBUG=false

# CORS
ALLOWED_HOSTS=["https://yourdomain.com","http://localhost:3000"]
```

### 3.2 Frontend Environment

Update the frontend environment variables in the Docker Compose file:

```yaml
environment:
  - REACT_APP_API_URL=https://yourdomain.com/api
```

## 4. SSL Certificate Setup

### 4.1 Using Certbot (Recommended)

```bash
# Stop nginx temporarily
sudo systemctl stop nginx

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Start nginx
sudo systemctl start nginx
```

### 4.2 Manual SSL Setup

If you have your own certificates:

```bash
# Copy certificates to nginx ssl directory
sudo cp your-cert.pem /etc/nginx/ssl/cert.pem
sudo cp your-key.pem /etc/nginx/ssl/key.pem
sudo chmod 600 /etc/nginx/ssl/key.pem
```

## 5. Deployment Process

### 5.1 Initial Deployment

1. Clone the repository to the server:
```bash
cd /opt
git clone https://github.com/your-org/internal-sea-core.git
cd internal-sea-core
```

2. Configure environment variables:
```bash
cp backend/env.example backend/.env
# Edit backend/.env with your production values
```

3. Run the deployment:
```bash
./deploy.sh
```

### 5.2 Automated Deployment

The GitHub Actions workflow will automatically:
1. Run tests for both backend and frontend
2. Perform SonarCloud code quality analysis
3. Deploy to the server if quality gates pass
4. Run database migrations
5. Perform health checks

## 6. Monitoring and Maintenance

### 6.1 Health Monitoring

```bash
# Check service status
./monitor.sh

# View application logs
docker-compose -f docker-compose.prod.yml logs -f

# Check specific service logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### 6.2 Backup

```bash
# Create backup
./backup.sh

# List backups
ls -la /opt/backups/internal-sea-core/
```

### 6.3 Updates

```bash
# Pull latest changes and redeploy
git pull origin main
./deploy.sh
```

## 7. Troubleshooting

### 7.1 Common Issues

**Docker containers not starting:**
```bash
# Check Docker logs
docker-compose -f docker-compose.prod.yml logs

# Check system resources
df -h
free -h
```

**Database connection issues:**
```bash
# Check PostgreSQL container
docker-compose -f docker-compose.prod.yml exec postgres psql -U user -d internal_sea_core

# Check database logs
docker-compose -f docker-compose.prod.yml logs postgres
```

**Nginx issues:**
```bash
# Check nginx configuration
sudo nginx -t

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

### 7.2 Performance Optimization

**Database optimization:**
```sql
-- Add indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_items_owner_id ON items(owner_id);
```

**Nginx optimization:**
```nginx
# Add to nginx.conf for better performance
client_max_body_size 10M;
client_body_buffer_size 128k;
```

## 8. Security Considerations

### 8.1 Firewall Configuration

```bash
# Check firewall status
sudo ufw status

# Allow only necessary ports
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

### 8.2 Regular Security Updates

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Update Docker images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### 8.3 SSL Certificate Renewal

```bash
# Set up automatic renewal
sudo crontab -e

# Add this line for automatic renewal
0 12 * * * /usr/bin/certbot renew --quiet
```

## 9. Scaling Considerations

### 9.1 Horizontal Scaling

For high-traffic applications, consider:
- Load balancer (HAProxy, Nginx)
- Multiple application instances
- Database clustering
- Redis clustering

### 9.2 Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Use CDN for static assets
- Implement caching strategies

## 10. Support and Maintenance

### 10.1 Regular Maintenance Tasks

- Weekly: Check logs and system resources
- Monthly: Update dependencies and security patches
- Quarterly: Review and update SSL certificates
- Annually: Review and update deployment procedures

### 10.2 Emergency Procedures

1. **Service down**: Check logs and restart services
2. **Database issues**: Restore from backup
3. **Security breach**: Isolate server and investigate
4. **Performance issues**: Scale resources or optimize code

For additional support, refer to the project documentation or contact the development team. 