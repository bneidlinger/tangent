# TANGNET Migration Guide

## 🚀 Quick Setup for GitHub Pages

To showcase your project professionally on GitHub:

### 1. Enable GitHub Pages
1. Go to your repository Settings
2. Navigate to Pages section
3. Set Source to "Deploy from a branch"
4. Select `/docs` folder from main branch
5. Save and wait a few minutes

Your site will be live at: `https://bneidlinger.github.io/tangent/`

### 2. Update Links in Documentation
Replace `yourusername` in these files:
- `/docs/index.html` - Multiple GitHub links
- `/README.md` - Badge links

### 3. Recommended File Moves

```bash
# Move overview docs to GitHub Pages
cp overview/*.html docs/
cp "set-up docs"/*.html docs/setup/

# Move architecture diagram
cp picluster.png docs/assets/images/

# Move mesh documentation
cp -r "mesh docs" docs/architecture/mesh/

# Move source code
mkdir -p src
mv tanchat src/
mv tanchat-node src/

# Archive old files
mkdir -p archive
mv oldtanchatfiles archive/
```

### 4. Update Git Remote (if needed)

```bash
# Check current remote
git remote -v

# Update if needed
git remote set-url origin https://github.com/bneidlinger/tangent.git
```

### 5. Commit and Push

```bash
git add .
git commit -m "Reorganize project structure for GitHub Pages"
git push origin main
```

## 📁 New Structure Benefits

1. **Professional GitHub presence** - Clean README with badges
2. **GitHub Pages ready** - Beautiful landing page at `/docs`
3. **Organized codebase** - Clear separation of concerns
4. **Easy navigation** - Logical folder structure
5. **Scalable** - Ready for 100-node expansion

## 🎯 Next Steps

1. **Add CI/CD** - GitHub Actions for automated testing
2. **Documentation** - Convert HTML docs to Markdown for easier editing
3. **Docker Support** - Containerize the chat API
4. **Monitoring** - Add Prometheus/Grafana stack
5. **API Documentation** - Add OpenAPI/Swagger specs

## 🔗 Quick Links

After setup, you'll have:
- **Main Site**: `https://bneidlinger.github.io/tangent/`
- **Setup Guide**: `https://bneidlinger.github.io/tangent/setup/guide.html`
- **API Docs**: `https://bneidlinger.github.io/tangent/api/`
- **GitHub Repo**: `https://github.com/bneidlinger/tangent`