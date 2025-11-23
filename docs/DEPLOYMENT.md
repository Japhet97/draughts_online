# Deployment Guide

## Production Deployment Checklist

### 1. Environment Configuration

Create `.env` file with production values:

```env
# Database - Use production PostgreSQL
DATABASE_URL=postgresql://prod_user:strong_password@db-host:5432/draughts_prod

# Redis - Use production Redis
REDIS_URL=redis://redis-host:6379/0

# Security - Generate strong secret key
SECRET_KEY=use-openssl-rand-hex-32-to-generate-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# PayChangu - Production credentials
PAYCHANGU_API_KEY=your_production_api_key
PAYCHANGU_SECRET_KEY=your_production_secret_key
PAYCHANGU_CALLBACK_URL=https://api.yourdomain.com/api/v1/payments/callback
PAYCHANGU_BASE_URL=https://api.paychangu.com/v1

# Application
APP_NAME=Draughts Online
DEBUG=false
COMMISSION_RATE=0.10
MIN_BET_AMOUNT=100.00
MAX_BET_AMOUNT=100000.00

# CORS - Specify your frontend domains
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://app.yourdomain.com
```

### 2. Database Setup

```bash
# Create production database
createdb draughts_prod

# Run migrations (if using Alembic)
alembic upgrade head

# Or create tables directly
python -c "from app.db.database import engine, Base; from app.models.models import *; Base.metadata.create_all(bind=engine)"
```

### 3. Docker Deployment (Recommended)

**Production docker-compose.yml:**

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
    networks:
      - backend

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: always
    networks:
      - backend

  api:
    build: .
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
      - PAYCHANGU_API_KEY=${PAYCHANGU_API_KEY}
      - PAYCHANGU_SECRET_KEY=${PAYCHANGU_SECRET_KEY}
    depends_on:
      - db
      - redis
    restart: always
    networks:
      - backend
      - frontend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: always
    networks:
      - frontend

volumes:
  postgres_data:
  redis_data:

networks:
  backend:
  frontend:
```

### 4. Nginx Configuration

**nginx.conf:**

```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;

        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket support
        location /ws {
            proxy_pass http://api;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### 5. SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (add to crontab)
0 12 * * * /usr/bin/certbot renew --quiet
```

### 6. Deploy Commands

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build api
```

### 7. Database Backups

**Backup script (backup.sh):**

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="draughts_prod"

# Backup database
docker-compose exec -T db pg_dump -U postgres $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

echo "Backup completed: db_$DATE.sql.gz"
```

**Add to crontab:**
```bash
0 2 * * * /path/to/backup.sh
```

### 8. Monitoring

**Install monitoring tools:**

```bash
# Prometheus + Grafana
docker-compose -f monitoring.yml up -d
```

**monitoring.yml:**
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus_data:
  grafana_data:
```

### 9. Security Hardening

1. **Firewall Configuration:**
```bash
# Allow only necessary ports
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

2. **Environment Variables:**
- Never commit `.env` to git
- Use secrets management (AWS Secrets Manager, HashiCorp Vault)

3. **Database Security:**
- Use strong passwords
- Restrict network access
- Regular security updates

4. **API Rate Limiting:**
Add to main.py:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### 10. PayChangu Production Setup

1. Switch to production API endpoint
2. Configure webhook URL in PayChangu dashboard
3. Test with small amounts first
4. Monitor transaction callbacks
5. Set up alerts for failed payments

### 11. CI/CD Pipeline (GitHub Actions)

**.github/workflows/deploy.yml:**

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/draughts
            git pull
            docker-compose down
            docker-compose up -d --build
```

### 12. Health Checks

Add monitoring endpoint checks:
```bash
# Add to monitoring system
curl https://api.yourdomain.com/health

# Expected response:
{"status": "healthy"}
```

### 13. Performance Optimization

1. **Database Indexing:**
```sql
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_games_status ON games(status);
CREATE INDEX idx_transactions_user ON transactions(user_id);
```

2. **Redis Caching:**
- Cache user sessions
- Cache leaderboard data
- Cache active games

3. **CDN for Static Assets**

### 14. Scaling Strategy

**Horizontal Scaling:**
```yaml
services:
  api:
    deploy:
      replicas: 3
    # ... rest of config
```

**Load Balancer:**
- Use Nginx or AWS ALB
- Session stickiness for WebSocket

### 15. Disaster Recovery

1. **Regular Backups:**
   - Database: Daily
   - Redis: Hourly snapshots
   - Application code: Git

2. **Recovery Plan:**
   ```bash
   # Restore database
   gunzip < backup.sql.gz | docker-compose exec -T db psql -U postgres draughts_prod
   
   # Restart services
   docker-compose restart
   ```

### 16. Monitoring & Alerts

Set up alerts for:
- API downtime
- Failed payments
- Database connection issues
- High error rates
- Low disk space

### 17. Documentation

Keep updated:
- API documentation
- Deployment procedures
- Troubleshooting guide
- Incident response plan

---

## Quick Production Deployment

```bash
# 1. Clone repository
git clone <repo-url>
cd Draughts_online/backend

# 2. Configure environment
cp .env.example .env
nano .env  # Edit with production values

# 3. Deploy with Docker
docker-compose -f docker-compose.prod.yml up -d --build

# 4. Check logs
docker-compose logs -f

# 5. Test API
curl https://yourdomain.com/health
```

## Post-Deployment Testing

1. Register test user
2. Deposit small amount
3. Play test game
4. Withdraw winnings
5. Check all endpoints
6. Monitor logs for errors

## Support

For production issues, check:
1. Application logs: `docker-compose logs api`
2. Database logs: `docker-compose logs db`
3. Nginx logs: `docker-compose logs nginx`
4. PayChangu dashboard for payment issues
