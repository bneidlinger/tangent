# TANGNET Project Structure

## 📁 Directory Layout

```
tangnet/
├── docs/                    # All documentation (for GitHub Pages)
│   ├── index.html          # Main landing page
│   ├── setup/              # Setup and configuration guides
│   ├── api/                # API documentation
│   ├── hardware/           # Hardware specs and build guides
│   └── architecture/       # System architecture docs
│
├── src/                     # Source code
│   ├── tanchat/            # Chat API server
│   ├── tanchat-node/       # Node.js chat implementation
│   ├── mesh/               # Mesh network management
│   └── ui/                 # Web interfaces
│
├── scripts/                 # Utility scripts
│   ├── setup/              # Installation scripts
│   ├── deploy/             # Deployment automation
│   └── monitoring/         # System monitoring
│
├── config/                  # Configuration files
│   ├── mesh/               # Mesh network configs
│   ├── models/             # Model configurations
│   └── services/           # Service configs
│
├── tests/                   # Test suites
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
│
├── .github/                 # GitHub specific files
│   ├── workflows/          # GitHub Actions
│   └── ISSUE_TEMPLATE/     # Issue templates
│
├── assets/                  # Images, diagrams, etc.
│   └── images/             # Project images
│
└── archive/                 # Old/deprecated files
    └── oldtanchatfiles/    # Previous implementations
```

## 🔄 Migration Plan

### Phase 1: Documentation Consolidation
- Move all HTML docs to `docs/` for GitHub Pages
- Organize by category (setup, api, hardware, etc.)
- Create unified navigation

### Phase 2: Source Code Organization
- Move `tanchat/` to `src/tanchat/`
- Move `tanchat-node/` to `src/tanchat-node/`
- Consolidate UI components

### Phase 3: Scripts and Automation
- Extract scripts from documentation
- Create deployment automation
- Add monitoring tools

### Phase 4: Configuration Management
- Centralize all configs
- Add environment templates
- Document all settings

## 🎯 Benefits

1. **Clear Organization**: Easy to navigate and understand
2. **GitHub Pages Ready**: `docs/` folder can be directly served
3. **Development Friendly**: Separated source from docs
4. **Scalable**: Ready for 100-node expansion
5. **Professional**: Industry-standard layout