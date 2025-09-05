# Portfolio Website - Django

A modern, responsive portfolio website built with Django and Bootstrap, designed to be deployed on AWS EC2.

## Features

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Modern UI**: Clean, professional design with smooth animations
- **Static File Optimization**: WhiteNoise for efficient static file serving
- **Production Ready**: Configured for deployment with Gunicorn and Nginx
- **SEO Friendly**: Proper meta tags and semantic HTML structure
- **Contact Form**: Interactive contact form with validation
- **Project Showcase**: Dedicated section for displaying projects
- **Skills Section**: Highlight your technical skills
- **Social Media Integration**: Links to GitHub, LinkedIn, and email

## Tech Stack

- **Backend**: Django 4.2.5
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Database**: SQLite (easily configurable for PostgreSQL)
- **Static Files**: WhiteNoise
- **Deployment**: AWS EC2, Ubuntu

## Project Structure

```
portfolio_project/
├── main/                   # Main Django app
│   ├── views.py           # View functions
│   ├── urls.py            # URL patterns
│   └── ...
├── portfolio/             # Django project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── ...
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── main/              # App-specific templates
├── static/                # Static files (CSS, JS, images)
│   └── css/
│       └── style.css      # Custom styles
├── requirements.txt       # Python dependencies
├── gunicorn.conf.py      # Gunicorn configuration
├── portfolio.service     # Systemd service file
├── nginx_portfolio.conf  # Nginx configuration
├── deploy.sh             # Deployment script
└── README.md             # This file
```

## Local Development

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd portfolio_project
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to view the website.

## Customization

### Personal Information

Edit the context dictionary in `main/views.py` to update:
- Your name and title
- About section
- Skills list
- Projects information
- Contact details

### Styling

- Modify `static/css/style.css` for custom styles
- Update color scheme by changing CSS variables in `:root`
- Replace images in `static/images/` with your own professional photos

### Images

The portfolio includes professional, open-source images from Unsplash:
- **Profile photo**: Professional headshot for the about section
- **Project images**: High-quality images representing different types of projects
- **Attribution**: All image credits are documented in `static/images/IMAGE_CREDITS.md`

To manage images:
```bash
# Optimize all images
python manage_images.py --optimize-all

# Optimize a specific image
python manage_images.py --optimize path/to/image.jpg

# Create responsive variants
python manage_images.py --create-variants path/to/image.jpg
```

### Content

- Update templates in `templates/main/` to modify page content
- Add new pages by creating views, URLs, and templates
- Customize the navigation in `templates/base.html`

## AWS EC2 Deployment

### Prerequisites

- AWS EC2 instance (Ubuntu 20.04 LTS recommended)
- SSH access to the instance
- Domain name (optional but recommended)

### Deployment Steps

1. **Connect to your EC2 instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. **Upload your project files**:
   ```bash
   # From your local machine
   scp -i your-key.pem -r portfolio_project ubuntu@your-ec2-ip:~/
   ```

3. **Run the deployment script**:
   ```bash
   cd portfolio_project
   sudo ./deploy.sh
   ```

The deployment script will:
- Install system dependencies
- Set up Python virtual environment
- Configure Gunicorn and Nginx
- Set up systemd service
- Configure firewall
- Set up log rotation

### Post-Deployment Configuration

1. **Update domain name** in `/etc/nginx/sites-available/portfolio`
2. **Set up SSL certificate** using Let's Encrypt:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```
3. **Update environment variables** for production
4. **Change default admin password**

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
# Edit .env with your actual values
```

Key variables to set:
- `SECRET_KEY`: Generate a new secret key for production
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Add your domain and IP addresses

## Monitoring and Maintenance

### Check Application Status

```bash
# Check Django application
sudo systemctl status portfolio

# Check Nginx
sudo systemctl status nginx

# View application logs
sudo journalctl -u portfolio -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Updating the Application

1. **Upload new code**:
   ```bash
   # Upload changes to the server
   scp -i your-key.pem -r updated-files ubuntu@your-ec2-ip:/var/www/portfolio/
   ```

2. **Restart services**:
   ```bash
   sudo systemctl restart portfolio
   sudo systemctl reload nginx
   ```

3. **Run migrations** (if database changes):
   ```bash
   cd /var/www/portfolio
   sudo -u www-data ./venv/bin/python manage.py migrate
   ```

4. **Collect static files** (if static files changed):
   ```bash
   sudo -u www-data ./venv/bin/python manage.py collectstatic --noinput
   ```

## Security Considerations

- Change default admin credentials
- Use environment variables for sensitive data
- Keep Django and dependencies updated
- Configure proper firewall rules
- Use HTTPS in production
- Regular security updates for the server
- Monitor application logs for suspicious activity

## Performance Optimization

- Enable Nginx gzip compression (included in config)
- Use CDN for static files (optional)
- Optimize images and assets
- Configure proper caching headers
- Monitor server resources and scale as needed

## Troubleshooting

### Common Issues

1. **Static files not loading**:
   - Run `python manage.py collectstatic`
   - Check Nginx configuration for static file paths

2. **Application not starting**:
   - Check logs: `sudo journalctl -u portfolio -f`
   - Verify virtual environment and dependencies

3. **Nginx errors**:
   - Test configuration: `sudo nginx -t`
   - Check error logs: `sudo tail -f /var/log/nginx/error.log`

4. **Permission issues**:
   - Ensure www-data owns application files
   - Check file permissions (755 for directories, 644 for files)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or issues:
- Create an issue in the repository
- Contact: otitimoses@gmail.com or otitimoses@outlook.com

---

**Note**: Remember to customize this README with your actual information, repository URLs, and contact details.
