#!/bin/bash

# Portfolio Django Application Deployment Script for AWS EC2
# This script sets up the Django application on a fresh Ubuntu EC2 instance

set -e  # Exit on any errors


echo "Starting deployment of Portfolio Django Application..."

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
echo "Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git curl

# Create application directory
echo "Setting up application directory..."
sudo mkdir -p /var/www/portfolio
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn

# Copy application files (assuming you're running this from the project directory)
echo "Copying application files..."
sudo cp -r . /var/www/portfolio/
sudo chown -R www-data:www-data /var/www/portfolio

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
cd /var/www/portfolio
sudo -u www-data python3 -m venv venv
sudo -u www-data /var/www/portfolio/venv/bin/pip install --upgrade pip
sudo -u www-data /var/www/portfolio/venv/bin/pip install -r requirements.txt

# Set up Django
echo "Setting up Django application..."
sudo -u www-data /var/www/portfolio/venv/bin/python manage.py collectstatic --noinput
sudo -u www-data /var/www/portfolio/venv/bin/python manage.py migrate

# Create Django superuser (optional - you can skip this or modify as needed)
echo "Creating Django superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | sudo -u www-data /var/www/portfolio/venv/bin/python manage.py shell

# Set up systemd service
echo "Setting up systemd service..."
sudo cp /var/www/portfolio/portfolio.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable portfolio
sudo systemctl start portfolio

# Set up Nginx
echo "Setting up Nginx..."
sudo cp /var/www/portfolio/nginx_portfolio.conf /etc/nginx/sites-available/portfolio
sudo ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default  # Remove default site
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
sudo systemctl enable nginx

# Set up firewall (UFW)
echo "Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

# Create log rotation for application logs
echo "Setting up log rotation..."
sudo tee /etc/logrotate.d/portfolio > /dev/null <<EOF
/var/log/gunicorn/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload portfolio
    endscript
}
EOF

# Set proper permissions
echo "Setting file permissions..."
sudo chown -R www-data:www-data /var/www/portfolio
sudo chmod -R 755 /var/www/portfolio
sudo chmod -R 644 /var/www/portfolio/staticfiles
sudo chmod -R 755 /var/log/gunicorn
sudo chmod -R 755 /var/run/gunicorn

echo "Deployment completed successfully!"
echo ""
echo "Your Django application should now be running on:"
echo "http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo ""
echo "To check the status of your application:"
echo "sudo systemctl status portfolio"
echo "sudo systemctl status nginx"
echo ""
echo "To view logs:"
echo "sudo journalctl -u portfolio -f"
echo "sudo tail -f /var/log/nginx/access.log"
echo "sudo tail -f /var/log/nginx/error.log"
echo ""
echo "Admin panel: http://your-ip/admin/"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Remember to:"
echo "1. Update the domain name in the Nginx configuration"
echo "2. Set up SSL certificate for HTTPS"
echo "3. Change the default admin password"
echo "4. Configure proper SECRET_KEY and DEBUG settings for production"
