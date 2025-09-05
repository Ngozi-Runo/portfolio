# AWS EC2 Deployment Guide for Django Portfolio Website

This guide will walk you through deploying your Django portfolio website on AWS EC2.

## Prerequisites

1. **AWS Account** with EC2 access
2. **Domain name** (optional but recommended)
3. **SSH key pair** for EC2 access
4. **Local development** environment set up

## Step 1: Launch EC2 Instance

### 1.1 Create EC2 Instance

1. **Log in to AWS Console** and navigate to EC2
2. **Click "Launch Instance"**
3. **Choose AMI**: Ubuntu Server 20.04 LTS (Free Tier Eligible)
4. **Choose Instance Type**: t2.micro (Free Tier) or t3.small (recommended for production)
5. **Configure Instance**:
   - Number of instances: 1
   - Network: Default VPC
   - Subnet: Default
   - Auto-assign Public IP: Enable
6. **Add Storage**: 8-20 GB (depending on your needs)
7. **Add Tags**: 
   - Key: Name, Value: Portfolio-Website
8. **Configure Security Group**:
   - Create new security group: "portfolio-sg"
   - Add rules:
     - SSH (22): Your IP
     - HTTP (80): Anywhere (0.0.0.0/0)
     - HTTPS (443): Anywhere (0.0.0.0/0)
9. **Review and Launch**
10. **Select existing key pair** or create new one
11. **Launch Instance**

### 1.2 Connect to Instance

```bash
# Replace with your key file and instance IP
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip
```

## Step 2: Prepare Your Code

### 2.1 Create Project Archive

On your local machine:

```bash
# Navigate to your project directory
cd /home/ngozi/portfolio_project

# Create a tar archive (excluding unnecessary files)
tar -czf portfolio.tar.gz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='db.sqlite3' \
    .
```

### 2.2 Upload to EC2

```bash
# Upload the archive to your EC2 instance
scp -i "your-key.pem" portfolio.tar.gz ubuntu@your-ec2-public-ip:~/
```

## Step 3: Deploy on EC2

### 3.1 Extract and Prepare

```bash
# On EC2 instance
cd ~
tar -xzf portfolio.tar.gz
cd portfolio_project  # or whatever your extracted folder is named
```

### 3.2 Run Deployment Script

```bash
# Make the script executable and run it
chmod +x deploy.sh
sudo ./deploy.sh
```

The deployment script will automatically:
- Update system packages
- Install Python, Nginx, and other dependencies
- Set up the application in `/var/www/portfolio`
- Configure Gunicorn and Nginx
- Start all services

### 3.3 Verify Deployment

```bash
# Check if services are running
sudo systemctl status portfolio
sudo systemctl status nginx

# Check if the website is accessible
curl http://localhost
```

## Step 4: Configure Domain (Optional)

### 4.1 Point Domain to EC2

1. **Get your EC2 public IP**: Check AWS Console or run `curl http://169.254.169.254/latest/meta-data/public-ipv4`
2. **Update DNS records**:
   - A record: `@` → Your EC2 IP
   - A record: `www` → Your EC2 IP

### 4.2 Update Nginx Configuration

```bash
# Edit Nginx configuration
sudo nano /etc/nginx/sites-available/portfolio

# Replace 'your-domain.com' with your actual domain
# Save and exit

# Test and reload Nginx
sudo nginx -t
sudo systemctl reload nginx
```

## Step 5: Set Up SSL Certificate (Recommended)

### 5.1 Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 5.2 Obtain SSL Certificate

```bash
# Replace with your domain
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Follow the prompts to:
- Enter email address
- Agree to terms
- Choose whether to share email with EFF
- Select redirect option (recommended: redirect HTTP to HTTPS)

### 5.3 Test Auto-Renewal

```bash
sudo certbot renew --dry-run
```

## Step 6: Production Configuration

### 6.1 Environment Variables

```bash
# Create environment file
sudo nano /var/www/portfolio/.env

# Add production settings:
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-ec2-ip
```

### 6.2 Update Django Settings

```bash
# Edit settings to use environment variables
sudo nano /var/www/portfolio/portfolio/settings.py

# Ensure these lines are present:
import os
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```

### 6.3 Install python-dotenv

```bash
cd /var/www/portfolio
sudo -u www-data ./venv/bin/pip install python-dotenv
sudo systemctl restart portfolio
```

## Step 7: Monitoring and Maintenance

### 7.1 Set Up Log Monitoring

```bash
# View real-time application logs
sudo journalctl -u portfolio -f

# View Nginx access logs
sudo tail -f /var/log/nginx/access.log

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### 7.2 Set Up Automated Backups

```bash
# Create backup script
sudo nano /usr/local/bin/backup-portfolio.sh

# Add content:
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/backups"
mkdir -p $BACKUP_DIR

# Backup database
cp /var/www/portfolio/db.sqlite3 $BACKUP_DIR/db_$DATE.sqlite3

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C /var/www/portfolio media/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sqlite3" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

# Make executable
sudo chmod +x /usr/local/bin/backup-portfolio.sh

# Add to crontab for daily backups
sudo crontab -e
# Add line: 0 2 * * * /usr/local/bin/backup-portfolio.sh
```

## Step 8: Security Hardening

### 8.1 Update Security Group

1. **Go to EC2 Console** → Security Groups
2. **Edit inbound rules** for your security group:
   - SSH (22): Restrict to your IP only
   - HTTP (80): 0.0.0.0/0 (if using HTTP to HTTPS redirect)
   - HTTPS (443): 0.0.0.0/0

### 8.2 Set Up Fail2Ban

```bash
# Install fail2ban
sudo apt install fail2ban -y

# Configure for SSH and Nginx
sudo nano /etc/fail2ban/jail.local

# Add content:
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true

# Start and enable fail2ban
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

### 8.3 Regular Updates

```bash
# Create update script
sudo nano /usr/local/bin/update-system.sh

# Add content:
#!/bin/bash
apt update
apt upgrade -y
apt autoremove -y

# Make executable
sudo chmod +x /usr/local/bin/update-system.sh

# Schedule weekly updates
sudo crontab -e
# Add line: 0 3 * * 0 /usr/local/bin/update-system.sh
```

## Step 9: Performance Optimization

### 9.1 Enable Nginx Caching

```bash
# Edit Nginx configuration
sudo nano /etc/nginx/sites-available/portfolio

# Add caching configuration in server block:
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 9.2 Monitor Resources

```bash
# Install htop for monitoring
sudo apt install htop -y

# Check resource usage
htop
df -h
free -h
```

## Troubleshooting

### Common Issues

1. **Website not accessible**:
   ```bash
   # Check if services are running
   sudo systemctl status nginx
   sudo systemctl status portfolio
   
   # Check firewall
   sudo ufw status
   ```

2. **Static files not loading**:
   ```bash
   # Collect static files
   cd /var/www/portfolio
   sudo -u www-data ./venv/bin/python manage.py collectstatic --noinput
   
   # Restart services
   sudo systemctl restart portfolio
   sudo systemctl reload nginx
   ```

3. **SSL certificate issues**:
   ```bash
   # Check certificate status
   sudo certbot certificates
   
   # Renew if needed
   sudo certbot renew
   ```

4. **Application errors**:
   ```bash
   # Check application logs
   sudo journalctl -u portfolio -n 50
   
   # Check Django debug info (temporarily enable DEBUG=True)
   ```

### Getting Help

- **AWS Documentation**: https://docs.aws.amazon.com/ec2/
- **Django Documentation**: https://docs.djangoproject.com/
- **Nginx Documentation**: https://nginx.org/en/docs/
- **Let's Encrypt**: https://letsencrypt.org/docs/

## Cost Optimization

### Free Tier Usage

- **t2.micro instance**: 750 hours/month free
- **30 GB EBS storage**: Free
- **15 GB data transfer out**: Free

### Cost Monitoring

1. **Set up billing alerts** in AWS Console
2. **Use AWS Cost Explorer** to monitor usage
3. **Consider Reserved Instances** for long-term use

## Scaling Considerations

For higher traffic, consider:

1. **Larger instance types** (t3.small, t3.medium)
2. **Application Load Balancer** with multiple instances
3. **RDS database** instead of SQLite
4. **CloudFront CDN** for static files
5. **Auto Scaling Groups** for automatic scaling

---

**Congratulations!** Your Django portfolio website should now be live on AWS EC2. Remember to:

- Keep your system updated
- Monitor logs regularly
- Backup your data
- Renew SSL certificates (automatic with certbot)
- Update your application code as needed

Your website should be accessible at:
- **HTTP**: http://your-ec2-ip or http://your-domain.com
- **HTTPS**: https://your-domain.com (if SSL configured)
