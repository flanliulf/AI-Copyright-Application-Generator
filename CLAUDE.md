# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains an **AI-driven Software Copyright Application Materials Generation System**. The system is designed to automatically generate complete documentation and code materials required for software copyright registration by providing necessary project requirements and technical specifications.

### Core System Components

The system consists of three main generation modules:

1. **Documentation Generation Module** - Automated creation of technical documentation and design specifications
2. **Source Code Generation Module** - Complete frontend and backend code generation for copyright submission
3. **Copyright Application Materials Module** - Specialized documents for software copyright registration process

### Key Features

- **Automated Material Generation**: Complete software copyright application materials from basic requirements
- **AI-Powered Code Creation**: Full-stack source code generation for copyright verification
- **Multiple UI Design Styles**: Twelve professional UI design options covering diverse aesthetic preferences with intelligent selection
- **User-Friendly Project Initialization**: Interactive setup with guided UI style selection and configuration
- **Standardized Documentation**: Professional technical documents meeting copyright office requirements
- **Multi-Format Output**: Generates code files, documentation, and application forms in required formats
- **Compliance Assurance**: Ensures all materials meet software copyright registration standards

### System Architecture

The system utilizes the following AI-driven generation framework:
- AI/LLM services for automated code and documentation generation
- Systematic prompt engineering for consistent output quality
- Template-based generation ensuring copyright compliance standards
- Multi-stage workflow for comprehensive material creation
- Quality assurance mechanisms for professional deliverables

### Development Context

This repository contains a complete software copyright materials generation framework:
- **requires_docs/**: Input requirements and technical specifications for any software project
- **output_docs/**: Generated copyright application materials (technical docs, user manuals, registration forms)
- **output_sourcecode/**: Complete generated source code for copyright submission
- **specs_docs/**: Fixed specification documents and templates for consistent generation
  - **ui_design_specs/**: Twelve comprehensive UI design specifications covering diverse aesthetic styles
  - **tech_stack_specs/**: Default technology stack templates
- **system_prompts/**: Seven specialized AI prompts for different generation stages
- **workflow documentation**: Step-by-step process for generating complete copyright materials

The system can process any software project requirements to generate complete copyright application packages with professional UI designs tailored to different application types.

### Important Notes

- Generated materials must comply with software copyright office requirements and standards
- All AI-generated content should be reviewed for accuracy and completeness before submission
- The system supports various software types and technical stacks for broad applicability
- Output materials are formatted specifically for copyright registration processes
- Quality assurance is essential for successful copyright application approval

### UI Design System

The system features twelve professionally designed UI styles to match diverse software application types and aesthetic preferences:

#### Professional Business Styles
1. **Corporate Style (Default)**: Professional business interface suitable for enterprise systems, management platforms, and government applications
2. **Bauhaus Style**: Function-first design with geometric purity, ideal for design tools, architectural systems, and academic platforms
3. **Art Deco Style**: Luxury aesthetics with geometric patterns, perfect for high-end e-commerce, hospitality, and cultural institutions

#### Modern & Technology Styles
4. **Cyberpunk Style**: Dark theme with technology aesthetics, ideal for developer tools, data analytics platforms, and tech-focused applications
5. **Futuristic Style**: Digital future aesthetics with HUD interfaces, suitable for data platforms, security systems, and trading applications
6. **Bold Modern Style**: Contemporary design with visual impact, perfect for creative platforms, fashion brands, and innovation products

#### Minimalist & Clean Styles
7. **Minimal Style**: Clean and content-focused design, perfect for content management systems, educational platforms, and productivity tools
8. **Japanese Style**: Zen minimalism with Wabi-Sabi aesthetics, ideal for meditation apps, cultural platforms, and lifestyle applications
9. **Scandinavian Style**: Functional simplicity with natural harmony, suitable for lifestyle apps, health platforms, and family-oriented systems

#### Creative & Artistic Styles
10. **Memphis Style**: Post-modern rebellion with color carnival, perfect for creative platforms, entertainment media, and youth social applications
11. **Pop Art Style**: Mass culture aesthetics with bright colors, ideal for entertainment platforms, fashion shopping, and creative marketing tools
12. **Elegant Vintage Style**: Classic printing aesthetics with warm tones, suitable for cultural education, academic research, and museum applications

#### UI Style Selection Methods:
- **Interactive Setup**: Choose during project initialization with `python3 scripts/init/init_project.py`
- **Configuration**: Set `ui_design_style` parameter in `ai-copyright-config.json`
- **Custom Override**: Create custom UI specification in `requires_docs/UI设计规范.md`

#### Priority System:
Custom UI Specification > User-Selected Style > System Default (Corporate)